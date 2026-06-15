from transformers import pipeline
import re


class SLMProcessor:
    """
    SLM Processor using NER (Named Entity Recognition) for anonymization
    and DistilBART for summarization
    """

    def __init__(self):
        print("[SLMProcessor] Loading NER model for anonymization...")
        self.ner = pipeline(
            "ner",
            model="dbmdz/bert-large-cased-finetuned-conll03-english",
            device=-1,
            aggregation_strategy="simple"
        )

        print("[SLMProcessor] Loading DistilBART for summarization...")
        self.summarizer = pipeline(
            "summarization",
            model="sshleifer/distilbart-cnn-6-6",
            device=-1
        )
        print("[SLMProcessor] ✓ All models loaded successfully!")

    def anonymize(self, text: str) -> str:
        """
        Anonymizes text using NER model + Regex
        1. Replace emails/phones with regex first
        2. Then use NER for names/cities/companies
        """
        if not text or len(text) < 50:
            return text
        
        try:
            print(f"[Anonymizer] Processing {len(text)} characters...")
            
            # STEP 1: Regex replacements (email, phone) - FIRST!
            # Emails
            text = re.sub(
                r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
                '[EMAIL]',
                text
            )
            
            # Phone numbers
            text = re.sub(
                r'\+?\d{1,3}[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b',
                '[PHONE]',
                text
            )
            
            print(f"[Anonymizer] After regex: {text[:100]}...")
            
            # STEP 2: NER for entities (PER, ORG, LOC)
            entities = self.ner(text)
            
            if entities:
                print(f"[Anonymizer] Found {len(entities)} NER entities")
                
                # Sort by START position DESCENDING to avoid index shifting
                entities_sorted = sorted(entities, key=lambda x: x['start'], reverse=True)
                
                # Replace each entity
                for entity in entities_sorted:
                    start = entity['start']
                    end = entity['end']
                    label = entity['entity_group']
                    
                    # Skip if entity contains our replacement tokens
                    entity_text = text[start:end]
                    if entity_text.startswith('[') and entity_text.endswith(']'):
                        continue
                    
                    # Map NER labels
                    replacement = {
                        'PER': '[NAME]',
                        'ORG': '[COMPANY]',
                        'LOC': '[CITY]'
                    }.get(label, f'[{label}]')
                    
                    text = text[:start] + replacement + text[end:]
                    print(f"  Replaced '{entity_text}' → {replacement}")
            
            print(f"[Anonymizer] ✓ Done!")
            return text
            
        except Exception as e:
            print(f"[Anonymizer] ✗ Error: {e}")
            import traceback
            traceback.print_exc()
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