# AI Research Agent

An agentic AI research assistant built with Python, Streamlit, and a local Qwen3 8B language model. The agent can answer questions, search the web, perform calculations, and answer questions from uploaded PDF documents using retrieval-augmented generation (RAG).

## Features

- 🤖 Agentic question routing
- 🔎 Web search for current information
- 🧮 Mathematical calculation tool
- 📄 PDF document upload and text extraction
- 📚 Retrieval-augmented generation (RAG) for PDF questions
- 🧠 Local Qwen3 8B language model
- 🖥️ Streamlit web interface

## Tech Stack

- **Python**
- **Streamlit** — web interface
- **Ollama + Qwen3 8B** — local language model
- **DDGS** — web search
- **PyPDF** — PDF text extraction
- **Git & GitHub** — version control

## How It Works

```text
User Question
      ↓
Agent Router
      ↓
 ┌────┼───────────┐
 ↓    ↓           ↓
Answer Search  Calculate
 ↓    ↓           ↓
Qwen  Web       Result
      Search

PDF Upload
      ↓
Text Extraction
      ↓
Text Chunking
      ↓
Keyword Retrieval
      ↓
Relevant Chunks
      ↓
Qwen3 8B
      ↓
PDF-based Answer

## How to Run

### 1. Clone the repository

```bash
git clone https://github.com/Harshh-4204/ai-research-agent.git
cd ai-research-agent

python -m venv venv

venv\Scripts\activate

pip install streamlit ollama ddgs pypdf

ollama pull qwen3:8b

streamlit run app.py

## Usage

### General Questions
Enter a question such as:

> What is Python?

The agent can answer directly using the local Qwen3 model.

### Web Search
Ask a question requiring current information:

> What are the latest developments in AI?

The agent routes the question to the web search tool.

### Calculations
Ask a mathematical question:

> What is 17% of 84500?

The agent routes the question to the calculator.

### PDF RAG
Upload a PDF and ask a question about its contents:

> What department was mentioned in the project report?

The system extracts the PDF text, retrieves relevant sections, and uses Qwen3 to generate an answer based on those sections.

## Future Improvements
- Replace keyword-based retrieval with semantic embeddings and vector search
- Add support for multiple PDF documents
- Add conversation history and memory
- Improve agent tool selection
- Add source citations for web research results
- Deploy the application for public access