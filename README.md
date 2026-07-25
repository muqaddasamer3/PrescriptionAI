# PrescriptionAI

### AI-Powered Prescription Understanding Assistant

PrescriptionAI helps patients understand their handwritten or printed prescriptions using OCR and Gemma 4 — safely, clearly, and without replacing the role of a doctor or pharmacist.

---

## The Problem

Handwritten prescriptions are often difficult to read, even for pharmacists. Patients frequently misunderstand medicine names, dosages, timing, and medical abbreviations (BD, TDS, SOS, OD, HS), which can lead to medication errors.

## Our Solution

PrescriptionAI takes a photo of a prescription and returns a clear, structured explanation:

- Medicine names and dosages
- Plain-English explanations of medical abbreviations
- Roman Urdu translation of instructions
- A simple medication schedule
- Clear flags on any text that couldn't be read confidently
- A chat feature to ask follow-up questions about the prescription

**Important:** This tool does not diagnose conditions, prescribe medicines, or recommend dosage changes. It only explains what is already written on the prescription, and always advises verifying with a doctor or pharmacist.

---

## Architecture
User uploads prescription image
│
▼
OCR (EasyOCR) — extracts raw text
│
▼
Text Cleaning
│
▼
Gemma 4 (gemma-4-26b-a4b-it via Google AI Studio API)
│
├── Medicine names & dosages
├── Abbreviation explanations
├── Roman Urdu translation
├── Medication schedule
├── Unclear/unreadable sections
└── Chat Q&A
│
▼
FastAPI Backend
│
▼
PostgreSQL Database
│
▼
React Frontend

---

## Tech Stack

| Layer | Technology |
|---|---|
| AI Model | Gemma 4 (`gemma-4-26b-a4b-it`) via Google AI Studio API |
| OCR | EasyOCR |
| Backend | FastAPI |
| Database | PostgreSQL (Supabase) |
| Frontend | React |

---

## Project Structure
PrescriptionAI/
├── ai_engine/ # OCR + Gemma integration (AI pipeline)
│ ├── ocr/ # Text extraction from images
│ ├── gemma/ # Prompt engineering + Gemma API client
│ ├── utils/
│ ├── tests/
│ └── README.md # AI module setup & usage docs
├── backend/ # FastAPI application (routers, services, models)
├── frontend/ # React application
├── requirements.txt
└── README.md

---

## Getting Started

### Requirements
- Python 3.11
- PostgreSQL (Supabase)
- Node.js (for frontend)

### Backend Setup
pip install -r requirements.txt
Create a `.env` file:
DATABASE_URL=...
GOOGLE_API_KEY=...

alembic upgrade head
Seed data:
python scripts/seed.py

### AI Engine Setup

See [`ai_engine/README.md`](ai_engine/README.md) for detailed setup and usage instructions for the OCR + Gemma module.

### Frontend Setup
cd frontend
npm install
npm start

---

## Team

| Member | Role |
|---|---|
| Muqaddas Amer | AI, OCR & Gemma Integration |
| Arslan | Backend & API Integration |
| Mueeza | Frontend / UI |
| Musab | Database |

---

## Built For

Built with Gemma 4 — GDG Cloud Lahore Hackathon.
