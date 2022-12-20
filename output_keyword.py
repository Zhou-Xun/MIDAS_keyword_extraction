# Xun Zhou (xunzhou)
import os
import sys, getopt
import json

sys.path.append("./model")
import keyphrase_extraction_kbir_inspec as kbir
import bert_uncased_keyword_extractor as bert
from keyphrasetransformer import KeyPhraseTransformer


def read_filename_and_path(txt_directory):
    filenames = []
    file_path = []

    # iterate over files in
    # that directory
    for filename in os.listdir(txt_directory):
        f = os.path.join(txt_directory, filename)
        # checking if it is a file
        if os.path.isfile(f):
            filenames.append(filename)
            file_path.append(f)

    return filenames, file_path


def kbir_inspec(filenames, file_path):
    model_name = "ml6team/keyphrase-extraction-kbir-inspec"
    extractor = kbir.KeyphraseExtractionPipeline(model=model_name)

    output_dict = dict()

    for i in range(len(file_path)):
        file = file_path[i]
        filename = filenames[i]
        with open(file, "r") as text_file:
            text = text_file.read()
            key_phrases = extractor(text)
            output_dict[filename] = list(key_phrases)

    return output_dict


def bert_keyword_extraction(filenames, file_path):
    model_name = "yanekyuk/bert-uncased-keyword-extractor"
    extractor = bert.KeyphraseExtractionPipeline(model=model_name)

    output_dict = dict()

    for i in range(len(file_path)):
        file = file_path[i]
        filename = filenames[i]
        with open(file, "r") as text_file:
            text = text_file.read()
            key_phrases = extractor(text)
            output_dict[filename] = list(key_phrases)

    return output_dict


def snrspeaks_keyphrase_transformer(filenames, file_path):
    kp = KeyPhraseTransformer()
    output_dict = dict()

    for i in range(len(file_path)):
        file = file_path[i]
        filename = filenames[i]
        with open(file, "r") as text_file:
            text = text_file.read()
            key_phrases = kp.get_key_phrases(text)
            output_dict[filename] = key_phrases

    return output_dict


def dict_to_json(output_dict, json_path):

    with open(json_path, 'w', encoding="utf-8") as file_obj:
        json.dump(output_dict, file_obj, indent=2)


def main():
    args = sys.argv[1:]
    try:
        opts, args = getopt.getopt(args, "hm:", ["model="])
    except getopt.GetoptError:
        print('output_keyword.py -m <model>')
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-m", "--model"):
            model = arg

    txt_directory = "output_txt"
    json_path = "output_keyword"
    filenames, file_path = read_filename_and_path(txt_directory)
    if model == "kbir":
        json_path += "/kbir_output.json"
        output_dict = kbir_inspec(filenames, file_path)
    elif model == "bert":
        json_path += "/bert_output.json"
        output_dict = bert_keyword_extraction(filenames, file_path)
    elif model == "skt":
        json_path += "/skt_output.json"
        output_dict = snrspeaks_keyphrase_transformer(filenames, file_path)

    dict_to_json(output_dict, json_path)


if __name__ == "__main__":
    main()


