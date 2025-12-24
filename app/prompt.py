# app/prompt.py

def build_prompt(context: str, question: str) -> str:
    return f"""
You are a strict document question-answering system.

RULES:
- You MUST answer using ONLY the context below.
- If the answer is NOT explicitly stated in the context,
  reply with EXACTLY this sentence and nothing else:
  Not found in provided documents.

- DO NOT guess.
- DO NOT infer.
- DO NOT add explanations.

Context:
{context}

Question:
{question}

Answer:
""".strip()
