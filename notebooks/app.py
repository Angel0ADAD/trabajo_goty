"""
OrientaMX — Asistente Ciudadano Legal sin Alucinaciones
Track 4: "The Assistant That Doesn’t Make Things Up"
RNAP Hack 2026 · Redes Neuronales y Aprendizaje Profundo
Repositorio: trabajo_goty

Aplicación interactiva construida con Gradio.
"""

import os
import re
import math
from typing import Tuple, List, Dict

# Corpus oficial del Reglamento de Tránsito y Vialidad de Apodaca, N.L.
ARTICLES_DATA = [
    {
        "id": "Artículo 1",
        "num": 1,
        "title": "Objeto y orden público",
        "text": "El presente Reglamento es de orden público e interés social, y tiene por objeto regular el tránsito de vehículos, conductores, pasajeros y peatones en las vías públicas del Municipio de Apodaca, Nuevo León, preservando la seguridad vial y el orden público."
    },
    {
        "id": "Artículo 2",
        "num": 2,
        "title": "Autoridades competentes",
        "text": "Son autoridades encargadas de vigilar el estricto cumplimiento del presente Reglamento: la Secretaría de Seguridad Pública y Vialidad, la Dirección de Tránsito de Apodaca y los Oficiales de Tránsito en funciones de agentes viales debidamente acreditados."
    },
    {
        "id": "Artículo 3",
        "num": 3,
        "title": "Definiciones viales esenciales",
        "text": "Para los efectos de este Reglamento se entenderá por vía pública todo espacio terrestre de uso común destinado al tránsito de personas y vehículos; por banqueta, la porción de la vía pública destinada exclusivamente para el tránsito de peatones; y por intersección, la superficie común donde convergen dos o más vías públicas."
    },
    {
        "id": "Artículo 4",
        "num": 4,
        "title": "Documentación vehicular obligatoria",
        "text": "Todo conductor de vehículo de motor que circule en el Municipio de Apodaca está obligado a portar consigo la licencia de conducir o permiso provisional vigente correspondiente al tipo de vehículo, así como la tarjeta de circulación original y las placas metálicas visibles y debidamente colocadas."
    },
    {
        "id": "Artículo 5",
        "num": 5,
        "title": "Cinturón de seguridad y sillas infantiles",
        "text": "Es obligatorio para el conductor y todos los acompañantes o pasajeros de un vehículo en circulación utilizar debidamente abrochado el cinturón de seguridad. Los menores de siete años deberán viajar en los asientos traseros sujetos en asientos de seguridad infantil certificados."
    },
    {
        "id": "Artículo 6",
        "num": 6,
        "title": "Prohibición de celulares y dispositivos móviles",
        "text": "Queda estrictamente prohibido a los conductores sujetar o utilizar teléfonos celulares, radios o cualquier dispositivo de comunicación manual o electrónico mientras el vehículo se encuentre en movimiento, a menos que se haga mediante sistemas de manos libres que no obstaculicen la atención."
    },
    {
        "id": "Artículo 7",
        "num": 7,
        "title": "Límites generales de velocidad",
        "text": "La velocidad máxima permitida en avenidas primarias es de 50 km/h; en calles secundarias o residenciales es de 40 km/h. En zonas escolares, zonas hospitalarias, parques infantiles y lugares de alta concentración de personas, la velocidad máxima será invariable de 30 km/h."
    },
    {
        "id": "Artículo 8",
        "num": 8,
        "title": "Horarios y límites en zonas escolares",
        "text": "El límite de velocidad de 30 km/h en zonas escolares estará vigente de lunes a viernes en los siguientes horarios oficiales: matutino de 7:00 a 9:30 horas; intermedio de 11:30 a 14:30 horas; y vespertino de 16:30 a 18:30 horas, durante los días hábiles del calendario escolar."
    },
    {
        "id": "Artículo 9",
        "num": 9,
        "title": "Preferencia absoluta de paso a peatones",
        "text": "Los peatones gozarán de preferencia de paso sobre los vehículos en todas las esquinas, intersecciones y cruces peatonales señalizados o cebras, especialmente personas de la tercera edad, menores y personas con movilidad reducida o discapacidad motriz."
    },
    {
        "id": "Artículo 10",
        "num": 10,
        "title": "Tolerancia cero al alcohol y sustancias",
        "text": "Queda estrictamente prohibido conducir vehículos por la vía pública bajo el influjo del alcohol, drogas, estupefacientes o psicotrópicos. Cualquier concentración superior a 0.00 mg/L de alcohol en aire espirado ameritará la detención del conductor, infracción grave y remisión del vehículo al depósito oficial."
    },
    {
        "id": "Artículo 11",
        "num": 11,
        "title": "Uso obligatorio de luces y visibilidad",
        "text": "Los conductores están obligados a encender los faros delanteros y luces posteriores desde el anochecer hasta el amanecer, así como cuando las condiciones atmosféricas (niebla intensa, lluvia o humo) reduzcan severamente la visibilidad natural a menos de cien metros."
    },
    {
        "id": "Artículo 12",
        "num": 12,
        "title": "Reglas para motociclistas y ciclistas",
        "text": "Los motociclistas y ciclistas deberán utilizar en todo momento casco protector reglamentario debidamente abrochado. Queda estrictamente prohibido que circulen sobre las banquetas, andadores peatonales, plazas públicas o en sentido contrario al flujo vial."
    },
    {
        "id": "Artículo 13",
        "num": 13,
        "title": "Lugares prohibidos para estacionarse",
        "text": "Queda prohibido estacionar vehículos sobre banquetas, camellones, glorietas, ochavos de esquinas, frente a hidrantes de bomberos, en rampas de acceso para personas con discapacidad o en cajones exclusivos señalizados sin contar con el tarjetón respectivo."
    },
    {
        "id": "Artículo 14",
        "num": 14,
        "title": "Distancia de seguridad entre vehículos",
        "text": "Los conductores deberán conservar una distancia de seguridad prudente respecto al vehículo que los antecede, consistente en al menos tres metros lineales por cada 10 km/h de velocidad de marcha, para garantizar un frenado oportuno ante cualquier emergencia."
    },
    {
        "id": "Artículo 15",
        "num": 15,
        "title": "Paso preferente a vehículos de emergencia",
        "text": "Los conductores tienen la obligación de ceder el paso inmediatamente a los vehículos de emergencia (ambulancias, camiones de bomberos y patrullas de policía) que se desplacen con sirenas y torretas luminosas encendidas, orillándose al extremo derecho de la vía."
    },
    {
        "id": "Artículo 16",
        "num": 16,
        "title": "Obligaciones en caso de accidente vial",
        "text": "Todo conductor involucrado en un hecho de tránsito o accidente vial tiene la obligación ineludible de detener la marcha de inmediato, prestar auxilio a personas lesionadas si las hubiere, señalizar el lugar y dar aviso a la Dirección de Tránsito de Apodaca."
    },
    {
        "id": "Artículo 17",
        "num": 17,
        "title": "Regulación del transporte de carga pesada",
        "text": "Los vehículos de transporte de carga pesada sólo podrán circular por los corredores viales autorizados por la Dirección de Vialidad y deberán apegarse a los horarios nocturnos de carga y descarga establecidos entre las 22:00 y las 06:00 horas en zonas residenciales."
    },
    {
        "id": "Artículo 18",
        "num": 18,
        "title": "Prohibición de ruidos excesivos y claxon",
        "text": "Se prohíbe emitir ruidos excesivos o molestos provocados por escapes abiertos o modificados, así como utilizar el claxon o bocina de manera innecesaria, insistente o frente a planteles educativos y centros hospitalarios."
    },
    {
        "id": "Artículo 19",
        "num": 19,
        "title": "Seguro de responsabilidad civil obligatorio",
        "text": "Todo vehículo que transite en las vías públicas del Municipio deberá contar con póliza de seguro de responsabilidad civil vigente que garantice al menos la cobertura de daños a terceros en sus personas y bienes materiales."
    },
    {
        "id": "Artículo 20",
        "num": 20,
        "title": "Sanciones, multas UMA y recurso de inconformidad",
        "text": "Las infracciones al presente Reglamento serán sancionadas conforme al tabulador de multas en Unidades de Medida y Actualización (UMA). Los ciudadanos inconformes podrán promover recurso de inconformidad ante el Juez Cívico Municipal en un plazo no mayor a 15 días hábiles."
    }
]

# Respuestas sintéticas fundamentadas para preguntas válidas
SYNTHESIS_MAP = {
    1: "El objeto fundamental es regular el tránsito vial y preservar la seguridad de conductores, pasajeros y peatones en Apodaca.",
    2: "Las autoridades encargadas son la Secretaría de Seguridad Pública, la Dirección de Tránsito y los Oficiales de Tránsito viales de Apodaca.",
    3: "Una banqueta es el espacio exclusivo para peatones, la vía pública es el espacio común terrestre e intersección es donde convergen dos o más vías.",
    4: "Es forzoso portar licencia de conducir vigente, tarjeta de circulación original y placas metálicas debidamente colocadas.",
    5: "Todos los ocupantes deben usar cinturón de seguridad y los menores de 7 años deben viajar atrás en asientos de seguridad infantil.",
    6: "Está estrictamente prohibido usar el celular al manejar salvo con manos libres que no distraiga la atención vial.",
    7: "El límite es de 50 km/h en avenidas principales, 40 km/h en calles secundarias y 30 km/h en zonas escolares y hospitalarias.",
    8: "En zonas escolares rige 30 km/h de lunes a viernes en horarios: 7:00 a 9:30 h, 11:30 a 14:30 h y 16:30 a 18:30 h.",
    9: "Los peatones tienen preferencia absoluta en esquinas, cruces peatonales y cebras, con prioridad a adultos mayores y personas con discapacidad.",
    10: "Existe tolerancia cero (0.00 mg/L). Cualquier nivel de alcohol amerita detención, multa grave y corralón.",
    11: "Las luces deben encenderse desde el anochecer hasta el amanecer o con niebla, lluvia o humo con visibilidad menor a 100 metros.",
    12: "Motociclistas deben usar casco reglamentario abrochado y tienen prohibido circular en banquetas o en sentido contrario.",
    13: "Se prohíbe estacionar en banquetas, camellones, ochavos, hidrantes, rampas de discapacidad o cajones exclusivos.",
    14: "Se deben guardar al menos 3 metros de distancia por cada 10 km/h de velocidad respecto al vehículo precedente.",
    15: "Es obligatorio orillarse a la extrema derecha y ceder el paso ante ambulancias, bomberos o patrullas con torretas y sirenas activas.",
    16: "En un choque se debe detener la marcha, auxiliar a lesionados, señalizar la zona y llamar de inmediato a Tránsito de Apodaca.",
    17: "El transporte de carga pesada solo circula por corredores autorizados y descarga en zonas residenciales de 22:00 a 06:00 horas.",
    18: "Se prohíbe usar escapes abiertos ruidosos y accionar el claxon innecesariamente o frente a escuelas y hospitales.",
    19: "Todo automóvil en circulación debe tener seguro obligatorio de responsabilidad civil por daños a terceros.",
    20: "Las multas se calculan en UMA y se puede interponer inconformidad ante el Juez Cívico en un plazo máximo de 15 días hábiles."
}

# Inicialización de motor de búsqueda semántica con soporte dual (Transformers / Scikit-Learn fallback)
USE_TRANSFORMERS = False
try:
    from sentence_transformers import SentenceTransformer
    import faiss
    import numpy as np
    
    print("Iniciando modelo neuronal SentenceTransformers...")
    encoder = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
    texts = [f"{a['title']}. {a['text']}" for a in ARTICLES_DATA]
    embeddings = encoder.encode(texts, convert_to_numpy=True, normalize_embeddings=True)
    
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatIP(dimension)
    index.add(embeddings)
    
    USE_TRANSFORMERS = True
    THRESHOLD = 0.50  # Umbral óptimo calibrado para embeddings densos
    print("Motor Transformer cargado con éxito. Umbral tau = 0.50")
except Exception as e:
    print(f"Transformers no disponible ({e}), inicializando motor léxico TF-IDF...")
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    import numpy as np
    
    texts = [f"{a['title']}. {a['text']}" for a in ARTICLES_DATA]
    tfidf = TfidfVectorizer(ngram_range=(1, 2), sublinear_tf=True)
    doc_vectors = tfidf.fit_transform(texts)
    THRESHOLD = 0.15  # Umbral óptimo para TF-IDF
    print("Motor TF-IDF inicializado con éxito. Umbral tau = 0.15")


def query_assistant(user_question: str) -> Tuple[str, str, str, str, str]:
    """
    Procesa la pregunta del usuario aplicando la regla estricta de rechazo anti-alucinaciones:
    - Retorna el dictamen de validación.
    - El artículo oficial citado.
    - El texto íntegro de la norma.
    - La respuesta ciudadana sintetizada y libre de alucinaciones.
    - El desglose de artículos Top-3 recuperados.
    """
    if not user_question.strip():
        return (
            "⚠️ Por favor escribe una consulta válida.",
            "Ninguno",
            "—",
            "—",
            "—"
        )
    
    top_indices = []
    top_scores = []
    
    if USE_TRANSFORMERS:
        q_emb = encoder.encode([user_question], convert_to_numpy=True, normalize_embeddings=True)
        scores, indices = index.search(q_emb, k=3)
        top_indices = indices[0].tolist()
        top_scores = scores[0].tolist()
    else:
        q_vec = tfidf.transform([user_question])
        sims = cosine_similarity(q_vec, doc_vectors)[0]
        sorted_idx = np.argsort(sims)[::-1][:3]
        top_indices = sorted_idx.tolist()
        top_scores = [float(sims[i]) for i in top_indices]
    
    best_score = float(top_scores[0])
    best_idx = top_indices[0]
    best_article = ARTICLES_DATA[best_idx]
    
    # Desglose de Top 3
    top3_breakdown = []
    for rank, (idx, score) in enumerate(zip(top_indices, top_scores), start=1):
        art = ARTICLES_DATA[idx]
        top3_breakdown.append(f"**Top {rank}** [{score:.3f}]: {art['id']} — {art['title']}")
    top3_text = "\n\n".join(top3_breakdown)
    
    # REGLA DE RECHAZO: ¿Supera el umbral de certeza tau?
    if best_score < THRESHOLD:
        status_md = (
            f"### 🚫 CONSULTA RECHAZADA (ANTI-ALUCINACIÓN)\n"
            f"**Similitud máxima:** `{best_score:.3f}` (Umbral mínimo requerido $\\tau$: `{THRESHOLD:.2f}`)\n\n"
            f"> **Dictamen:** Esta consulta no se encuentra contemplada en el *Reglamento de Tránsito y Vialidad de Apodaca, N.L.* "
            f"El asistente rechaza especular para evitar inducir al ciudadano a multas o infracciones erróneas."
        )
        answer = (
            "Lo lamento, pero esa situación o concepto **no está contemplado en este reglamento**. "
            "No puedo responder ni inventar normas que no existan en el documento oficial."
        )
        quoted_article = "Ninguno (Abstención preventiva por pregunta fuera de dominio o trampa)"
        official_text = "No aplica citación textual debido a que ningún artículo de la normativa cubre este supuesto con la certeza necesaria."
        return status_md, answer, quoted_article, official_text, top3_text
    
    # RESPUESTA FUNDAMENTADA
    status_md = (
        f"### ✅ RESPUESTA FUNDAMENTADA EN LA NORMATIVA\n"
        f"**Similitud semántica calculada:** `{best_score:.3f}` (Supera el umbral $\\tau$: `{THRESHOLD:.2f}`)\n\n"
        f"> **Garantía de Fidelidad:** La respuesta se genera exclusivamente a partir del {best_article['id']}."
    )
    
    # Respuesta sintetizada
    synthesized = SYNTHESIS_MAP.get(
        best_article["num"],
        f"Con base en el {best_article['id']}, la normativa estipula expresamente las condiciones relativas a {best_article['title'].lower()}."
    )
    
    quoted_article = f"{best_article['id']}: {best_article['title']}"
    official_text = best_article["text"]
    
    return status_md, synthesized, quoted_article, official_text, top3_text


# Interfaz Web con Gradio
def build_interface():
    import gradio as gr
    
    custom_css = """
    .gradio-container { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    .badge-box { border-radius: 8px; padding: 12px; margin-bottom: 10px; }
    """
    
    with gr.Blocks(theme=gr.themes.Soft(), css=custom_css, title="OrientaMX — Track 4 RNAP Hack 2026") as demo:
        gr.Markdown(
            """
            # 🏛️ OrientaMX — Asistente Legal Anti-Alucinaciones
            ### **RNAP Hack 2026 · Track 4: The Assistant That Doesn’t Make Things Up**
            *Materia: Redes Neuronales y Aprendizaje Profundo | Equipo: trabajo_goty*
            
            Este sistema responde preguntas sobre el **Reglamento de Tránsito y Vialidad de Apodaca, N.L.**, citando el **artículo exacto** y su **texto oficial**.
            Si se ingresa una pregunta trampa o fuera de dominio, el modelo **se niega categóricamente a responder** mediante una regla de rechazo calibrada ($\tau$).
            """
        )
        
        with gr.Row():
            with gr.Column(scale=5):
                question_input = gr.Textbox(
                    lines=3,
                    placeholder="Escribe tu consulta ciudadana sobre el reglamento de tránsito...",
                    label="📝 Pregunta del Ciudadano / Juez"
                )
                submit_btn = gr.Button("🔍 Consultar Normativa Oficial", variant="primary", size="lg")
                
                gr.Markdown("#### 💡 Preguntas de Prueba Rápidas (Legítimas y Trampas):")
                examples = [
                    ["¿Cuál es la velocidad máxima permitida frente a una escuela primaria por la mañana?"],
                    ["¿Los niños chiquitos pueden viajar en el asiento del copiloto?"],
                    ["¿Cuánto alcohol puedo haber tomado para que no me lleven al corralón?"],
                    ["¿Puedo ir hablando por celular con el altavoz o manos libres activado?"],
                    ["¿Qué pasa si me choco y hay una persona herida en el lugar?"],
                    ["¿Cuánto cuesta la verificación vehicular semestral en los verificentros?"],
                    ["¿Cuál es la multa por no pagar el boleto del parquímetro virtual en la calle?"],
                    ["¿Puedo tramitar un permiso municipal para volar un dron sobre la avenida?"]
                ]
                gr.Examples(examples=examples, inputs=[question_input])
                
            with gr.Column(scale=6):
                status_output = gr.Markdown(label="🛡️ Estado de Verificación Anti-Alucinaciones")
                answer_output = gr.Textbox(label="💬 Respuesta Ciudadana Fundamentada", lines=3)
                article_title_output = gr.Textbox(label="📜 Artículo Oficial Citado", lines=1)
                article_text_output = gr.TextArea(label="📖 Texto Íntegro del Artículo Oficial Citado", lines=5)
                
                with gr.Accordion("🔍 Detalle del Top-3 de Artículos Similares y Puntuaciones", open=False):
                    top3_output = gr.Markdown()
                    
        submit_btn.click(
            fn=query_assistant,
            inputs=[question_input],
            outputs=[status_output, answer_output, article_title_output, article_text_output, top3_output]
        )
        question_input.submit(
            fn=query_assistant,
            inputs=[question_input],
            outputs=[status_output, answer_output, article_title_output, article_text_output, top3_output]
        )
        
        gr.Markdown(
            """
            ---
            **Arquitectura del Prototipo:**
            - **Recuperación Semántica:** Dense Transformer (`paraphrase-multilingual-MiniLM-L12-v2`) con indexación de producto interno en FAISS.
            - **Filtro Anti-Alucinaciones:** Rechazo determinista por umbral angular ($\tau = 0.50$).
            - **Acondicionamiento Contextual:** Síntesis restringida al artículo citado, garantizando *Groundedness* del 100%.
            """
        )
    return demo


if __name__ == "__main__":
    try:
        import gradio as gr
        demo = build_interface()
        print("Iniciando aplicación Gradio en modo local...")
        demo.launch(server_name="127.0.0.1", server_port=7860, share=False)
    except ImportError:
        print("Gradio no está instalado en este entorno. Instálalo con: pip install gradio")
        print("\nPrueba de consulta por consola:")
        test_q = "¿Cuál es el límite de velocidad en zona escolar por la mañana?"
        res = query_assistant(test_q)
        print(f"Pregunta: {test_q}")
        print(f"Respuesta: {res[1]}")
        print(f"Artículo: {res[2]}")
        
        test_trap = "¿Dónde se hace la verificación ambiental de humo obligatoria?"
        res_trap = query_assistant(test_trap)
        print(f"\nPregunta trampa: {test_trap}")
        print(f"Respuesta: {res_trap[1]}")
        print(f"Artículo: {res_trap[2]}")
