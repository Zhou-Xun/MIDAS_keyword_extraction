# Thomas Horak (thorames)
# category_glossary.py
import os
import re
import csv
import wikipediaapi
import tqdm as tqdm
import pandas as pd
from nltk.tokenize import sent_tokenize

def generate_terms(wiki, domain):
    category = ["Category:" + domain]
    categories = category + [link for link in list(wiki.page(category).categorymembers.keys()) if "Category:" in link]

    print("Generating Terms...")

    terms = []
    for category in tqdm.tqdm(categories):
        for result in list(wiki.page(category).categorymembers):
            if "Category:" not in result:
                if result not in terms:
                    terms.append(result)

    return sorted(terms)

def generate_glossary(wiki, terms):
    print("Generating Definitions...")

    for term in tqdm.tqdm(terms):
        try:
            definition = wiki.page(term).summary

            if len(definition) < 100:
                continue

            definition = re.sub('\n', ' ', definition)
            definition = re.split(r'[\s]{3,}', definition)

            if len(definition) == 1:
                yield (term, " ".join(definition))
        except:
            continue

def output_glossary(glossary, domain):
    with open("Glossaries/" + re.sub(r'\s', '_', domain).title() + ".csv", 'w+') as output_file:
        csv_output = csv.writer(output_file, delimiter='\t')

        for term, definition in glossary:
            csv_output.writerow([term, definition])

def output_terms(terms, domain):
    pd.DataFrame(terms).to_csv("Glossaries/" + re.sub(r'\s', '_', domain).title() + ".csv", index=False, header=None)

def main():
    # Specify the domain and language library
    domains = ["chemistry", "Inorganic chemistry", "biology", "biochemistry"]
    wiki = wikipediaapi.Wikipedia('en')

    if not os.path.isdir("Glossaries"):
        os.mkdir("Glossaries")

    all_terms = []
    # A list of terms that are related to the domain
    for domain in domains:
        print("generating domain: {}".format(domain))
        terms = generate_terms(wiki, domain)
        all_terms += terms
        output_terms(terms, domain)

    # output all terms to a csv
    output_terms(sorted(set(all_terms)), "all_terms")

    # glossary = list(generate_glossary(wiki, terms))
    # output_glossary(glossary, domain)

main()