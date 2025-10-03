"""
Ingestion script: Load and update knowledge base (KB)
"""

import json
import os

KB_PATH = "knowledge_base.json"

DEFAULT_KB = [
    {
        "question": "What should we know about your life story in a few sentences?",
        "answer": "I'm Aditi Sharma, a Full-Stack engineer passionate about AI and building developer tools that empower people."
    },
    {
        "question": "What's your #1 superpower?",
        "answer": "Turning ambiguous problems into small, testable experiments and shipping fast."
    },
    {
        "question": "What are the top 3 areas you'd like to grow in?",
        "answer": "Model fine-tuning, production ML infra, and leadership communication."
    },
    {
        "question": "What misconception do your coworkers have about you?",
        "answer": "That I'm always confident. In reality, I iterate a lot and rely on feedback."
    },
    {
        "question": "How do you push your boundaries and limits?",
        "answer": "I deliberately take on projects outside my comfort zone and seek feedback."
    }
]

def load_kb():
    if not os.path.exists(KB_PATH):
        with open(KB_PATH, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_KB, f, indent=2)
    with open(KB_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_kb(kb):
    with open(KB_PATH, "w", encoding="utf-8") as f:
        json.dump(kb, f, indent=2)
