#!/usr/bin/env bash

# Define the input paths
declare -a files=("data/en.jpg" "data/en.png" "data/en.tiff" "data/en.webp" "data/zh_CN.pdf" "data/zh_CN.png")

SCRIPT_COMMAND='apple-ocr'

# Define a function to print a horizontal rule
function hr() {
    echo "---------------------------------------------"
}

# Test the script with different options
for file in "${files[@]}"; do
    echo "Testing file: $file"
    hr

    # Determine the language option based on file name
    lang_opt=""
    if [[ "$file" == data/en.* ]]; then
        lang_opt="-l eng"
    fi


    # If the file is a PDF, run additional tests
    if [[ "$file" == *.pdf ]]; then
        # Run the script with the appropriate language option
        $SCRIPT_COMMAND "$file" $lang_opt -p
        hr
        # Test PDF to text with JSON output
        echo "Test: PDF to text with JSON output"
        $SCRIPT_COMMAND "$file" -p -j
        hr

        # Test PDF to images only with default temp directory
        echo "Test: PDF to images only with default temp directory"
        $SCRIPT_COMMAND "$file" -p --pdf2image-only
        hr

        # Test PDF to images only with specified output directory
        output_dir="output_images"
        echo "Test: PDF to images only with specified output directory"
        $SCRIPT_COMMAND "$file" -p --pdf2image-only --pdf2image-dir "$output_dir"
        hr

        # Cleanup the created non-temp directory
        if [ -d "$output_dir" ]; then
            echo "Cleaning up: $output_dir"
            rm -rf "$output_dir"
        fi
    else
        # Run the script with the appropriate language option
        $SCRIPT_COMMAND "$file" $lang_opt
        hr
    fi
done

echo "All tests completed."