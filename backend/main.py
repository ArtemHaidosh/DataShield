from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
import time
from dotenv import load_dotenv
from slm_processor import SLMProcessor
from file_processor import FileProcessor

load_dotenv()

app = FastAPI(
    title="DataShield API",
    description="Document anonymization using SLM",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize processors
print("\n[APP] Initializing SLMProcessor...")
slm_processor = SLMProcessor()
file_processor = FileProcessor()
print("[APP] ✓ All processors ready!\n")


@app.get("/")
def read_root():
    """Health check endpoint"""
    return {
        "status": "DataShield API running",
        "version": "1.0.0"
    }


@app.get("/health")
def health():
    """Health check"""
    return {"status": "healthy"}


@app.post("/api/anonymize")
async def anonymize(file: UploadFile = File(...)):
    """
    Main endpoint for document anonymization
    """
    try:
        print(f"\n[API] New request: {file.filename}")
        start_time = time.time()

        # Read file
        content = await file.read()
        print(f"[API] File size: {len(content)} bytes")

        # Extract text
        text = file_processor.extract_text(content, file.filename)

        # Anonymize
        anonymized_text = slm_processor.anonymize(text)

        # Summarize
        summary = slm_processor.summarize(anonymized_text)

        # Calculate time
        processing_time = time.time() - start_time

        print(f"[API] ✓ Success! Processing time: {processing_time:.2f}s\n")

        return {
            "status": "success",
            "original_text": text[:300],
            "anonymized_text": anonymized_text,
            "summary": summary,
            "statistics": {
                "original_length": len(text),
                "anonymized_length": len(anonymized_text),
                "processing_time_ms": int(processing_time * 1000),
                "compression_ratio": round((len(anonymized_text) / len(text)) * 100, 2)
            }
        }
    except Exception as e:
        print(f"[API] ✗ Error: {str(e)}\n")
        raise HTTPException(status_code=400, detail=str(e))


if __name__ == "__main__":
    port = int(os.getenv("BACKEND_PORT", 8000))
    print(f"\n🚀 Starting DataShield API on port {port}\n")
    uvicorn.run(app, host="0.0.0.0", port=port)