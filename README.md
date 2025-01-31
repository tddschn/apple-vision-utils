# Apple Vision Framework Python Utilities

Fast and accurate OCR on images and PDFs using Apple Vision framework (`pyobjc-framework-Vision`) directly from command line.

- [Apple Vision Framework Python Utilities](#apple-vision-framework-python-utilities)
  - [Features](#features)
  - [Demo](#demo)
  - [Installation](#installation)
    - [pipx](#pipx)
    - [pip](#pip)
    - [`uv tool` installation doesn't work](#uv-tool-installation-doesnt-work)
  - [Usage](#usage)
    - [Command Line](#command-line)
    - [As a Library](#as-a-library)
  - [Develop](#develop)
  - [Test](#test)

## Features

- Fast and accurate, multi-language support (`-l`, `--lang`), powered by Apple's industry-strength Vision framework (`pyobjc-framework-Vision`).
- Supports all common input image formats: PNG, JPEG, TIFF and WebP.
- Supports PDF input (the file gets converted to images first). This tool does NOT assume a file is PDF just because it has a `.pdf` extension, you need to pass `-p`, `--pdf` flag.
- Outputs extracted text only by default, but can output in JSON format containing confidence of recognition for each line with `-j`, `--json` flag.
- Supports text clipping based on start and end markers (`-s`, `-S`, `-e`, `-E`).

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

### `uv tool` installation doesn't work

I tried to install this with `uv tool install` using different Python versions on Apple Silicon Mac, it didn't work. May be caused by some peculiarities of objc interfacing libs. Just use `pipx` for now.

## Usage

### Command Line

```
$ apple-ocr --help

usage: apple-ocr [-h] [-j] [-p] [-l LANG] [--pdf2image-only] [--pdf2image-dir PDF2IMAGE_DIR] [-s START_MARKER_INCLUSIVE] [-S START_MARKER_EXCLUSIVE] [-e END_MARKER_INCLUSIVE] [-E END_MARKER] [-V] file_path

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
  -s START_MARKER_INCLUSIVE, --start-marker-inclusive START_MARKER_INCLUSIVE
                        Specify the start marker (included, as the first line of the extracted text) for text extraction in PDF.
  -S START_MARKER_EXCLUSIVE, --start-marker-exclusive START_MARKER_EXCLUSIVE
                        Specify the start marker (excluded, as the first line of the extracted text) for text extraction in PDF.
  -e END_MARKER_INCLUSIVE, --end-marker-inclusive END_MARKER_INCLUSIVE
                        Specify the end marker (included, as the last line of the extracted text) for text extraction in PDF.
  -E END_MARKER, --end-marker END_MARKER
                        Specify the end marker (excluded, as the last line of the extracted text) for text extraction in PDF.
  -V, --version         show program's version number and exit
```

### As a Library

You can also use the utility functions in your own Python code:

```python
from apple_vision_utils.utils import image_to_text, pdf_to_images, process_pdf, clip_results

# Extract text from an image
results = image_to_text("path/to/image.png", lang="eng")

# Convert PDF to images
images = pdf_to_images("path/to/document.pdf")

# Process PDF for text recognition
pdf_results = process_pdf("path/to/document.pdf", lang="eng")

# Clip text results based on markers
clipped_results = clip_results(results, start_marker_inclusive="Start", end_marker_exclusive="End")
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