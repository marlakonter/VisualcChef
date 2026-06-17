import streamlit as st
import pandas as pd
import json
from google import genai
from PIL import Image
from marcadores import MARCADORES, evaluar_semaforo, obtener_preguntas

st.set_page_config(page_title="LabCheck — Lee tus resultados", page_icon="📑", layout="wide")

# ============================================================
# SISTEMA DE DISEÑO
# Paleta: azul tinta (texto/headers), hueso cálido (fondo),
# verde bosque / ámbar mostaza / terracota (estados del semáforo).
# Tipografía: serif con carácter para títulos (evoca "documento
# clínico anotado"), sans limpia para cuerpo y datos.
# ============================================================
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Source+Serif+4:opsz,wght@8..60,500;8..60,700&family=Inter:wght@400;500;600&display=swap');

    :root {
        --tinta: #1B3A4B;
        --hueso: #F7F3EC;
        --verde: #3D7068;
        --ambar: #C9A227;
        --terracota: #A8453E;
    }

    .stApp {
        background-color: var(--hueso);
    }

    h1, h2, h3 {
        font-family: 'Source Serif 4', serif !important;
        color: var(--tinta) !important;
    }

    p, span, div, label, .stMarkdown, .stRadio label, .stFileUploader label,
    [data-testid="stWidgetLabel"] p {
        font-family: 'Inter', sans-serif;
        color: var(--tinta) !important;
    }

    [data-testid="stFileUploaderDropzone"] {
        background-color: var(--hueso) !important;
        border: 1px dashed #C9C2AE !important;
    }
    [data-testid="stFileUploaderDropzone"] * {
        color: var(--tinta) !important;
    }

    .lc-hero {
        text-align: center;
        padding: 1.5rem 0 0.5rem 0;
    }
    .lc-hero h1 {
        font-size: 2.6rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
        letter-spacing: -0.01em;
    }
    .lc-hero p {
        font-size: 1.05rem;
        color: #5A6B72;
        font-style: italic;
        margin-top: 0;
    }

    /* Tarjeta de anotación: borde lateral grueso del color del estado,
       como si el resultado estuviera subrayado en el margen. */
    .lc-anotacion {
        background-color: white;
        border-left: 6px solid var(--lc-color);
        border-radius: 4px;
        padding: 14px 18px;
        margin-bottom: 10px;
        box-shadow: 0 1px 3px rgba(27, 58, 75, 0.08);
    }
    .lc-anotacion b {
        font-family: 'Source Serif 4', serif;
        font-size: 1.05rem;
    }

    /* Barra de progreso de pasos */
    .lc-progreso {
        display: flex;
        justify-content: center;
        gap: 0.4rem;
        margin: 0.5rem 0 1.5rem 0;
    }
    .lc-paso {
        font-family: 'Inter', sans-serif;
        font-size: 0.82rem;
        font-weight: 500;
        padding: 5px 14px;
        border-radius: 20px;
        color: #8A9499;
        background-color: transparent;
        border: 1px solid #D8D2C4;
    }
    .lc-paso-activo {
        color: white;
        background-color: var(--tinta);
        border: 1px solid var(--tinta);
    }
    .lc-paso-hecho {
        color: var(--verde);
        border: 1px solid var(--verde);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="lc-hero">
        <h1>📑 LabCheck</h1>
        <p>Tu estudio, explicado en tu idioma — antes de tu próxima consulta</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# --- Disclaimer fijo: código fijo, NO generado por la IA, siempre visible ---
st.warning(
    "⚠️ **Esto es una herramienta informativa y educativa.** No ofrece diagnósticos "
    "ni sustituye la opinión de un profesional de la salud. Lleva siempre tus "
    "resultados originales y estas preguntas a tu médico."
)

# --- Inicializar estado de sesión para controlar el flujo entre pantallas ---
if "paso" not in st.session_state:
    st.session_state.paso = 1
if "valores_extraidos" not in st.session_state:
    st.session_state.valores_extraidos = None
if "valores_confirmados" not in st.session_state:
    st.session_state.valores_confirmados = None

# --- Barra de progreso de los 4 pasos ---
nombres_pasos = ["1 · Datos", "2 · Confirmar", "3 · Resultados", "4 · Preguntas"]
html_pasos = '<div class="lc-progreso">'
for i, nombre in enumerate(nombres_pasos, start=1):
    if i == st.session_state.paso:
        clase = "lc-paso lc-paso-activo"
    elif i < st.session_state.paso:
        clase = "lc-paso lc-paso-hecho"
    else:
        clase = "lc-paso"
    html_pasos += f'<span class="{clase}">{nombre}</span>'
html_pasos += "</div>"
st.markdown(html_pasos, unsafe_allow_html=True)

# --- Obtener API key de los Secrets ---
api_key = st.secrets.get("GEMINI_API_KEY", None)
if not api_key:
    st.error("🚨 Error de configuración: La API Key de Gemini no se ha configurado en los Secrets del servidor.")
    st.stop()

client = genai.Client(api_key=api_key)


def extraer_valores_con_gemini(imagen: Image.Image) -> dict:
    """
    Manda la imagen del estudio a Gemini y regresa un diccionario con los
    valores detectados. Si Gemini falla en regresar JSON válido, regresa
    un diccionario vacío -- eso es lo que dispara la tabla editable en blanco
    para que el usuario llene manualmente.
    """
    nombres_marcadores = list(MARCADORES.keys())

    prompt = f"""Eres un asistente que extrae valores de estudios de laboratorio a partir de una imagen.
Busca ÚNICAMENTE estos marcadores, usando exactamente estos nombres como llaves:
{json.dumps(nombres_marcadores, ensure_ascii=False)}

Para cada marcador que SÍ encuentres en la imagen, extrae su valor numérico tal como
aparece impreso, sin redondear ni convertir unidades.
Si un marcador no aparece en la imagen, simplemente NO lo incluyas en la respuesta.

Responde ÚNICAMENTE con un JSON válido, sin texto adicional, sin explicación,
sin marcadores de markdown como ```json, con esta estructura exacta:
{{"Hemoglobina": 14.2, "Glucosa": 95}}"""

    try:
        respuesta = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[prompt, imagen],
        )
        texto_limpio = respuesta.text.strip()
        texto_limpio = texto_limpio.replace("```json", "").replace("```", "").strip()
        valores = json.loads(texto_limpio)
        # Filtro de seguridad: solo aceptar llaves que están en nuestra tabla fija
        valores = {k: v for k, v in valores.items() if k in MARCADORES}
        return valores
    except Exception:
        # Si Gemini regresa algo no parseable, no truena la app -- regresa vacío
        # y la Pantalla 2 deja la tabla en blanco para llenado manual.
        return {}


# ============================================================
# PANTALLA 1 — Datos básicos
# ============================================================
if st.session_state.paso == 1:
    st.subheader("Sube o fotografía tu estudio")
    sexo = st.radio("Sexo", ["Hombre", "Mujer"], horizontal=True)

    metodo = st.radio("¿Cómo quieres ingresar tu estudio?", ["📁 Subir archivo", "📷 Tomar foto"], horizontal=True)

    imagen = None
    if metodo == "📁 Subir archivo":
        archivo_subido = st.file_uploader("Sube la foto de tu estudio de laboratorio", type=["jpg", "jpeg", "png"])
        if archivo_subido:
            imagen = Image.open(archivo_subido)
    else:
        foto_tomada = st.camera_input("Toma una foto de tu estudio de laboratorio")
        if foto_tomada:
            imagen = Image.open(foto_tomada)

    if imagen:
        st.image(imagen, caption="Estudio cargado", width=400)

        if st.button("Analizar estudio →", type="primary"):
            st.session_state.sexo = sexo
            st.session_state.imagen = imagen
            with st.spinner("🔎 Leyendo tu estudio..."):
                st.session_state.valores_extraidos = extraer_valores_con_gemini(imagen)
            st.session_state.paso = 2
            st.rerun()

# ============================================================
# PANTALLA 2 — Confirmación de lectura (editable)
# ============================================================
elif st.session_state.paso == 2:
    st.subheader("Confirma lo que leímos")

    if not st.session_state.valores_extraidos:
        st.info(
            "No se detectaron valores automáticamente (foto borrosa o formato no reconocido). "
            "Agrega los valores manualmente abajo, o regresa y sube una foto más clara."
        )

    # Construir filas: todos los marcadores detectados, listas para edición.
    # El usuario también puede agregar manualmente los que falten.
    filas = []
    for nombre, valor in (st.session_state.valores_extraidos or {}).items():
        filas.append({"Marcador": nombre, "Valor": valor, "Unidad": MARCADORES[nombre]["unidad"]})

    if not filas:
        # Tabla vacía con los marcadores disponibles para que el usuario elija y llene
        filas = [{"Marcador": "", "Valor": 0.0, "Unidad": ""}]

    df = pd.DataFrame(filas)

    tabla_editada = st.data_editor(
        df,
        num_rows="dynamic",
        column_config={
            "Marcador": st.column_config.SelectboxColumn(
                "Marcador", options=list(MARCADORES.keys()), required=True
            ),
            "Valor": st.column_config.NumberColumn("Valor", required=True),
            "Unidad": st.column_config.TextColumn("Unidad", disabled=True),
        },
        use_container_width=True,
        key="editor_valores",
    )

    col_a, col_b = st.columns([1, 1])
    with col_a:
        if st.button("← Regresar"):
            st.session_state.paso = 1
            st.rerun()
    with col_b:
        if st.button("Confirmar y ver resultados →", type="primary"):
            confirmados = {}
            for _, fila in tabla_editada.iterrows():
                if fila["Marcador"]:
                    confirmados[fila["Marcador"]] = fila["Valor"]
            st.session_state.valores_confirmados = confirmados
            st.session_state.paso = 3
            st.rerun()

# ============================================================
# PANTALLA 3 — Semáforo
# ============================================================
elif st.session_state.paso == 3:
    st.subheader("Tus resultados, explicados")

    color_hex = {"verde": "#3D7068", "amarillo": "#C9A227", "rojo": "#A8453E", "desconocido": "#8A9499"}
    etiqueta = {"verde": "EN RANGO", "amarillo": "ATENCIÓN", "rojo": "FUERA DE RANGO", "desconocido": "SIN DATO"}

    for nombre, valor in st.session_state.valores_confirmados.items():
        semaforo = evaluar_semaforo(nombre, valor, st.session_state.sexo)
        info = MARCADORES[nombre]
        st.markdown(
            f"""<div class="lc-anotacion" style="--lc-color: {color_hex[semaforo]};">
                <b>{nombre}</b>
                <span style="color:{color_hex[semaforo]}; font-size:0.78rem; font-weight:600; margin-left:8px;">
                    {etiqueta[semaforo]}
                </span><br>
                <span style="color:#5A6B72;">{valor} {info['unidad']}</span><br>
                {info['explicacion']}
            </div>""",
            unsafe_allow_html=True,
        )

    st.write("")
    col_a, col_b = st.columns([1, 1])
    with col_a:
        if st.button("← Editar valores"):
            st.session_state.paso = 2
            st.rerun()
    with col_b:
        if st.button("Ver preguntas para mi doctor →", type="primary"):
            st.session_state.paso = 4
            st.rerun()

# ============================================================
# PANTALLA 4 — Preguntas para el doctor
# ============================================================
elif st.session_state.paso == 4:
    st.subheader("Preguntas para tu próxima consulta")
    st.caption("El objetivo no es darte un diagnóstico, sino ayudarte a aprovechar mejor el tiempo con tu médico.")

    hay_preguntas = False
    for nombre, valor in st.session_state.valores_confirmados.items():
        semaforo = evaluar_semaforo(nombre, valor, st.session_state.sexo)
        if semaforo in ("amarillo", "rojo"):
            preguntas = obtener_preguntas(nombre, valor, st.session_state.sexo)
            if preguntas:
                hay_preguntas = True
                with st.container(border=True):
                    st.markdown(f"**Sobre tu {nombre}:**")
                    for p in preguntas:
                        st.markdown(f"- {p}")

    if not hay_preguntas:
        st.success("✅ Todos tus valores están dentro de rango. Aun así, lleva tus resultados a tu médico de rutina.")

    st.write("---")
    st.warning(
        "⚠️ Recuerda: esta lista es informativa y educativa, generada a partir de rangos de "
        "referencia general. No sustituye una consulta médica ni un diagnóstico profesional."
    )

    if st.button("← Regresar a resultados"):
        st.session_state.paso = 3
        st.rerun()

    if st.button("🔄 Analizar otro estudio"):
        st.session_state.paso = 1
        st.session_state.valores_extraidos = None
        st.session_state.valores_confirmados = None
        st.rerun()