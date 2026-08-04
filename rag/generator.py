import json
import re
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from utils.logger import logger

# -------------------------
# Load Structured Financial Data
# -------------------------

with open("financial_data.json", "r") as f:
    FINANCIALS = json.load(f)

# -------------------------
# Load Local LLM
# -------------------------

MODEL_NAME = "google/flan-t5-base"

print("Loading local LLM...")

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)

# -------------------------
# Prompt Template
# -------------------------

PROMPT_TEMPLATE = """
Answer the question strictly using the context below.
If the answer is not explicitly mentioned in the context, say:
"The information is not available in the Swiggy Annual Report."

Context:
{context}

Question:
{question}

Answer:
"""

# -------------------------
# Helper Functions
# -------------------------

def get_financial_year(question):
    q = question.lower()
    
    # Use regex for robust year extraction
    if re.search(r"fy\s*24|2024", q):
        return "FY24"
        
    if re.search(r"fy\s*23|2023", q):
        return "FY23"
        
    return None


def get_scope(question):

    q = question.lower()

    if "consolidated" in q:
        return "consolidated"

    return "standalone"


# -------------------------
# Main Answer Generator
# -------------------------
def context_relevant(question, context_chunks):
    q_words = set(question.lower().split())
    # Remove common stop words
    stop_words = {"what", "is", "the", "in", "of", "and", "a", "an", "for", "on", "was", "were", "to", "how", "many", "who"}
    q_words = q_words - stop_words
    
    if not q_words:
        return True # If question is only stop words, let it pass to LLM
        
    context_text = " ".join([c["text"].lower() for c in context_chunks])
    overlap = sum(1 for w in q_words if w in context_text)
    
    return overlap >= 1 # At least one meaningful word matches

def generate_answer(context_chunks, question):

    if not context_chunks:
        return "The information is not available in the Swiggy Annual Report.", "not_found"
    # Validate context relevance
    if not context_relevant(question, context_chunks):
        return "The information is not available in the Swiggy Annual Report.", "not_found"

    q = question.lower()
    year = get_financial_year(question)
    scope = get_scope(question)

    # -------------------------
    # Structured Financial Handling
    # -------------------------

    if year is None:

        if "fy25" in q:
            return "The information is not available in the Swiggy Annual Report.", "not_found"

        if any(word in q for word in ["net loss", "total income", "total expenses", "earnings per share"]):
            return "Please specify the financial year (FY23 or FY24).", "structured"

    if year and scope in FINANCIALS:

        data = FINANCIALS[scope]

        if "net loss" in q:
            value = data.get("net_loss_after_tax", {}).get(year)
            if value: return f"The {scope} net loss after tax in {year} was ({value}).", "structured"

        if "total income" in q:
            value = data.get("total_income", {}).get(year)
            if value: return f"The {scope} total income in {year} was {value}.", "structured"

        if "total expenses" in q:
            value = data.get("total_expenses", {}).get(year)
            if value: return f"The {scope} total expenses including depreciation in {year} were {value}.", "structured"

        if "earnings per share" in q:
            value = data.get("earnings_per_share", {}).get(year)
            if value: return f"The {scope} earnings per share in {year} were ({value}).", "structured"

    # -------------------------
    # Fallback to LLM
    # -------------------------

    # Take at most top 2 chunks to avoid context truncation for flan-t5-base
    context_chunks = context_chunks[:2]
    context = "\n\n".join(
        [f"(Page {c['metadata']['page_number']}) {c['text']}" for c in context_chunks]
    )

    prompt = PROMPT_TEMPLATE.format(
        context=context,
        question=question
    )

    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        truncation=True,
        max_length=1024
    )

    outputs = model.generate(
        **inputs,
        max_new_tokens=150
    )

    answer = tokenizer.decode(outputs[0], skip_special_tokens=True)

    logger.info(f"QUERY: {question} | ANSWER: {answer}")

    return answer, "llm"