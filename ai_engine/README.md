# AI Engine - OCR + Gemma Module

Extracts text from prescription images and uses Gemma AI to generate structured medical information.

## What It Does

This module takes a prescription image and returns:
- Medicine names, dosage, frequency
- Abbreviation meanings (BD, TDS, etc.)
- Roman Urdu translation
- Medication schedule
- Unclear/unreadable sections
- Confidence note

## For Backend: How To Use

from ai_engine.pipeline import process_prescription
result = process_prescription(image_path)

The result is a Python dict with the following structure:

{
  medicines: [ { name, dosage, frequency, abbreviation_meaning } ],
  roman_urdu_translation: string,
  medication_schedule: [ { medicine, time, instructions } ],
  unclear_sections: [string],
  confidence_note: string,
  raw_ocr_text: string
}

If an error occurs (e.g. no text could be extracted), it returns:

{ error: 'error message here' }

## Setup (For Local Testing)

1. Create a virtual environment: python -m venv venv
2. Activate it: .\venv\Scripts\Activate
3. Install dependencies: pip install -r ai_engine/requirements.txt
4. Create a .env file in the root folder and add: GOOGLE_API_KEY=your_key_here

## Folder Structure

- ocr/ - Extracts text from images (EasyOCR)
- gemma/ - Handles Gemma AI communication and prompt engineering
- utils/ - Helper functions
- pipeline.py - Main function that connects everything together

## Model Used

Gemma 4 (gemma-4-26b-a4b-it) via Google AI Studio API
