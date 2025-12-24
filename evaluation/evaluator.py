# evaluation/evaluator.py

import json
import time
import requests

API_URL = "http://127.0.0.1:8000/query"

def run_evaluation():
    with open("evaluation/eval_questions.json") as f:
        eval_data = json.load(f)

    results = []

    for item in eval_data:
        question = item["question"]
        expected = item["expected_keywords"]

        start = time.time()
        response = requests.post(
            API_URL,
            params={"question": question}
        )
        latency = time.time() - start

        answer = response.json().get("answer", "").lower()

        keyword_hits = sum(1 for k in expected if k in answer)

        results.append({
            "question": question,
            "latency_sec": round(latency, 2),
            "keyword_score": f"{keyword_hits}/{len(expected)}"
        })

    return results


if __name__ == "__main__":
    output = run_evaluation()
    for r in output:
        print(r)
