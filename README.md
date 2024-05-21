# Apple Vision Framework Python Utilities

Fast and accurate OCR on images and PDFs using Apple Vision framework (`pyobjc-framework-Vision`) directly from command line.

- [Apple Vision Framework Python Utilities](#apple-vision-framework-python-utilities)
  - [Features](#features)
  - [Demo](#demo)
  - [Installation](#installation)
    - [pipx](#pipx)
    - [pip](#pip)
  - [Usage](#usage)
  - [Develop](#develop)
  - [Test](#test)

## Features

- Fast and accurate, multi-language support (`-l`, `--lang`), powered by Apple's industry-strength Vision framework (`pyobjc-framework-Vision`).
- Supports all common input image formats: PNG, JPEG, TIFF and WebP.
- Supports PDF input (the file gets converted to images first). This tool does NOT assume a file is PDF just because it has a `.pdf` extension, you need to pass `-p`, `--pdf` flag.
- Outputs extracted text only by default, but can output in JSON format containing confidence of recognition for each line with `-j`, `--json` flag.


## Demo

Below is the output of running the [tests](#test):

https://g.teddysc.me/96d5b1217b90035c163b3c97ce99112f

## Installation

Requires Python >= 3.11, <4.0.

Since this package uses Apple's Vision framework, it only works on macOS.

To OCR PDFs with `-p`, you need to install required dependency `poppler` with `brew install poppler` ([detailed guide](https://github.com/Belval/pdf2image)).

### pipx

This is the recommended installation method.

```
$ pipx install apple-vision-utils
```

### [pip](https://pypi.org/project/apple-vision-utils/)

```
$ pip install apple-vision-utils
```

## Usage

```
$ apple-ocr --help

usage: apple-ocr [-h] [-j] [-p] [-l LANG] [--pdf2image-only]
                 [--pdf2image-dir PDF2IMAGE_DIR] [-V]
                 file_path

Extract text from an image or PDF using Apple's Vision framework.

positional arguments:
  file_path             Path to the image or PDF file.

options:
  -h, --help            show this help message and exit
  -j, --json            Output results in JSON format.
  -p, --pdf             Specify if the input file is a PDF.
  -l LANG, --lang LANG  Specify the language for text recognition (e.g., eng,
                        fra, deu, zh-Hans for Simplified Chinese, zh-Hant for
                        Traditional Chinese). Default is 'zh-Hant', which
                        works with images containing both Chinese characters
                        and latin letters.
  --pdf2image-only      Only convert PDF to images without performing OCR.
  --pdf2image-dir PDF2IMAGE_DIR
                        Specify the directory to store output images. By
                        default, a secure temporary directory is created.
  -V, --version         show program's version number and exit
```


## Develop

```
$ git clone https://github.com/tddschn/apple-vision-utils.git
$ cd apple-vision-utils
$ poetry install
```

## Test

```
# in the root of the project
poetry install
poetry shell
cd tests && ./test.sh
```