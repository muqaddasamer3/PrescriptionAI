import easyocr
from typing import List, Dict

# Reader ko ek hi baar initialize karna behtar hai (bar bar load na ho)
reader = easyocr.Reader(['en'], gpu=False)


def extract_text_from_image(image_path: str) -> List[Dict]:
    """
    Prescription image se text extract karta hai.

    Args:
        image_path: Prescription image ka file path

    Returns:
        List of dicts, har dict mein: text, confidence, bounding_box
    """
    results = reader.readtext(image_path)

    extracted_data = []
    for (bbox, text, confidence) in results:
        extracted_data.append({
            "text": text,
            "confidence": round(confidence, 2),
            "bounding_box": bbox
        })

    return extracted_data


def get_full_text(image_path: str) -> str:
    """
    Sirf plain text return karta hai (Gemma ko bhejne ke liye).
    """
    data = extract_text_from_image(image_path)
    return " ".join([item["text"] for item in data])


if __name__ == "__main__":
    # Testing ke liye
    sample_path = "sample_prescription.jpg"
    result = extract_text_from_image(sample_path)
    for item in result:
        print(f"Text: {item['text']} | Confidence: {item['confidence']}")
