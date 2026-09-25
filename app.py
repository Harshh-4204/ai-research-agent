import streamlit as st
import ollama
from ddgs import DDGS
from agent import decide_action
from pypdf import PdfReader
import re

st.title("🤖 AI Research Agent")
st.caption("Ask questions, search the web, calculate results, or query your PDF documents.")
st.markdown(
    """
    This AI agent uses a local LLM to decide whether a question
    should be answered directly, searched on the web, calculated,
    or answered using information from an uploaded PDF.
    """
)
question = st.text_input("What would you like me to research?")
uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])
def chunk_text(text, chunk_size=1000):
    chunks = []

    for i in range(0, len(text), chunk_size):
        chunk = text[i:i + chunk_size]
        chunks.append(chunk)

    return chunks
def retrieve_chunks(question, chunks, top_k=3):
    question_words = set(re.findall(r"\b\w+\b", question.lower()))

    scored_chunks = []

    for chunk in chunks:
        chunk_words = set(re.findall(r"\b\w+\b", chunk.lower()))
        score = len(question_words & chunk_words)
        scored_chunks.append((score, chunk))

    scored_chunks.sort(reverse=True, key=lambda x: x[0])

    return [chunk for score, chunk in scored_chunks[:top_k]]
def answer_from_pdf(question, retrieved_chunks):
    context = "\n\n".join(retrieved_chunks)

    prompt = f"""
You are answering a question about a PDF.

Use ONLY the information in the provided PDF excerpts.
If the answer cannot be found in the excerpts, say:
"I couldn't find the answer in the provided PDF."

PDF excerpts:
{context}

Question:
{question}

Give a clear and concise answer.
"""

    response = ollama.chat(
        model="qwen3:8b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        think=False
    )

    return response["message"]["content"]
if uploaded_file:
    reader = PdfReader(uploaded_file)
    pdf_text = ""

    for page in reader.pages:
        pdf_text += page.extract_text() + "\n"

    st.success("PDF loaded successfully!")
    chunks = chunk_text(pdf_text)
    
def web_search(query):
    results = DDGS().text(query, max_results=5)

    text = ""

    for result in results:
        text += f"Title: {result['title']}\n"
        text += f"URL: {result['href']}\n"
        text += f"Summary: {result['body']}\n\n"

    return text


def calculate(question):
    prompt = f"""
Calculate the answer to this mathematical question.

Question:
{question}

Return only the final numerical answer.
"""

    response = ollama.chat(
        model="qwen3:8b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        think=False
    )

    return response["message"]["content"]


if st.button("Research"):
    
    if question:

        with st.spinner("Agent is thinking..."):

            # If a PDF is uploaded, answer using the PDF
            if uploaded_file:

                st.info("📄 Agent is using the uploaded PDF.")

                retrieved = retrieve_chunks(question, chunks)

                answer = answer_from_pdf(
                    question,
                    retrieved
                )

            else:

                action = decide_action(question)

                st.write(f"**Agent decision:** `{action}`")

                if action == "SEARCH":

                    st.info("🔎 Agent decided to search the web.")

                    search_results = web_search(question)

                    prompt = f"""
You are an AI research assistant.

User question:
{question}

Web search results:
{search_results}

Give a clear answer based on the search results.
Mention useful sources.
"""

                    response = ollama.chat(
                        model="qwen3:8b",
                        messages=[
                            {
                                "role": "user",
                                "content": prompt
                            }
                        ],
                        think=False
                    )

                    answer = response["message"]["content"]

                elif action == "CALCULATE":

                    st.info("🧮 Agent decided to calculate.")

                    answer = calculate(question)

                else:

                    st.info("🧠 Agent decided web search was not necessary.")

                    response = ollama.chat(
                        model="qwen3:8b",
                        messages=[
                            {
                                "role": "user",
                                "content": question
                            }
                        ],
                        think=False
                    )

                    answer = response["message"]["content"]

        st.subheader("Result")
        st.write(answer)

    else:
        st.warning("Please enter a question.")