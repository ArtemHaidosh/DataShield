# Backend - DataShield API

FastAPI application for document anonymization using NER and regex patterns.

## Architecture

### Anonymization Pipeline

1. **File Extraction** (`FileProcessor`)
   - PDF: PyPDF2
   - DOCX: python-docx
   - TXT: plain text

2. **PII Detection** (`SLMProcessor`)
   - Regex: Emails, phones, account numbers
   - NER: Names, organizations, locations
   - BERT-large-cased model for entity classification

3. **Summarization**
   - DistilBART for abstractive summarization

## Requirements

- Python 3.9+
- Virtual environment (venv)
- 8GB RAM minimum

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

First run downloads models (~850 MB). Takes 5-10 minutes.

### 4. Run Server
```bash
python main.py
```

Server runs on http://localhost:8000

## API Endpoints

### GET /
Health check

### POST /api/anonymize
Upload and anonymize document

**Request:** `multipart/form-data`
- `file`: PDF, DOCX, or TXT file

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
    "processing_time_ms": 35000,
    "compression_ratio": 95.0
  }
}
```

## Models

### BERT-Large-Cased (NER)
- **Size:** 768 MB
- **Task:** Named Entity Recognition
- **Training Data:** CONLL03 dataset
- **Entities Detected:** PER, ORG, LOC
- **Accuracy:** ~95%

### DistilBART-CNN
- **Size:** 80 MB
- **Task:** Abstractive summarization
- **Input:** Anonymized text
- **Output:** Document summary

### Code Style
- Python 3.9+
- Type hints recommended
- Docstrings for all functions