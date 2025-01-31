#!/usr/bin/env python3
"""
Author : Teddy Xinyuan Chen <45612704+tddschn@users.noreply.github.com>
Date   : 2024-05-18
"""

import pathlib
import json
import argparse
from apple_vision_utils import __version__
from apple_vision_utils.utils import image_to_text, pdf_to_images, process_pdf


def main():
    parser = argparse.ArgumentParser(
        description="Extract text from an image or PDF using Apple's Vision framework."
    )
    parser.add_argument("file_path", type=str, help="Path to the image or PDF file.")
    parser.add_argument(
        "-j", "--json", action="store_true", help="Output results in JSON format."
    )
    parser.add_argument(
        "-p", "--pdf", action="store_true", help="Specify if the input file is a PDF."
    )
    parser.add_argument(
        "-l",
        "--lang",
        type=str,
        default="zh-Hant",
        help="Specify the language for text recognition (e.g., eng, fra, deu, zh-Hans for Simplified Chinese, zh-Hant for Traditional Chinese). Default is 'zh-Hant', which works with images containing both Chinese characters and latin letters.",
    )
    parser.add_argument(
        "--pdf2image-only",
        action="store_true",
        help="Only convert PDF to images without performing OCR.",
    )
    parser.add_argument(
        "--pdf2image-dir",
        type=str,
        help="Specify the directory to store output images. By default, a secure temporary directory is created.",
    )
    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    args = parser.parse_args()

    file_path = pathlib.Path(args.file_path)
    if not file_path.is_file():
        parser.error("Invalid file path")
    file_path = str(file_path.resolve())

    if args.pdf2image_only:
        output_dir = args.pdf2image_dir
        img_paths = pdf_to_images(file_path, output_dir=output_dir)
        print(f"Images saved to: {output_dir or 'a secure temporary directory'}")
        for img_path in img_paths:
            print(img_path)
        return

    if args.pdf:
        results = process_pdf(file_path, lang=args.lang)
    else:
        results = image_to_text(file_path, lang=args.lang)

    if args.json:
        print(json.dumps(results, indent=2, ensure_ascii=False))
    else:
        for result in results:
            print(result["text"])


if __name__ == "__main__":
    main()
