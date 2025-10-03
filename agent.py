"""
Agent logic: retrieval + LLaMA-based prompt application
"""

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

from ingestion import load_kb
from prompt import apply_prompt  # updated to use LLaMA

# Load KB
kb = load_kb()

# Load embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Precompute embeddings
def compute_embeddings(kb_items):
    texts = [entry['question'] + " [SEP] " + entry['answer'] for entry in kb_items]
    return model.encode(texts, convert_to_numpy=True)

kb_embeddings = compute_embeddings(kb)

def normalize_query(query: str) -> str:
    q = query.lower()
    if any(word in q for word in ["best thing", "strength", "unique", "quality", "standout"]):
        return "What's your #1 superpower?"
    if "background" in q or "story" in q or "journey" in q:
        return "What should we know about your life story in a few sentences?"
    return query

def retrieve(query, top_k=1):
    q_emb = model.encode([query], convert_to_numpy=True)
    sims = cosine_similarity(q_emb, kb_embeddings)[0]
    idx_sorted = np.argsort(-sims)
    results = []
    for idx in idx_sorted[:top_k]:
        results.append({
            'question': kb[idx]['question'],
            'answer': kb[idx]['answer'],
            'score': float(sims[idx])
        })
    return results

def agent_response(query):
    """
    Generate a response using NVIDIA LLaMA-3.3 Nemotron Super 49B v1.5.
    """
    normalized = normalize_query(query)
    retrieved = retrieve(normalized, top_k=1)
    if not retrieved:
        return "I'm not sure about that, but I’d love to focus on my professional journey."

    answer = retrieved[0]['answer']
    # Pass the LLaMA model instance to apply_prompt for rephrasing
    return apply_prompt(query, answer)
