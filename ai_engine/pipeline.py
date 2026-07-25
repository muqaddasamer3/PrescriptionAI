from ai_engine.ocr.ocr_extractor import get_full_text
from ai_engine.ocr.text_cleaner import clean_ocr_text
from ai_engine.gemma.gemma_client import get_gemma_response
from ai_engine.gemma.response_parser import parse_gemma_response


def process_prescription(image_path: str) -> dict:
    """
    Poora pipeline: prescription image se lekar final structured JSON tak.
    """
    raw_text = get_full_text(image_path)

    if not raw_text or raw_text.strip() == "":
        return {
            "error": "No text could be extracted from the image. Please upload a clearer image."
        }

    cleaned_text = clean_ocr_text(raw_text)
    gemma_raw_response = get_gemma_response(cleaned_text)
    parsed_result = parse_gemma_response(gemma_raw_response)

    if parsed_result is None:
        return {
            "error": "Could not parse AI response. Please try again.",
            "raw_response": gemma_raw_response
        }

    parsed_result["raw_ocr_text"] = cleaned_text
    return parsed_result


if __name__ == "__main__":
    result = process_prescription("ai_engine/sample.jpg")
    import json
    print(json.dumps(result, indent=2, ensure_ascii=False))
