# 🏛️ OrientaMX — The Assistant That Doesn’t Make Things Up
> **Reliable citizen-facing legal assistant that answers municipal traffic regulation questions with exact article citations and refuses out-of-domain questions to prevent hallucination.**

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Gradio](https://img.shields.io/badge/Interface-Gradio%204.0-FF6B6B?logo=gradio&logoColor=white)](https://gradio.app/)
[![SentenceTransformers](https://img.shields.io/badge/Embeddings-paraphrase--multilingual--MiniLM-blue)](https://huggingface.co/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2)
[![FAISS](https://img.shields.io/badge/Vector%20Index-FAISS%20IndexFlatIP-brightgreen)](https://github.com/facebookresearch/faiss)
[![License](https://img.shields.io/badge/License-MIT-lightgrey.svg)](LICENSE)

---

## 1. Product Name & Overview
**OrientaMX** is a verifiable, anti-hallucination legal AI assistant designed for citizens of Apodaca, Nuevo León. It answers everyday inquiries regarding local traffic regulations, displays the exact quoted article along with its full official text, and deterministically refuses adversarial or out-of-scope trap questions.

* **Course:** Redes Neuronales y Aprendizaje Profundo / Comunicación Integral en Inglés Técnico I (RNAP Hack 2026)
* **Track:** Track 4 — The Assistant That Doesn’t Make Things Up
* **Team:** `trabajo_goty`
* **Team Members:** Julio Treviño, Ángel Daniel
* **Client / Organization:** Orienta MX

---

## 2. The Problem and Who Has It
Citizens frequently consult generic AI chatbots about municipal traffic rules, driving penalties, and school zone speed limits. Unfortunately, standard large language models regularly **hallucinate**: they invent nonexistent articles, fabricate fines, and present false regulatory claims with total confidence. In a recent real-world scenario, a citizen paid an illegitimate fine after a generic chatbot asserted it was mandatory.

OrientaMX solves this crisis of trust by establishing a **Zero-Tolerance Hallucination Gate**:
* Every answer must be directly supported by an official municipal article.
* If a question falls outside the regulatory corpus (trap question or irrelevant inquiry), the system **strictly refuses** to speculate.

---

## 3. How the Product Works
OrientaMX uses a two-tier **Retrieval-Augmented Generation (RAG)** pipeline designed for legal precision:

```
                  ┌────────────────────────────────────────┐
                  │          Citizen Query in Spanish      │
                  └───────────────────┬────────────────────┘
                                      │
                                      ▼
                  ┌────────────────────────────────────────┐
                  │    paraphrase-multilingual-MiniLM      │
                  │        384-d Dense Embedding           │
                  └───────────────────┬────────────────────┘
                                      │
                                      ▼
                  ┌────────────────────────────────────────┐
                  │       FAISS Inner-Product Index        │
                  │   Cosine Similarity Scoring (Top-3)    │
                  └───────────────────┬────────────────────┘
                                      │
               ┌──────────────────────┴──────────────────────┐
               │                                             │
      Score >= tau (0.50)                            Score < tau (0.50)
               │                                             │
               ▼                                             ▼
┌──────────────────────────────┐              ┌──────────────────────────────┐
│  Grounding & Article Quote   │              │   Deterministic Abstention   │
│ - Exact Article Cited        │              │ - Anti-Hallucination Rejection│
│ - Full Verbatim Text Shown   │              │ - Out-of-Domain Alert        │
│ - Factually Bound Answer     │              │ - Refuses to Invent Rules    │
└──────────────────────────────┘              └──────────────────────────────┘
```

1. **Document Segmentation:** The official *Reglamento de Tránsito y Vialidad de Apodaca, N.L.* is parsed into canonical articles using regular expressions and PyMuPDF.
2. **Dense Semantic Retrieval:** Queries and legal articles are mapped to continuous 384-dimensional vector spaces via `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`.
3. **Calibrated Refusal Gate ($\tau = 0.50$):** Inner-product similarity between query and articles is evaluated against a strictly calibrated threshold $\tau$. If $\max_i \text{sim}(q, d_i) < \tau$, the system immediately halts and emits a safe abstention notice.
4. **Context-Restricted Synthesis:** Legitimate queries are answered strictly based on the retrieved article text, with zero ungrounded generation.

---

## 4. Quantitative Results & Evaluation Metrics

We evaluated three consecutive systems on our labeled benchmark of 80 queries (45 legitimate questions and 35 adversarial traps):

| Metric / Dimension | Baseline (TF-IDF + Cosine) | Pretrained (MiniLM + FAISS) | Transformer RAG Pipeline |
| :--- | :---: | :---: | :---: |
| **Top-3 Retrieval Accuracy** | 77.8% | 100.0% | **100.0%** |
| **Trap Rejection Rate (Anti-Hallucination)** | 100.0% | 100.0% | **100.0%** |
| **Factual Faithfulness (Groundedness)** | 66.7% | 88.9% | **100.0%** |
| **Mean Inference Latency** | 1.2 ms | 18.5 ms | **42.0 ms** |
| **Resistance to Paraphrasing / Synonyms** | Poor | High | **Superior** |

### Evaluation Visualizations
* **Comparative Metrics:** `eval_metrics_comparison.png`
* **Threshold Calibration Trade-off Curve:** `eval_threshold_curve.png`
* **Computational Latency Profile:** `eval_latency_profile.png`
* **Cross-Attention Mechanism Heatmap:** `attention_mechanism_diagram.png`

---

## 5. What We Have Learned and Next Steps
* **Threshold Calibration is Vital:** An uncalibrated retriever either answers traps falsely or refuses valid questions. Setting $\tau = 0.50$ on validation data achieved the optimal balance (100% Top-3 accuracy, 100% trap rejection).
* **Attention Restricts Drift:** Cross-attention matrices between user query tokens and regulation tokens keep the model grounded, proving that attention can be leveraged as an audit tool for legal explainability.
* **Next Steps:**
  * Deploy permanently to Hugging Face Spaces with automated continuous integration.
  * Integrate an OCR pipeline for legacy scanned government bulletins.
  * Expand multi-article fusion for complex compound infractions.

---

## 6. How to Run the Prototype Interface (Gradio v1)

### Option A: Local Execution
```bash
git clone https://github.com/Angel0ADAD/trabajo_goty.git
cd trabajo_goty
pip install -r requirements.txt
python app.py
```
Then navigate to `http://127.0.0.1:7860` in your web browser.

### Option B: Google Colab with Public URL
Open `notebooks/entrenamiento.ipynb` in Google Colab and run the final cell to launch Gradio with `share=True`.
