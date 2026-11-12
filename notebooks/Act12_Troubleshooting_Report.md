# Engineering Audit & Troubleshooting Report
**Course:** Comunicación Integral en Inglés Técnico I / RNAP Hack 2026  
**Activity:** Evidencia de Aprendizaje · Act. 12 — Troubleshooting Report  
**Date:** November 12, 2026  
**Team:** trabajo_goty  
**Track:** Track 4 — The Assistant That Doesn’t Make Things Up  
**Authors:** Julio Treviño, Ángel Daniel  
**Organization / Fictional Client:** Orienta MX  

---

## 1. Audit Status
Our engineering team has already deployed the Phase 2 prototype of the OrientaMX legal assistant on GitHub and Gradio. Since the beginning of the hackathon, we have evaluated three consecutive architectures on our labeled benchmark of 80 municipal transit queries. The baseline model has reached a Top-3 retrieval accuracy of 77.8%, while our Transformer RAG pipeline has achieved a 100% accuracy on legitimate questions. Furthermore, our calibrated rejection threshold has successfully blocked 100% of adversarial trap queries for two consecutive evaluation cycles. However, our system has not yet handled extreme Monterrey colloquial slang with complete semantic stability, and we have not incorporated optical character recognition for scanned municipal gazettes yet.

### Current Performance Metrics (Test Set Evaluation)

| Architecture / Model | Top-3 Accuracy (%) | Trap Rejection Rate (%) | Groundedness (%) | Mean Latency (ms) |
| :--- | :---: | :---: | :---: | :---: |
| **Baseline (TF-IDF + Cosine)** | 77.8% | 100.0% | 66.7% | 1.2 ms |
| **Pretrained (MiniLM-L12 + FAISS)** | 100.0% | 100.0% | 88.9% | 18.5 ms |
| **Transformer RAG Pipeline** | **100.0%** | **100.0%** | **100.0%** | **42.0 ms** |

---

## 2. Immediate Solutions
If we integrated a specialized Spanish cross-encoder re-ranker before the generation stage, the confidence scores on borderline queries would increase significantly. If our team expanded the prompt template with three explicit few-shot regional examples, the assistant would interpret colloquial Mexican phrasing much more effectively without altering the official legal terminology. Additionally, if we converted our vector index to an optimized quantized structure, the end-to-end inference latency would drop below 20 milliseconds on standard CPU hardware.

---

## 3. Root Cause Analysis
If we had implemented strict lexical lemmatization during the initial baseline phase, the TF-IDF model would not have failed on plural noun variations such as *camellones* versus *camellón*. Moreover, if we had established a higher similarity threshold during our first validation experiment, the system would not have retrieved misleading articles for ungrounded parking meter inquiries. Finally, if our team had preserved full chapter headers alongside individual article bodies, the encoder would have disambiguated school zone restrictions from general residential speed limits even faster.
