import re


def clean_ocr_text(raw_text: str) -> str:
    """
    OCR se aaye hue raw text ko clean karta hai.
    - Extra spaces hatata hai
    - Non-printable/garbage characters kam karta hai
    - Basic normalization karta hai
    """
    if not raw_text:
        return ""

    # Multiple spaces ko ek space mein convert karna
    text = re.sub(r'\s+', ' ', raw_text)

    # Bohot ajeeb characters hatana (lekin numbers, letters, basic punctuation rakhna)
    text = re.sub(r'[^\w\s.,:/\-()]', ' ', text)

    # Dobara extra spaces clean karna (upar wale step ke baad)
    text = re.sub(r'\s+', ' ', text)

    return text.strip()


if __name__ == "__main__":
    sample = "C1z 24/ /2 c9 60   Lu Ls Cn  042-3624238144 CLOSED ON: SATURDAY"
    print(clean_ocr_text(sample))
