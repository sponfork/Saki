#Saki

An AI-powered draft recommendation system for Mobile Legends: Bang Bang (MLBB). This assistant leverages scraped hero statistics and a Retrieval-Augmented Generation (RAG) architecture with Gemini to recommend strategic counter-picks and team compositions in real time.

---

##  Project Overview

Developing high-tier draft strategies requires analyzing win rates, pick/ban dynamics, and hero counters. This project automates data collection from competitive statistics endpoints, indexes structured telemetry, and injects context into a LLM to deliver real-time drafting advice.

### System Architecture
1. **Data Ingestion**: Scrape dynamic stats from web sources using Playwright.
2. **Data Pipeline**: Clean, normalize, and parse raw DOM/JSON payloads into structured JSON datasets.
3. **Retrieval Engine (RAG)**: Query clean local hero statistics to construct contextual prompts.
4. **Inference & Recommendation**: Supply formatted queries to Gemini via Google AI Studio API for real-time draft suggestions.

---

## Tech Stack & Environment

* **Language**: Python 3.14+
* **Scraping & Automation**: Playwright
* **LLM Engine**: Google GenAI SDK
* **Environment**: Python `venv`
