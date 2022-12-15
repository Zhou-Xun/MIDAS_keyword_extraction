import fitz
import os

import sys, getopt
from io import BytesIO


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


def partial_ocr_for_one_pdf(filenames, file_path, output_dir):
    '''
    output: the partial ocr result for each pdf
    :return:
    '''
    for filename in os.listdir(output_dir):
        f = os.path.join(output_dir, filename)
        os.remove(f)

    for i in range(len(file_path)):
        file = file_path[i]
        name = filenames[i]
        if file[-3:] == "pdf":
            with open(file, "rb") as fh:
                buf = BytesIO(fh.read())
            doc = fitz.open(file, buf)
            text = ""
            for page in doc:
                partial_tp = page.get_textpage_ocr(flags=0, full=False)
                tmp = page.get_text(textpage=partial_tp).replace("\n", " ")
                text += tmp + " "
            with open(os.path.join(output_dir, filenames[i][:-3] + "txt"), 'w') as f:
                f.write(text)


def partial_ocr_for_one_page(filenames, file_path, output_dir):
    '''
    output: the partial ocr result for each page
    :return: 
    '''
    for filename in os.listdir(output_dir):
        f = os.path.join(output_dir, filename)
        os.remove(f)

    for i in range(len(file_path)):
        file = file_path[i]
        if file[-3:] == "pdf":
            with open(file, "rb") as fh:
                buf = BytesIO(fh.read())
            doc = fitz.open(file, buf)

            for j in range(len(doc)):
                page = doc[j]
                partial_tp = page.get_textpage_ocr(flags=0, full=False)
                text = page.get_text(textpage=partial_tp).replace("\n", " ")

                with open(os.path.join(output_dir, filenames[i][:-4] + "_page_" + str(j) + ".txt"), 'w') as f:
                    f.write(text)


def main():
    args = sys.argv[1:]
    try:
        opts, args = getopt.getopt(args, "h-m:", ["mode="])
    except getopt.GetoptError:
        print('test.py -i <id> -q <query>')
        sys.exit(2)

    mode = "file"
    for opt, arg in opts:
        if opt in ("-m", "--mode"):
            mode = arg

    input_dir = "input_pdf"
    output_dir = "output_txt"
    filenames, file_path = read_filename_and_path(input_dir)
    if mode == "page":
        partial_ocr_for_one_page(filenames, file_path, output_dir)
    else:
        partial_ocr_for_one_pdf(filenames, file_path, output_dir)


if __name__ == '__main__':
    print("start ocr")
    main()

