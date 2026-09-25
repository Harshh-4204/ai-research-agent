import ollama
import re


def decide_action(question):

    q = question.lower().strip()

    # Obvious calculation questions
    calculation_patterns = [
        r"\bwhat is .*%\s*of\b",
        r"\bcalculate\b",
        r"\bcompute\b",
        r"\bsolve\b",
    ]

    for pattern in calculation_patterns:
        if re.search(pattern, q):
            return "CALCULATE"

    # Obvious web-search questions
    search_words = [
        "latest",
        "current",
        "today",
        "recent",
        "news",
        "this week",
        "this month",
        "current price",
    ]

    if any(word in q for word in search_words):
        return "SEARCH"

    # Let the LLM decide ambiguous questions
    prompt = f"""
Choose ONE action for this question:

SEARCH = requires current/external information
ANSWER = can be answered from general knowledge

Question:
{question}

Reply with ONLY SEARCH or ANSWER.
"""

    response = ollama.chat(
        model="qwen3:8b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        think=False,
        options={
            "temperature": 0,
            "num_predict": 5
        }
    )

    decision = response["message"]["content"].strip().upper()

    if "SEARCH" in decision:
        return "SEARCH"

    return "ANSWER"