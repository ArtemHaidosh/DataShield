# Backend - DataShield API

FastAPI application for document anonymization.

## Requirements

- Python 3.9+
- Virtual environment (venv)

## Setup

### 1. Create Virtual Environment
```bash
python -m venv venv
```

### 2. Activate
**Windows:**
```bash
venv\Scripts\activate
```

**Mac/Linux:**
```bash
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

First run will download SLM models (~320 MB), takes 5-10 minutes.

### 4. Run Server
```bash
python main.py
```

Server runs on http://localhost:8000

## API Endpoints

### GET /
Health check endpoint

### POST /api/anonymize
Upload file and anonymize

**Request:** multipart/form-data
- file: binary file (PDF, DOCX, TXT)

**Response:**
```json
{
  "status": "success",
  "original_text": "...",
  "anonymized_text": "...",
  "summary": "...",
  "statistics": {
    "original_length": 1000,
    "anonymized_length": 950,
    "processing_time_ms": 2500,
    "compression_ratio": 95.0
  }
}
```

## Models

- **FLAN-T5-small** (240 MB) - Anonymization
- **DistilBART-CNN** (80 MB) - Summarization

Auto-downloaded on first run.