import base64
import json
import re

import httpx

from app.core.config import settings

SYSTEM_PROMPT = """You are a Prescription Explainer assistant. Your ONLY job is to help
the user understand what is written on their prescription. You are NOT a doctor.

STRICT RULES:
- Never say a medicine treats a specific condition as fact. Say it is "commonly used for"
  and tell the user to confirm with their doctor.
- Never give dosage advice beyond restating what is literally written on the prescription.
- Never say two medicines are "dangerous together" - say they "may interact according to
  medicine information sources" and to consult a pharmacist/doctor.
- If handwriting or text is unclear, say so explicitly instead of guessing.
- Explain medical abbreviations (BD, TDS, SOS, OD, HS, etc.) in plain language.
- Translate instructions into Roman Urdu when asked.

Respond ONLY with valid JSON matching this exact schema, no preamble, no markdown fences:
{
  "medicines": [
    {
      "name": "string",
      "dosage_instruction_raw": "string or null",
      "frequency_explained": "string or null",
      "timing_note": "string or null",
      "form": "string or null",
      "confidence": "clear" or "unclear"
    }
  ],
  "general_notes": "string or null",
  "unclear_sections": ["list of strings describing what couldn't be read"],
  "disclaimer": "This explains what appears to be written on your prescription. It is not medical advice - please confirm with your doctor or pharmacist."
}
"""


class GemmaError(Exception):
    pass


def _extract_json(raw_text: str) -> dict:
    """Gemma sometimes wraps JSON in markdown fences or adds stray text - strip that."""
    cleaned = re.sub(r"^```(json)?|```$", "", raw_text.strip(), flags=re.MULTILINE).strip()
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", cleaned, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(0))
            except json.JSONDecodeError as e:
                raise GemmaError(f"Could not parse Gemma response as JSON: {e}") from e
        raise GemmaError("Gemma response did not contain valid JSON.")


async def analyze_prescription_text(ocr_text: str) -> dict:
    """Send OCR-extracted text to Gemma and get back structured JSON."""
    payload = {
        "model": settings.GEMMA_MODEL_NAME,
        "prompt": f"{SYSTEM_PROMPT}\n\nPrescription text (from OCR):\n{ocr_text}",
        "stream": False,
    }
    return await _call_gemma(payload)


async def analyze_prescription_image(image_path: str) -> dict:
    """Send the raw image directly to a vision-capable Gemma endpoint (skips OCR)."""
    with open(image_path, "rb") as f:
        image_b64 = base64.b64encode(f.read()).decode("utf-8")

    payload = {
        "model": settings.GEMMA_MODEL_NAME,
        "prompt": SYSTEM_PROMPT,
        "images": [image_b64],
        "stream": False,
    }
    return await _call_gemma(payload)


async def _call_gemma(payload: dict) -> dict:
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(settings.GEMMA_API_URL, json=payload)
            response.raise_for_status()
    except httpx.HTTPError as e:
        raise GemmaError(f"Gemma API request failed: {e}") from e

    data = response.json()
    raw_text = data.get("response") or data.get("text") or ""
    if not raw_text:
        raise GemmaError("Gemma returned an empty response.")

    return _extract_json(raw_text)


async def answer_question(prescription_gemma_data: dict, question: str) -> str:
    """Answer a follow-up question against already-extracted structured data
    (e.g. 'Which medicine is taken at night?'). Avoids re-reading the image."""
    payload = {
        "model": settings.GEMMA_MODEL_NAME,
        "prompt": (
            f"{SYSTEM_PROMPT}\n\nHere is the structured prescription data:\n"
            f"{json.dumps(prescription_gemma_data)}\n\n"
            f"Answer this question using ONLY that data, in one or two sentences: {question}"
        ),
        "stream": False,
    }
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(settings.GEMMA_API_URL, json=payload)
            response.raise_for_status()
    except httpx.HTTPError as e:
        raise GemmaError(f"Gemma API request failed: {e}") from e

    data = response.json()
    return data.get("response") or data.get("text") or "I couldn't generate an answer."