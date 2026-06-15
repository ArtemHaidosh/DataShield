# 🛡️ DataShield - Document Anonymizer with NER & SLM

Remove personal information from documents using Named Entity Recognition (NER) and Small Language Models (DistilBART for summarization).

## Features

- 📄 Support for PDF, DOCX, TXT files
- 🔒 100% local processing (no cloud APIs)
- ⚡ Fast inference on CPU (~30-40 sec per document)
- 📊 Document summarization included
- 🎯 Replaces PII with tokens: [NAME], [EMAIL], [PHONE], [CITY], [COMPANY]
- 🤖 Uses BERT-based NER for entity detection
- 📝 Regex patterns for email, phone, and bank account numbers

## Technology Stack

- **Backend:** FastAPI, Python 3.9+
- **Frontend:** Vue 3, Vite, Tailwind CSS
- **NER Model:** BERT-large-cased (dbmdz/bert-large-cased-finetuned-conll03-english)
- **Summarization:** DistilBART-CNN
- **Document Parsing:** PyPDF2, python-docx
- **Entity Recognition:** Transformers library

## Architecture

### Anonymization Pipeline

1. **File Processing:** Extract text from PDF/DOCX/TXT
2. **Regex Patterns:** Replace emails, phones, bank accounts
3. **NER Model:** Find and classify entities (names, organizations, locations)
4. **Entity Replacement:** Replace detected entities with tokens
5. **Summarization:** Generate summary of anonymized text

### Models

- **BERT-NER** (768 MB)
  - Detects: Person (PER), Organization (ORG), Location (LOC)
  - Fine-tuned on CONLL03 dataset
  - ~95% accuracy on named entity detection

- **DistilBART-CNN** (80 MB)
  - Generates abstractive summaries
  - Works on anonymized text

## Quick Start

### Backend

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate

pip install -r requirements.txt
python main.py
```

Server runs on `http://localhost:8000`

### Frontend

```bash
cd frontend
npm install
npm run dev
```

App opens on `http://localhost:5173`

## API Endpoints

### POST /api/anonymize

Upload document and anonymize

**Request:**
Content-Type: multipart/form-data

file: binary file (PDF, DOCX, TXT)

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

## Project Structure
DataShield/

├── backend/

│   ├── main.py                 # FastAPI application

│   ├── slm_processor.py        # NER + regex anonymization

│   ├── file_processor.py       # PDF/DOCX/TXT parsing

│   ├── requirements.txt        # Python dependencies

│   ├── .env                    # Environment config

│   ├── .gitignore

│   └── README.md

├── frontend/

│   ├── index.html              # HTML structure

│   ├── app.js                  # Vue 3 component

│   ├── vite.config.js          # Vite configuration

│   ├── package.json            # Node dependencies

│   ├── .gitignore

│   └── README.md

├── .gitignore

└── README.md

## How It Works

### NER-Based Anonymization

Instead of instruction-following models (which don't work well for this task), DataShield uses:

1. **Named Entity Recognition (NER):** 
   - BERT model identifies names, organizations, locations in text
   - Outputs: entity type + position in text

2. **Regex Patterns:**
   - Emails: `user@example.com` → `[EMAIL]`
   - Phones: `+1-555-1234` → `[PHONE]`
   - Bank accounts: `1234567890` → `[ACCOUNT_NUMBER]`

3. **Entity Replacement:**
   - Replace found entities with standardized tokens
   - Preserve document structure and meaning

## Security

✅ 100% local processing (no cloud)  
✅ No external API calls  
✅ No data logging or persistence  
✅ GDPR/HIPAA compatible  

## License

MIT

## Author

Built as a diploma project for demonstrating:
- NLP & SLM understanding
- Named Entity Recognition implementation
- Full-stack web application development
- Document processing pipelines