# Saki: Mobile Legends: Bang Bang (MLBB) AI Draft Coach

Saki is an intelligent, dual-model draft strategy coach designed for Mobile Legends: Bang Bang (MLBB). It transitions from a standard LLM prototype into a robust, real-time drafting interface that combines official match data with a custom-tuned coaching persona.

---

## Dual-Model Architecture

Saki utilizes a powerful **dual-model pipeline** to ensure tactical accuracy, zero data hallucination, and an authentic coaching persona:

1. **The 27B RAG Retriever & Analyzer**: 
   * **Model**: Powered by high-parameter reasoning models (e.g., `qwen/qwen3.8-27b`).
   * **Role**: Acts as the first-stage intelligence. It scans the structured hero database (`mlbb_heroes_clean.json`), extracts specific counter matchup scores, and synthesizes raw game statistics based on the user's draft query.
2. **The Fine-Tuned 7B Persona (Saki)**: 
   * **Model**: Fine-tuned using LoRA/QLoRA on `unsloth/Qwen2.5-7B-Instruct-bnb-4bit` (Saved adapter: `checkpoint-60`).
   * **Role**: Acts as the second-stage persona generator. It takes the grounded statistical context passed down from the RAG layer and delivers sharp, professional draft analysis in Saki's signature coaching tone.


