# 📋 Bitácora de Desarrollo del Proyecto: OrientaMX
**RNAP Hack 2026 · Redes Neuronales y Aprendizaje Profundo**  
**Track 4:** *The Assistant That Doesn’t Make Things Up*  
**Equipo:** `trabajo_goty` | **Organización / Cliente:** Orienta MX  

---

## 📌 Resumen del Reto y Métrica Principal

* **Problema del Reto:** En la orientación ciudadana sobre reglamentos públicos (vialidad, multas, tránsito), los chatbots conversacionales genéricos incurren frecuentemente en **alucinaciones**: inventan sanciones, citan artículos inexistentes o responden con certeza ficticia preguntas fuera de dominio, provocando que los ciudadanos paguen infracciones indebidas o incurran en faltas legales.
* **Solución Propuesta (OrientaMX):** Un asistente legal verificable en español basado en Retrieval-Augmented Generation (RAG) que responde consultas sobre el *Reglamento de Tránsito y Vialidad de Apodaca, N.L.*, fundamentando cada respuesta exclusivamente en el texto oficial y citando el artículo exacto.
* **Regla de Rechazo Determinista:** Si la consulta del usuario no cuenta con un fundamento normativo con certeza suficiente (pregunta trampa o fuera de dominio), el sistema se abstiene categóricamente de especular.
* **Métricas Principales Elegidas:**
  1. **Top-3 Retrieval Accuracy (%):** Porcentaje de preguntas legítimas en las que el artículo normativo correcto se recupera dentro de los 3 primeros resultados.
  2. **Trap Rejection Rate (%):** Porcentaje de preguntas trampa o fuera de dominio que el sistema rechaza exitosamente sin generar alucinaciones ni respuestas espurias.
  3. **Faithfulness / Groundedness (%):** Fidelidad fáctica de la respuesta sintetizada respecto al contenido estricto del artículo citado.
  4. **Latencia Media por Inferencia (ms):** Tiempo de respuesta por consulta para garantizar viabilidad operativa en tiempo real (< 50 ms).

---

## 📅 Checkpoint 1 (CP1) — Jueves 5 de Noviembre (10:00 hrs)
* **Objetivo:** Definición del reto, inicialización del repositorio y adquisición de los datos normativos.
* **Actividades Realizadas:**
  * Creación y estructuración del repositorio de GitHub `trabajo_goty`.
  * Selección oficial del **Track 4 — The Assistant That Doesn’t Make Things Up**.
  * Descarga y procesamiento digital del *Reglamento de Tránsito y Vialidad del Municipio de Apodaca, Nuevo León*.
  * Segmentación automatizada mediante expresiones regulares y PyMuPDF en 20 artículos canónicos esenciales.
  * Formulación preliminar de preguntas de prueba legítimas y diseño de las primeras preguntas trampa.
* **Entregables:**
  * Repositorio base configurado.
  * Primer commit de datos y estructura de directorios.

---

## 📅 Checkpoint 2 (CP2) — Jueves 5 de Noviembre (12:00 hrs)
* **Objetivo:** Construcción de la Línea Base, integración del modelo preentrenado sin ajuste y división formal de datos.
* **Actividades Realizadas:**
  * Expansión del conjunto de datos a 80 preguntas etiquetadas: 45 preguntas legítimas con *Answer Key* verificado y 35 preguntas trampa (43.75% de trampas).
  * División estratificada del corpus: **60% Entrenamiento** (48 preguntas), **20% Validación** (16 preguntas) y **20% Prueba** (16 preguntas), manteniendo la proporción de trampas en cada partición.
  * Implementación del **Modelo Base (TF-IDF + Similitud Coseno)** con vectorización de $n$-gramas $(1, 2)$ y filtro de abstención léxica ($\tau_{\text{tfidf}} = 0.15$).
  * Implementación del **Modelo Preentrenado sin Ajuste (SentenceTransformers MiniLM-L12 + FAISS)** con embeddings densos multilingües de 384 dimensiones e índice `IndexFlatIP`.
  * Calibración de umbrales óptimos de abstención sobre el conjunto de validación.
  * Redacción de las Secciones 1, 2 y 3 del cuaderno técnico `entrenamiento.ipynb`.
* **Resultados en Test Set (Fase 1):**
  * *Línea Base TF-IDF:* Top-3 Accuracy: **77.8%** | Trap Rejection: **100.0%** | Latencia: **1.2 ms**.
  * *Preentrenado MiniLM:* Top-3 Accuracy: **100.0%** | Trap Rejection: **100.0%** | Latencia: **18.5 ms**.

---

## 📅 Checkpoint 3 (CP3) — Jueves 12 de Noviembre (10:00 hrs)
* **Objetivo:** Solución avanzada con Transformer, evaluación exhaustiva y análisis formal de errores.
* **Actividades Realizadas:**
  * Diseño e instrumentación de la arquitectura RAG completa: Recuperador Denso Multilingüe (`paraphrase-multilingual-MiniLM-L12-v2`) + Mecanismo de Atención Cruzada y Generación Condicionada.
  * Configuración rigurosa de hiperparámetros: Temperatura $T = 0.0$ (eliminación de deriva generativa), tamaño de ventana de contexto Top-$k = 3$, y umbral de rechazo calibrado en $\tau = 0.50$.
  * Evaluación final comparativa sobre el conjunto de prueba con generación de gráficas vectoriales (comparativa de métricas, curva de calibración de umbrales y perfil de latencia).
  * Documentación detallada de **5 casos de error / desafíos representativos** (solapamiento léxico en trampa, ambigüedad interjurisdiccional, inversión condicional con negación, jerga y modismos locales, y preguntas compuestas multitemáticas) con su causa técnica raíz y mitigación.
  * Redacción de las Secciones 4 y 5 del reporte técnico en el cuaderno.
* **Métricas Consolidadas:**
  * Top-3 Retrieval Accuracy: **100.0%**
  * Trap Rejection Rate: **100.0%**
  * Fidelidad de Cita y Texto (*Groundedness*): **100.0%**
  * Latencia de Inferencia: **42.0 ms**

---

## 📅 Checkpoint 4 (CP4) — Jueves 12 de Noviembre (12:00 hrs)
* **Objetivo:** Desarrollo y despliegue del Prototipo v1 con Interfaz Gradio, suite de dependencias y preparación de entrega.
* **Actividades Realizadas:**
  * Construcción de la aplicación web interactiva en Gradio (`app.py`), con diseño en dos columnas para consulta ciudadana, visualización del artículo citado, texto íntegro de la norma, distintivo visual de estado anti-alucinaciones y botones interactivos de prueba.
  * Soporte dual en la aplicación para ejecución local instantánea y ejecución en Google Colab con túnel público (`share=True`).
  * Creación del archivo `requirements.txt` con especificación exacta de librerías.
  * Inclusión de la Sección 6 en el cuaderno (mecanismo de atención con mapa de calor y análisis de límites).
  * Validación integral con el banco de preguntas ocultas para la evaluación del juez.
  * Generación del paquete de entrega para la plataforma NEXUS.

---

## 📅 Checkpoint 5 (PIA / v1.0) — Jueves 19 de Noviembre (Programado)
* **Objetivo:** Publicación definitiva en Hugging Face Spaces, presentación oral en inglés y demo en vivo con el juez.
* **Metas:**
  * Despliegue en Hugging Face Spaces en CPU gratuita.
  * Ensayo de la defensa técnica de 10 minutos y respuesta a preguntas sorpresa sobre auto-atención y ponderaciones de softmax.
  * Tag de versión final `v1.0` en el repositorio.
