# 🛡️ Anti-Hallucination Multi-Agent Coding System

A high-fidelity Multi-Agent system built with **AutoGen v0.4** and **Streamlit**. This project implements a **Generator-Discriminator** pattern to eliminate LLM hallucinations during code generation by grounding agents in a local source of truth.

## 🚀 The Architecture
This is a **Multi-Agent RAG (Retrieval-Augmented Generation)** system. 
- **Coder Agent:** Proposes modifications to the codebase.
- **Judge Agent (LLM-as-a-Judge):** Cross-references proposals against the physical `target_code.py` file.
- **Orchestration:** Round-Robin logic ensures no code is output without a mandatory audit turn.

## 🛠️ Tech Stack
- **Framework:** AutoGen v0.4 (Async API)
- **Model:** Llama-3.1-8b-instant (via Groq)
- **UI:** Streamlit
- **Observability:** LangSmith (for trace analysis)

## 📖 How to Run
1. Clone the repo.
2. Add your `GROQ_API_KEY` to `train.py`.
3. Run `streamlit run app.py`.
