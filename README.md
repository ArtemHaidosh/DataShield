# 🛡️ DataShield - Document Anonymizer with SLM

Remove personal information from documents using Small Language Models (FLAN-T5 + DistilBART).

## Features

- 📄 Support for PDF, DOCX, TXT files
- 🔒 100% local processing (no cloud)
- ⚡ Fast inference on CPU
- 📊 Document summarization included
- 🎯 Replaces PII with tokens: [NAME], [EMAIL], [PHONE], [CITY], [COMPANY]

## Quick Start

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

Server runs on http://localhost:8000

### Frontend
```bash
cd frontend
npm install
npm run dev
```

App opens on http://localhost:5173

## Project Structure

DataShield/
├── backend/
│   ├── main.py
│   ├── slm_processor.py
│   ├── file_processor.py
│   ├── requirements.txt
│   └── .env
├── frontend/
│   ├── index.html
│   ├── app.js
│   ├── vite.config.js
│   └── package.json
└── README.md

## Technology Stack

- **Backend:** FastAPI, Python 3.9+
- **Frontend:** Vue 3, Vite, Tailwind CSS
- **SLM Models:** FLAN-T5-small, DistilBART
- **Document Parsing:** PyPDF2, python-docx

## Status

Development in progress - Day 1/5
