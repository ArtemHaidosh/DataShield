from PyPDF2 import PdfReader
from docx import Document
from io import BytesIO


class FileProcessor:
    """File processor for PDF, DOCX, TXT files"""

    SUPPORTED_FORMATS = ['.pdf', '.docx', '.txt']

    def extract_text(self, file_content: bytes, filename: str) -> str:
        """
        Extracts text from uploaded file
        """
        filename_lower = filename.lower()

        print(f"[FileProcessor] Processing {filename}...")

        if filename_lower.endswith('.pdf'):
            text = self._extract_pdf(file_content)
        elif filename_lower.endswith('.docx'):
            text = self._extract_docx(file_content)
        elif filename_lower.endswith('.txt'):
            text = self._extract_txt(file_content)
        else:
            raise ValueError(f"Unsupported format: {filename}")

        print(f"[FileProcessor] ✓ Extracted {len(text)} characters")
        return text

    def _extract_pdf(self, content: bytes) -> str:
        """Extract text from PDF"""
        try:
            pdf = PdfReader(BytesIO(content))
            text = ""

            for page_num, page in enumerate(pdf.pages):
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"

            if not text.strip():
                raise ValueError("No text extracted from PDF")

            return text
        except Exception as e:
            raise Exception(f"PDF extraction error: {str(e)}")

    def _extract_docx(self, content: bytes) -> str:
        """Extract text from DOCX"""
        try:
            doc = Document(BytesIO(content))
            text = ""

            for paragraph in doc.paragraphs:
                if paragraph.text.strip():
                    text += paragraph.text + "\n"

            if not text.strip():
                raise ValueError("No text extracted from DOCX")

            return text
        except Exception as e:
            raise Exception(f"DOCX extraction error: {str(e)}")

    def _extract_txt(self, content: bytes) -> str:
        """Extract text from TXT"""
        try:
            text = content.decode('utf-8', errors='ignore')

            if not text.strip():
                raise ValueError("TXT file is empty")

            return text
        except Exception as e:
            raise Exception(f"TXT extraction error: {str(e)}")