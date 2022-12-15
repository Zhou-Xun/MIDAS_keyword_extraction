# MIDAS_keyword_extraction

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
