# Thomas Horak (thorames)
# glossary_transcripts.py
import nltk
nltk.download('stopwords')

import re
import os
import csv
import sys
import json
import string
import operator
import pandas as pd
import requests
import editdistance
import tqdm as tqdm
from datetime import date
from nltk.util import ngrams
from collections import Counter
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from multi_rake import Rake as Multi_Rake
from nltk.tokenize import sent_tokenize, word_tokenize
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from nltk.corpus import stopwords
stopwords = set(stopwords.words('english'))
stemmer = PorterStemmer()
lemmatizer = WordNetLemmatizer()


def read_transcripts(transcript_directory):
    transcripts = {}

    input_files = [files for (path, dir, files) in os.walk(transcript_directory)]

    for file in input_files[0]:
        transcript_name = file.split(".")[0]
        file_path = (transcript_directory + '/' + file)

        if ".json" in file_path:
            with open(file_path) as json_file:
                document = json.load(json_file, strict=False)
                transcripts[transcript_name] = document['results']['transcripts'][0]['transcript']
                #transcripts[transcript_name] = document["transcript"]["full_transcript"]

    return transcripts


def read_text(transcript_directory):
    transcripts = {}

    input_files = [files for (path, dir, files) in os.walk(transcript_directory)]

    for file in input_files[0]:
        transcript_name = file.split(".")[0]
        file_path = (transcript_directory + '/' + file)

        if ".txt" in file_path:
            with open(file_path, "r") as text_file:
                transcripts[transcript_name] = text_file.read()

    return transcripts


def read_text_files(text_directory):
    transcripts = {}

    files = [[(path + '/' + file) for file in files] for (path, dir, files) in os.walk(text_directory)][0]

    for file in files:
        with open(file) as csvin:
            reader = csv.reader(csvin, delimiter=',')

            rows = [row for row in reader]
            rows = rows[0][0].split("\n")
            rows = [re.sub('\t', ' ', row) for row in rows]
            rows = [row for row in rows if len(row) > 3]
            transcripts[(file.split('/')[1]).split(".")[0]] = " ".join(rows)

    return transcripts

def read_definitions(definitions_file):
    with open(definitions_file) as tsvin:
        reader = csv.reader(tsvin, delimiter='\t')

        for row in reader:
            yield (row[0], row[1])

def rake_keywords(transcripts):
    for key, value in transcripts.items():
        rake = Multi_Rake(min_chars=3, max_words=5, min_freq=1, language_code='en')
        yield (key, [keyword for keyword, score in rake.apply(value)])

def ngram_keywords(transcripts):
    for key, value in transcripts.items():
        unigrams = [phrase[0] for phrase in list(ngrams(value.split(), 1))]
        bigrams = [" ".join([phrase[0], phrase[1]]) for phrase in list(ngrams(value.split(), 2))]
        trigrams = [" ".join([phrase[0], phrase[1], phrase[2]]) for phrase in list(ngrams(value.split(), 3))]
        quadgrams = [" ".join([phrase[0], phrase[1], phrase[2], phrase[3]]) for phrase in list(ngrams(value.split(), 4))]
        yield (key, list(set(unigrams + bigrams + trigrams + quadgrams)))

def clean_phrase(phrase):
    phrase = "".join([char if char not in string.punctuation else '' for char in phrase]).strip()
    #phrase = phrase.split("  ")[0].lower()
    #phrase = phrase.strip().lower()
    #return " ".join([token for token in phrase.split() if token not in stopwords])
    return "".join(phrase.split()).lower()

def stem_phrase(phrase):
    #return " ".join([stemmer.stem(token) for token in phrase.split()])
    # return " ".join([lemmatizer.lemmatize(token) for token in phrase.split()])
    return phrase

def search_definitions(term, definitions):
    #definitions = dict([(clean_phrase(key), value) for key, value in definitions.items()])
    stemmed_definitions = dict([(key, stem_phrase(clean_phrase(key))) for key, value in definitions.items()])
    #term = clean_phrase(term)
    stemmed_term = stem_phrase(clean_phrase(term))

    if term.lower() in definitions.keys():
        return (term, definitions[term.lower()])

    if len(stemmed_term):
        distances = [(key, editdistance.eval(stemmed_term, value)) for key, value in stemmed_definitions.items() if len(value)]
        sorted_distances = sorted(distances, key=operator.itemgetter(1))
        print("???")
        print(sorted_distances)
        if (sorted_distances[0][1] / (sum([len(sorted_distances[0][0]), len(term)]) / 2)) < 0.1:
            return (sorted_distances[0][0], definitions[sorted_distances[0][0]])

        # if term.lower() in text:
        #     return (term, "Appear in definitions")

def search_terms(keyword, terms):
    """
    Calculate the edit distance between keyword and each term
    Check if the closest term meet the threshold, and return that term if so
    :param keyword:
    :param terms:
    :return term that meets the threshold:
    """
    # lower the case of terms list
    terms_lower = [term.lower() for term in terms]
    # remove the punctuations and lower the case
    cleaned_keyword = clean_phrase(keyword).lower()

    # Data structure of distances: [(term_1, edit distance between term_1 and keyword),...()]
    distances = []

    if not cleaned_keyword:
        return None

    for i in range(len(terms_lower)):
        distances.append((terms[i], editdistance.eval(cleaned_keyword, terms_lower[i])))

    sorted_distances = sorted(distances, key=operator.itemgetter(1))
        # Threshold.
        # Basically this threshold means divide the shortest edit distance by the average length of keyword and term
    if (sorted_distances[0][1] / (sum([len(sorted_distances[0][0]), len(cleaned_keyword)]) / 2)) < 0.1:
            # return the term
        return sorted_distances[0][0]


def prep_output(keywords, count, key):
    day = date.fromordinal(738037 + (count * 4))
    return [{"date": day, "corpus_name": key, "keyword": term, "definition": definition} for term, definition in keywords]


def prep_output_terms_only(terms, key):
    return [{"corpus_name": key, "keyword": term} for term in terms]


def output_keywords(key, keywords):
    output = json.dumps({key.split("_")[0]: keywords}, indent=4, sort_keys=True, default=str)

    with open(key, 'w+') as output_file:
        output_file.write(output)


def generate_keywords_for_transcripts(transcript_directory, definitions):
    # transcripts = read_transcripts(transcript_directory)
    # transcripts = read_text_files(transcript_directory)
    transcripts = read_text(transcript_directory)

    rakes = dict(rake_keywords(transcripts))

    #rakes = dict(ngram_keywords(transcripts))
    total_hits = {}
    count = 0
    output = []
    for key, value in tqdm.tqdm(rakes.items()):
        hits = {}
        for keyword in tqdm.tqdm(value):
            print(keyword)
            hit = search_definitions(keyword, definitions)
            if hit:
                if hit[0] not in hits:
                    hits[hit[0]] = hit[1]
                if hit[0] not in total_hits:
                    total_hits[hit[0]] = hit[1]

        sorted_vocab = sorted(hits.items(), key=operator.itemgetter(0))
        output += prep_output(sorted_vocab, count, key)

        count += 1

        print("-----" + key + "-----")
        for term, definition in sorted_vocab:
            print(term)
        print("\n")

    #sorted_vocab = sorted(total_hits.items(), key=operator.itemgetter(0))

    # output_keywords("CLIMATE102_Keywords.json", output)
    output_keywords("CHEM451_Keywords_final.json", output)


def generate_keywords_for_transcripts_terms_only(transcript_directory, terms, output_path):
    # return a dictionary, keys: name of each transcript, values: text of each transcript
    transcripts = read_text(transcript_directory)

    # return a dictionary, keys: name of each transcript, values: extracted keywords based on rake for each transcript
    rakes = dict(rake_keywords(transcripts))

    output = []
    for key, value in tqdm.tqdm(rakes.items()):
        # key: corpus name, value: corpus text
        print("Extracting corpus: {}".format(key))
        terms_each_transcipt = set()
        for keyword in tqdm.tqdm(value):
            term = search_terms(keyword, terms)
            if term:
                terms_each_transcipt.add(term)

        terms_each_transcipt = sorted(terms_each_transcipt)
        output += prep_output_terms_only(terms_each_transcipt, key)

    output_keywords(output_path, output)

def main():
    # transcript_directory = sys.argv[1]
    # definitions_file = sys.argv[2]

    # definitions = dict(read_definitions(definitions_file))
    # definitions = dict((k.lower(), v.lower()) for k,v in definitions.items())
    #
    # generate_keywords_for_transcripts(transcript_directory, definitions)

    transcript_directory = "data/output_451"
    dictionary = "Glossaries/All_Terms.csv"
    output_path = "output/CHEM451_Keywords_only_terms.json"


    # 1. first read the dictionary, get a list of terms
    terms = pd.read_csv(dictionary, header=None)
    terms = list(terms[0].values)

    # 2. generate keywords according to the transcript and terms
    generate_keywords_for_transcripts_terms_only(transcript_directory, terms, output_path)

main()
# main("data/output_451", "Glossaries/Chem.csv")
# main("data/lectures", "Glossaries/Inorganic_Chemistry.csv")