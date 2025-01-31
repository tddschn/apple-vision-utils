"""Utility functions for Apple Vision text recognition."""

import pathlib
import tempfile
import os


def image_to_text(img_path: str, lang: str = "eng") -> list:
    """Extract text from an image using Apple's Vision framework.

    Args:
        img_path: Path to the image file.
        lang: Language code for text recognition. Examples:
            - eng: English
            - fra: French
            - deu: German
            - zh-Hans: Simplified Chinese
            - zh-Hant: Traditional Chinese

    Returns:
        List of dictionaries containing recognized text and confidence scores.
        Example: [{"text": "Hello", "confidence": 0.95}, ...]
    """
    from Cocoa import NSURL
    from Foundation import NSDictionary
    import Quartz
    import Vision
    from wurlitzer import pipes

    input_url = NSURL.fileURLWithPath_(img_path)

    with pipes() as (out, err):
        input_image = Quartz.CIImage.imageWithContentsOfURL_(input_url)

    vision_options = NSDictionary.dictionaryWithDictionary_({})
    vision_handler = Vision.VNImageRequestHandler.alloc().initWithCIImage_options_(
        input_image, vision_options
    )
    results = []
    handler = make_request_handler(results)
    vision_request = Vision.VNRecognizeTextRequest.alloc().initWithCompletionHandler_(
        handler
    )
    vision_request.setRecognitionLanguages_([lang])
    vision_handler.performRequests_error_([vision_request], None)

    return results


def make_request_handler(results: list):
    """Create a handler function for Vision framework requests.

    Args:
        results: List to store recognition results.

    Returns:
        Handler function for Vision framework requests.
    """
    if not isinstance(results, list):
        raise ValueError("results must be a list")

    def handler(request, error):
        if error:
            print(f"Error! {error}")
        else:
            observations = request.results()
            for text_observation in observations:
                recognized_text = text_observation.topCandidates_(1)[0]
                results.append(
                    {
                        "text": recognized_text.string(),
                        "confidence": recognized_text.confidence(),
                    }
                )

    return handler


def pdf_to_images(pdf_path: str, output_dir: str = None) -> list:
    """Convert PDF file to images.

    Args:
        pdf_path: Path to the PDF file.
        output_dir: Directory to save the generated images.
            If None, creates a temporary directory.

    Returns:
        List of paths to the generated image files.
    """
    from pdf2image import convert_from_path

    if output_dir is None:
        output_dir = tempfile.mkdtemp()
    else:
        pathlib.Path(output_dir).mkdir(parents=True, exist_ok=True)

    images = convert_from_path(pdf_path)
    img_paths = []
    for i, image in enumerate(images):
        img_path = os.path.join(output_dir, f"page_{i}.png")
        image.save(img_path, "PNG")
        img_paths.append(img_path)
    return img_paths


def process_pdf(pdf_path: str, lang: str) -> list:
    """Process PDF file for text recognition.

    Args:
        pdf_path: Path to the PDF file.
        lang: Language code for text recognition.

    Returns:
        List of dictionaries containing recognized text and confidence scores.
    """
    images = pdf_to_images(pdf_path)
    results = []
    for img_path in images:
        results.extend(image_to_text(img_path, lang))
    return results


def clip_results(
    results: list,
    start_marker_inclusive: str = None,
    start_marker_exclusive: str = None,
    end_marker_inclusive: str = None,
    end_marker_exclusive: str = None,
) -> list:
    """Clip text results based on start and end markers.

    Args:
        results: List of dictionaries containing recognized text and confidence scores.
        start_marker_inclusive: Start marker for text extraction (inclusive).
        start_marker_exclusive: Start marker for text extraction (exclusive).
        end_marker_inclusive: End marker for text extraction (inclusive).
        end_marker_exclusive: End marker for text extraction (exclusive).

    Returns:
        List of dictionaries containing clipped text and confidence scores.
    
        
    Example:
        results = [
            {"text": "before", "confidence": 0.95},
            {"text": "cjskaj Start marker lsjdkjfjdwo", "confidence": 0.95}, # only check if marker is in text, doesn't need to 100% match
            {"text": "Text", "confidence": 0.90},
            {"text": "End marker", "confidence": 0.85},
            {"text": "after", "confidence": 0.85},
        ]
        clipped_results = clip_results(
            results,
            start_marker_inclusive="Start",
            end_marker="End",
        )
        print(clipped_results)
        # Output: [{"text": "Start marker", "confidence": 0.95}, {"text": "Text", "confidence": 0.90}]
    """
    clipped = []
    capturing = (not start_marker_inclusive) and (not start_marker_exclusive)
    for item in results:
        text = item["text"]
        if not capturing:
            if (start_marker_inclusive and start_marker_inclusive in text):
                capturing = True
                clipped.append(item)
                continue
            if (start_marker_exclusive and start_marker_exclusive in text):
                capturing = True
                continue
        else:
            if (end_marker_inclusive and end_marker_inclusive in text):
                clipped.append(item)
                break
            if (end_marker_exclusive and end_marker_exclusive in text):
                break
            clipped.append(item)
    return clipped