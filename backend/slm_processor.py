from transformers import pipeline


class SLMProcessor:

    # Small Language Model Processor for anonymization and summarization
    # Uses FLAN-T5 for anonymization and DistilBART for summarization


    def __init__(self):
        print("[SLMProcessor] Loading FLAN-T5 for anonymization...")
        self.anonymizer = pipeline(
            "text2text-generation",
            model="google/flan-t5-small",
            device=-1  # -1 = CPU, 0 = GPU if available
        )

        print("[SLMProcessor] Loading DistilBART for summarization...")
        self.summarizer = pipeline(
            "summarization",
            model="sshleifer/distilbart-cnn-6-6",
            device=-1
        )
        print("[SLMProcessor] ✓ All models loaded successfully!")

    def anonymize(self, text: str) -> str:

        # use FLAN-T5
        # replaces: names → [NAME], emails → [EMAIL], phones → [PHONE], cities → [CITY], companies → [COMPANY]

        if not text or len(text) < 50:
            return text

        text_truncated = text[:2000]

        prompt = f"""Remove all personal information from this text.
                Replace names with [NAME], emails with [EMAIL], 
                phone numbers with [PHONE], cities with [CITY],
                company names with [COMPANY].
                Keep the meaning of the text.
                
                Text: {text_truncated}"""

        try:
            print(f"[Anonymizer] Processing {len(text)} characters...")
            result = self.anonymizer(
                prompt,
                max_length=1024,
                num_beams=2
            )
            anonymized = result[0]['generated_text']
            print(f"[Anonymizer] ✓ Done!")
            return anonymized
        except Exception as e:
            print(f"[Anonymizer] ✗ Error: {e}")
            return text

    def summarize(self, text: str) -> str:
        """
        Summarizes text using DistilBART
        """
        if not text or len(text) < 100:
            return "Text too short for summary"

        text_truncated = text[:1024]

        try:
            print(f"[Summarizer] Processing {len(text)} characters...")
            result = self.summarizer(
                text_truncated,
                max_length=150,
                min_length=50,
                do_sample=False
            )
            summary = result[0]['summary_text']
            print(f"[Summarizer] ✓ Done!")
            return summary
        except Exception as e:
            print(f"[Summarizer] ✗ Error: {e}")
            return text[:100] + "..."