import sys
import os
import fitz

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import pickle
import json

from embeddings.embedder import Embedder
from rag.retriever import retrieve
from rag.generator import generate_answer

def render_page(page_number):

    doc = fitz.open("data/swiggy_annual_report.pdf")

    page = doc.load_page(page_number - 1)

    pix = page.get_pixmap()

    return pix.tobytes("png")

# -------------------------
# Session State
# -------------------------
if "history" not in st.session_state:
    st.session_state.history = []


st.set_page_config(
    page_title="Swiggy Annual Report RAG",
    layout="wide"
)

st.title("Swiggy Annual Report FY 2023–24 QA System")
st.markdown("Hybrid Structured + RAG Financial Intelligence Engine")


# -------------------------
# Sidebar: Query History
# -------------------------
with st.sidebar:
    st.header("🕓 Query History")

    for q in reversed(st.session_state.history[-10:]):
        st.write("•", q)


# -------------------------
# Load Resources
# -------------------------
@st.cache_resource
def load_system():

    with open("vector_store.pkl", "rb") as f:
        vector_store = pickle.load(f)

    with open("financial_data.json", "r") as f:
        financial_data = json.load(f)

    embedder = Embedder()

    return vector_store, embedder, financial_data



vector_store, embedder, financial_data = load_system()

# -------------------------
# Financial Dashboard
# -------------------------

st.header("📊 Financial Summary Dashboard")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Standalone Net Loss FY24",
        financial_data["standalone"]["net_loss_after_tax"]["FY24"]
    )

with col2:
    st.metric(
        "Standalone Total Income FY24",
        financial_data["standalone"]["total_income"]["FY24"]
    )

with col3:
    st.metric(
        "Standalone EPS FY24",
        financial_data["standalone"]["earnings_per_share"]["FY24"]
    )
# -------------------------
# User Input
# -------------------------
query = st.text_input("Ask a question about the Swiggy Annual Report:")

if query:

    st.session_state.history.append(query)

    with st.spinner("Analyzing document..."):
        chunks = retrieve(query, embedder, vector_store)
        answer, source_type = generate_answer(chunks, query)

    # -------------------------
    # Final Answer
    # -------------------------

    st.subheader("Final Answer")
    st.success(answer)

    # -------------------------
    # Downloadable Report
    # -------------------------

    supporting_pages = []

    if chunks:
        supporting_pages = [c["metadata"]["page_number"] for c in chunks]

    report = f"""
Swiggy Annual Report QA Result
--------------------------------

Question:
{query}

Answer:
{answer}

Answer Type:
{source_type}

Supporting Pages:
{supporting_pages}
"""

    st.download_button(
        label="📑 Download Answer Report",
        data=report,
        file_name="swiggy_qa_report.txt",
        mime="text/plain"
    )

    # -------------------------
    # Answer Source Badge
    # -------------------------

    if source_type == "structured":
        st.success("🟢 Structured Financial Answer")

    elif source_type == "llm":
        st.info("🤖 LLM Generated Answer")

    else:
        st.warning("⚠️ Information Not Found In Document")

    # -------------------------
    # Retrieval Confidence
    # -------------------------

    if chunks:

        avg_score = sum([c["score"] for c in chunks]) / len(chunks)

        st.subheader("Retrieval Confidence")
        st.progress(min(avg_score, 1.0))
        st.caption(f"Average Similarity Score: {round(avg_score,3)}")

    else:
        st.warning("No relevant chunks retrieved.")

    # -------------------------
    # Supporting Context
    # -------------------------

    if chunks:

        st.subheader("Supporting Context")

        for i, c in enumerate(chunks):

            page_number = c["metadata"]["page_number"]

            with st.expander(
                f"Page {page_number} | Score: {round(c['score'],3)}"
            ):

                st.write(c["text"])

                if st.button(f"Preview Page {page_number}", key=f"preview_{page_number}_{i}"):

                    image = render_page(page_number)

                    st.image(image, caption=f"Page {page_number}")