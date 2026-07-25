import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
from ai_engine.gemma.gemma_prompt import SYSTEM_PROMPT

load_dotenv()

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))


def get_gemma_response(ocr_text: str) -> str:
    """
    OCR se nikla hua text Gemma ko bhejta hai aur uska raw JSON response return karta hai.

    Args:
        ocr_text: Cleaned OCR text prescription se

    Returns:
        Gemma ka raw JSON string response
    """
    prompt = f"Here is the extracted prescription text:\n\n{ocr_text}\n\nAnalyze it according to your instructions."

    response = client.models.generate_content(
        model="gemma-4-26b-a4b-it",
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            response_mime_type="application/json",
        )
    )
    return response.text


if __name__ == "__main__":
    sample_text = "Panadol 500mg BD x 5 days. Amoxicillin 250mg TDS x 7 days."
    result = get_gemma_response(sample_text)
    print(result)
