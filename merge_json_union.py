import os
import json

def read_filename_and_path(pdf_directory):
    filenames = []
    file_path = []

    # iterate over files in
    # that directory
    for filename in os.listdir(pdf_directory):
        f = os.path.join(pdf_directory, filename)
        # checking if it is a file
        if os.path.isfile(f):
            filenames.append(filename)
            file_path.append(f)

    return filenames, file_path


def read_json_and_merge(file_path):
    keyword_list = []
    for file in file_path:
        if file[-4:] == "json":
            with open(file) as f:
                data = json.load(f)
            for value in data.values():
                keyword_list += list(map(lambda x: x.lower(), value))

    keyword_list = list(set(keyword_list))
    with open('output_keyword/keyword.txt', 'w') as f:
        for keyword in keyword_list:
            f.write(f"{keyword}\n")


def main():
    filenames, file_path = read_filename_and_path("output_keyword")
    # print((filenames, file_path))
    read_json_and_merge(file_path)


if __name__ == '__main__':
    main()