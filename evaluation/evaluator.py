import sys
import os

# Add project root to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import pickle
from embeddings.embedder import Embedder
from rag.retriever import retrieve
from rag.generator import generate_answer
from evaluation.test_questions import TEST_CASES


def evaluate():

    with open("vector_store.pkl", "rb") as f:
        vector_store = pickle.load(f)

    embedder = Embedder()

    correct = 0
    total = len(TEST_CASES)

    for case in TEST_CASES:

        question = case["question"]
        expected = case["expected"]

        chunks = retrieve(question, embedder, vector_store)
        answer = generate_answer(chunks, question)

        if expected.lower() in answer.lower():
            correct += 1
            status = "✅"
        else:
            status = "❌"

        print(f"{status} Q: {question}")
        print(f"   Expected contains: {expected}")
        print(f"   Got: {answer}")
        print("-" * 60)

    print(f"\nFinal Accuracy: {correct}/{total} = {round((correct/total)*100,2)}%")


if __name__ == "__main__":
    evaluate()