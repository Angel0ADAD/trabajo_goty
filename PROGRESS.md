# Bitácora de Progreso del Proyecto (PROGRESS.md)
## Redes Neuronales y Aprendizaje Profundo · RNAP Hack 2026
### Track 4: "The Assistant That Doesn’t Make Things Up" (Orienta MX)

**Equipo de Desarrollo:**
* Julio Treviño T.
* Enrique Martínez R.
* Enrique Colis
* Ángel Argüelles

---

## Checkpoint 1 (CP1) — Definición del Reto y Partición de Datos
* **Fecha:** Jueves 5 de noviembre de 2026
* **Objetivo:** Definición del problema normativo, selección de métricas clave y curaduría del conjunto de datos.

### Actividades Desarrolladas:
1. **Definición del Reto:** Se eligió el **Track 4**, enfocado en la prevención de alucinaciones en consultas jurídicas y viales de la empresa ficticia **Orienta MX**.
2. **Adquisición del Corpus:** Se seleccionó el *Reglamento de Tránsito y Vialidad de Apodaca, Nuevo León*, segmentando sus primeros 20 artículos canónicos mediante expresiones regulares y PyMuPDF.
3. **Construcción del Dataset Sintético:** Se elaboró una batería balanceada de **80 consultas**:
   - **45 preguntas legítimas** con artículo objetivo explícito (*Answer Key*).
   - **35 preguntas trampa** (materias estatales, trámites foráneos, impuestos prediales) cuya etiqueta esperada es `RECHAZAR`.
4. **Partición Formal de Datos:**
   - **Entrenamiento (Train):** 60% (48 preguntas: 27 reales, 21 trampas).
   - **Validación (Val):** 20% (16 preguntas: 9 reales, 7 trampas), reservado para calibración de umbrales.
   - **Prueba (Test):** 20% (16 preguntas: 9 reales, 7 trampas), aislado para evaluación final.
5. **Métricas Principales Seleccionadas:**
   - **Top-3 Retrieval Accuracy (%):** Porcentaje de preguntas reales donde el artículo correcto se ubica entre los tres primeros candidatos.
   - **Trap Rejection Rate (%):** Porcentaje de preguntas trampa donde el sistema se abstiene de responder.

---

## Checkpoint 2 (CP2) — Dimensión 3: Línea Base y Preentrenado sin Ajuste
* **Fecha:** Jueves 5 de noviembre de 2026
* **Objetivo:** Implementación del modelo clásico desde cero y comparación con modelo denso sin ajuste sobre el Test Set.

### Actividades Desarrolladas:
1. **Modelo Base desde Cero (TF-IDF + Coseno):**
   - Vectorizador TF-IDF con $n$-gramas $(1, 2)$ y matriz dispersa.
   - Regla de rechazo basada en umbral de similitud coseno ($\tau_{\text{tfidf}} = 0.15$).
2. **Modelo Preentrenado sin Ajuste (SentenceTransformers + FAISS):**
   - Encoder denso `paraphrase-multilingual-MiniLM-L12-v2` (384 dimensiones).
   - Indexación vectorial plana de alta velocidad con FAISS `IndexFlatIP`.
   - Umbral de rechazo por producto interno calibrado ($\tau_{\text{dense}} = 0.50$).
3. **Tabla Comparativa de Desempeño en Test Set:**

| Modelo Evaluado | Top-3 Accuracy | Trap Rejection Rate | Latencia Media |
| :--- | :---: | :---: | :---: |
| **Línea Base (TF-IDF + Coseno)** | 77.8% | 100.0% | **1.2 ms** |
| **Preentrenado (MiniLM-L12 + FAISS)** | **100.0%** | **100.0%** | 18.5 ms |

* **Conclusión:** Aunque TF-IDF es ultra rápido, fracasa ante sinónimos y lenguaje coloquial (ej. *"tomado"* vs. *"ebriedad"*). El modelo denso preentrenado logra 100% de recuperación semántica en el conjunto de prueba.

---

## Checkpoint 3 (CP3) — Solución Transformer RAG y Análisis de Errores
* **Fecha:** Jueves 12 de noviembre de 2026
* **Objetivo:** Construcción de la arquitectura RAG completa con citación estricta y auditoría profunda de casos de fallo.

### Actividades Desarrolladas:
1. **Arquitectura RAG Integral:**
   - Integración de la compuerta de verificación de umbral ($\tau = 0.50$) con generación condicionada (*Grounded Generation*).
   - El sistema tiene prohibido responder sin adjuntar el texto oficial del artículo recuperado.
   - Fidelidad fáctica (*Groundedness*) evaluada: **100.0%**.
2. **Análisis de 5 Casos de Error y Desafío:**
   - *Caso 1 (Solapamiento Léxico Engañoso):* Multas UMA en predial. TF-IDF alucinó sanción vial; Transformer RAG rechazó correctamente.
   - *Caso 2 (Ambigüedad Interjurisdiccional):* Verificación vehicular ambiental estatal. Transformer se abstuvo con 0.38 < 0.50.
   - *Caso 3 (Sinonimia Coloquial Extrema):* *"Manejar tomado"*. TF-IDF falló por ausencia de la palabra; Transformer recuperó Artículo 10 (cero tolerancia).
   - *Caso 4 (Trámite Administrativo Ajeno):* Pasaporte mexicano en tránsito. Rechazado limpiamente.
   - *Caso 5 (Complejidad de Subreglas):* Horarios de zonas escolares (Art. 8). Top-1 exacto.

---

## Checkpoint 4 (CP4) — Prototipo Interactivo Gradio v1
* **Fecha:** Jueves 12 de noviembre de 2026
* **Objetivo:** Desarrollo de la interfaz gráfica web v1 conectada al modelo para pruebas en vivo.

### Actividades Desarrolladas:
1. **Construcción de la Interfaz:** Implementación de la interfaz en Gradio v1 (en `notebooks/entrenamiento.ipynb` y script `app.py`).
2. **Funcionalidades de la Interfaz:**
   - Entrada de texto libre para preguntas del usuario/juez.
   - Columna dual: dictamen fundamentado + texto íntegro del artículo citado.
   - Acordeón desplegable con el desglose del Top-3 de candidatos vectoriales en FAISS.
   - Batería de botones con pruebas rápidas legítimas y preguntas trampa para la evaluación.
3. **Verificación de Estabilidad:** La interfaz responde en menos de 50 ms por consulta y no sufre caídas de memoria.

---

## Versión 1.0 (v1.0) — Producto Final (PIA Fase 3)
* **Fecha:** Martes 17 de noviembre de 2026 (Preparación para Evaluación del Jueves 19)
* **Objetivo:** Congelamiento de código, desacoplamiento a aplicación autónoma y preparación para la defensa con el juez.

### Actividades Desarrolladas:
1. **Desacoplamiento a Aplicación Autónoma:** Creación de `app.py` y `requirements.txt` en la raíz del repositorio para ejecución local en cualquier laptop sin necesidad de Google Colab.
2. **Mecanismo de Contingencia Resiliente:** Se integró un modo de fallback automático en `app.py` para asegurar que la demo funcione ininterrumpidamente bajo cualquier contingencia en la laptop del equipo.
3. **Documentación Técnica Completa:** Redacción de `README.md` con explicación matemática del mecanismo de atención multicabezal ($\text{Attention}(Q, K, V) = \text{softmax}(QK^T/\sqrt{d_k})V$) y lecciones aprendidas.
4. **Guía de Defensa para el Juez:** Elaboración de `GUIA_DEFENSA_JUEZ.md` con respuestas preparadas a preguntas sorpresa sobre matrices Q, K, V y calibración de umbrales.
5. **Estado del Repositorio:** Versión v1.0 lista y validada localmente en `goty_repo`.
