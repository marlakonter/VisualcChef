import streamlit as st
from google import genai
from PIL import Image

# Configuración de la página (Pone el título en la pestaña del navegador y un diseño ancho)
st.set_page_config(page_title="ChefVisual - IA", page_icon="🍳", layout="wide")

# Diseño hermoso con títulos avanzados
st.markdown("<h1 style='text-align: center; color: #FF4B4B;'>🍳 ChefVisual</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #555555;'>¡Toma una foto a tus ingredientes y la IA te dirá qué cocinar gratis!</h3>", unsafe_allow_html=True)
st.write("---")

# Intentar obtener la API Key desde los Secrets de Streamlit de forma segura
api_key = None
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]

if not api_key:
    st.error("🚨 Error de configuración: La API Key de Gemini no se ha configurado correctamente en los Secrets del servidor.")
else:
    # Inicializar el cliente de Google GenAI con la clave de los secrets
    client = genai.Client(api_key=api_key)

    # Crear dos columnas: Izquierda para subir la foto, Derecha para los resultados
    col1, col2 = st.columns([1, 1.2], gap="large")

    with col1:
        st.subheader("📸 Sube la foto de tu refrigerador o ingredientes")
        archivo_subido = st.file_uploader("Elige una imagen...", type=["jpg", "jpeg", "png"])
        
        if archivo_subido:
            imagen = Image.open(archivo_subido)
            # Muestra la imagen en una tarjeta bonita con bordes
            with st.container(border=True):
                st.image(imagen, caption="Tus ingredientes listos", use_container_width=True)

    with col2:
        st.subheader("🧑‍🍳 Recetas Sugeridas")
        
        if archivo_subido:
            # Mensaje de carga animado super profesional
            with st.spinner("🧠 El chef está analizando tu foto y creando las mejores recetas..."):
                try:
                    # El prompt definitivo para que la IA decore el texto de forma hermosa
                    prompt = (
                        "Actúa como un chef profesional y creativo. Analiza detalladamente los ingredientes "
                        "visibles en esta imagen y propón 3 recetas diferentes que se puedan preparar con ellos. "
                        "Usa negritas para los títulos, listas ordenadas para los pasos, pon los ingredientes "
                        "necesarios al inicio de cada receta y decora los textos con emojis de cocina (🍅, 🍗, 🧅, 🧂) "
                        "para que se vea muy vistoso, limpio, elegante y apetecible."
                    )
                    
                    # Llamada al modelo de Gemini con soporte de imagen
                    respuesta = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=[prompt, imagen]
                    )
                    
                    # Mostrar el resultado dentro de un contenedor elegante con bordes
                    with st.container(border=True):
                        st.markdown(respuesta.text)
                        st.success("¡Buen provecho! 🍽️")
                        
                except Exception as e:
                    st.error(f"❌ Hubo un problema al conectar con Gemini. Verifica tu API Key. Detalle: {e}")
        else:
            # Mensaje amigable si aún no suben foto
            st.info("💡 Por favor, sube una foto en la sección de la izquierda para que el chef pueda empezar a cocinar.")