## MIDAS_keyword_extraction
This project is for MIDAS team to extract keywords from pdf files.<br>
There are three sections in this project:
- fit_Tesseract_OCR.py: Extract text from pdf using partial ocr
- output_keyword.py: Extract keyword from text using different models(3 models for now)
- old directory: Old project for keyword extraction(including how to build wiki dictionary and how to use rake)
  - For details, please see README.md in the old directory.

<ol>
    <li>Extract text from pdf using partial ocr</li>
    <ol>
        <li>How to run: `python fitz_Tesseract_OCR.py [-m page]`</li>

</ol>
    <li>Keyphrase extraction</li>
</ol>



#### Install Tesseract

- Windows
    - go to `https://github.com/UB-Mannheim/tesseract/wiki`
    - download installer `tesseract-ocr-w64-setup-v5.2.0.20220712.exe`
    - Follow the step
- Mac OS
    - brew install tesseract
    
#### install fitz

- python -m pip install --upgrade pymupdf

#### Reference

- The library I'm using is `PyMuPDF`, and below is the demo code
    - https://github.com/pymupdf/PyMuPDF-Utilities/blob/master/jupyter-notebooks/partial-ocr.ipynb
    
#### Make sure you have TESSDATA_PREFIX in your os env

- Windows
    - configure `TESSDATA_PREFIX` as `C:\Program Files\Tesseract-OCR\tessdata`
- Mac OS
    - I use homebrew to install Tesseract, so my tessdata is in
        - `/opt/homebrew/Cellar/tesseract/5.2.0/share/tessdata`
    - vim ~/.zprofile
        - `export TESSDATA_PREFIX=/opt/homebrew/Cellar/tesseract/5.2.0/share/tessdata`
        - `export PATH=$TESSDATA_PREFIX:$PATH`'
    - source ~/.zprofile
    - restart anaconda
