import json
import re
import os
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class RAGEngine:
    def __init__(self, base_dir=None):
        if base_dir is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        self.faqs_path = os.path.join(base_dir, "knowledge_base", "faqs.json")
        self.tickets_path = os.path.join(base_dir, "knowledge_base", "support_tickets.json")
        
        self.documents = []
        self.vectorizer = None
        self.tfidf_matrix = None
        
        self._load_and_index_documents()

    def pii_scrub(self, text: str) -> str:
        """PII Redaction pass using regex for emails, phone numbers, and user names."""
        # Scrub emails
        text = re.sub(r'[\w\.-]+@[\w\.-]+\.\w+', '[REDACTED_EMAIL]', text)
        # Scrub phone numbers
        text = re.sub(r'\+?\d{1,4}?[-.\s]?\(?\d{1,3}?\)?[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,9}', '[REDACTED_PHONE]', text)
        # Scrub account IDs
        text = re.sub(r'acc_\w+', '[REDACTED_ACC_ID]', text)
        return text

    def _load_and_index_documents(self):
        """Extract, scrub PII, chunk, and index FAQ & support ticket data."""
        self.documents = []

        # 1. Load FAQs
        if os.path.exists(self.faqs_path):
            with open(self.faqs_path, "r", encoding="utf-8") as f:
                faqs = json.load(f)
                for item in faqs:
                    clean_content = self.pii_scrub(item["content"])
                    self.documents.append({
                        "id": item["id"],
                        "source_type": "faq",
                        "title": item["title"],
                        "product_area": item["product_area"],
                        "text": f"{item['title']} - {clean_content}",
                        "raw_content": clean_content
                    })

        # 2. Load Support Tickets
        if os.path.exists(self.tickets_path):
            with open(self.tickets_path, "r", encoding="utf-8") as f:
                tickets = json.load(f)
                for item in tickets:
                    clean_q = self.pii_scrub(item["question"])
                    clean_r = self.pii_scrub(item["resolution"])
                    chunk_text = f"Customer Question: {clean_q} | Resolution: {clean_r}"
                    self.documents.append({
                        "id": item["id"],
                        "source_type": "ticket",
                        "title": clean_q,
                        "product_area": item["product_area"],
                        "text": chunk_text,
                        "raw_content": clean_r
                    })

        # 3. Compute TF-IDF Indexing
        if self.documents:
            corpus = [doc["text"] for doc in self.documents]
            self.vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
            self.tfidf_matrix = self.vectorizer.fit_transform(corpus)

    def query(self, user_question: str, product_area_filter: str = None, top_k: int = 3, confidence_threshold: float = 0.12):
        """
        Retrieval & Generation Flow:
        1. Query vector similarity search.
        2. Re-rank top-k by score & source priority (FAQ > ticket on tie).
        3. Confidence threshold check.
        4. Grounded answer generation.
        """
        if not self.vectorizer or self.tfidf_matrix is None or len(self.documents) == 0:
            return {
                "answer": "Knowledge base unavailable. Would you like me to open a support ticket for our team?",
                "confidence": 0.0,
                "sources": []
            }

        # Vector Similarity
        query_vec = self.vectorizer.transform([user_question])
        scores = cosine_similarity(query_vec, self.tfidf_matrix).flatten()

        # Product Area infering / filtering
        candidate_indices = list(range(len(self.documents)))
        if product_area_filter:
            candidate_indices = [
                idx for idx in candidate_indices 
                if self.documents[idx]["product_area"] == product_area_filter
            ]

        if not candidate_indices:
            candidate_indices = list(range(len(self.documents)))

        # Score & Rank
        ranked = sorted(
            [(idx, scores[idx]) for idx in candidate_indices],
            key=lambda x: (x[1], 1 if self.documents[x[0]]["source_type"] == "faq" else 0),
            reverse=True
        )

        top_results = ranked[:top_k]
        best_score = top_results[0][1] if top_results else 0.0

        # Confidence Guardrail Check
        if best_score < confidence_threshold:
            return {
                "answer": "I'm not completely sure based on our verified help articles. Would you like me to open a support ticket for our team?",
                "confidence": float(best_score),
                "sources": [],
                "low_confidence": True
            }

        # Context assembly & Grounded Response synthesis
        retrieved_chunks = []
        for idx, score in top_results:
            if score > 0.05:
                doc = self.documents[idx]
                retrieved_chunks.append(doc)

        if not retrieved_chunks:
            return {
                "answer": "I'm not sure based on our product guide. Want me to open a support ticket for you?",
                "confidence": 0.0,
                "sources": [],
                "low_confidence": True
            }

        # Grounded system synthesis (concise, click-path based, < 80 words)
        primary_doc = retrieved_chunks[0]
        answer_text = primary_doc["raw_content"]
        
        # Enforce < 80 words constraint
        words = answer_text.split()
        if len(words) > 80:
            answer_text = " ".join(words[:80]) + "..."

        return {
            "answer": answer_text,
            "confidence": float(best_score),
            "sources": [doc["title"] for doc in retrieved_chunks],
            "low_confidence": False
        }
