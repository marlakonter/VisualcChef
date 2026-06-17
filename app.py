import streamlit as st
from google import genai
from google.genai import types
from PIL import Image
import os

# Configuración de la página web
st.set_page_config(page_title="ChefVisual - Recetas Inteligentes", page_icon="🍳", layout="centered")

st.title("🍳 ChefVisual")
st.write("¡Toma una foto a tus ingredientes y la IA te dirá qué cocinar gratis!")

# Intentar obtener la API Key de los secretos guardados en el servidor
# Si no existe, busca una variable de entorno local
api_key = st.secrets.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")

if not api_key:
    st.error("Error de configuración: La API Key de Gemini no se ha configurado en el servidor.", icon="🚨")
else:
    # Inicializar el cliente de Google GenAI de forma interna y automática
    client = genai.Client(api_key=api_key)

    # Componente para subir la imagen
    uploaded_file = st.file_uploader("Sube una foto de tus ingredientes o tu refrigerador", type=["jpg", "jpeg", "png"])

    # Filtros adicionales
    preferencia = st.selectbox(
        "¿Tienes alguna preferencia de dieta o tiempo?",
        ["Sin restricciones", "Vegana", "Vegetariana", "Saludable/Fitness", "Rápida (menos de 20 min)", "Apta para niños"]
    )

    if uploaded_file is not None:
        imagen = Image.open(uploaded_file)
        st.image(imagen, caption="Tus ingredientes", use_container_width=True)
        
        if st.button("✨ ¡Generar Receta!"):
            with st.spinner("El Chef está analizando tus ingredientes..."):
                try:
                    prompt_texto = f"""
                    Actúa como un chef profesional creativo. Analiza detenidamente la imagen provista e identifica todos los ingredientes visibles.
                    Con base en ellos (y permitiendo ingredientes básicos de alacena como agua, sal, pimienta, aceite u otros condimentos comunes), 
                    crea una receta deliciosa.
                    
                    Restricción de dieta/tiempo seleccionada por el usuario: {preferencia}.
                    
                    Devuelve la respuesta estructurada elegantemente en formato Markdown:
                    1. Nombre del Platillo (con un emoji).
                    2. Tiempo estimado y dificultad.
                    3. Lista de ingredientes identificados en la foto y los extras de alacena necesarios.
                    4. Instrucciones paso a paso bien detalladas.
                    5. Un tip secreto del chef para mejorar el platillo.
                    """

                    response = client.models.generate_content(
                        model='gemini-1.5-flash',
                        contents=[imagen, prompt_texto]
                    )
                    
                    st.success("¡Receta lista!")
                    st.markdown(response.text)
                    
                except Exception as e:
                    st.error(f"Hubo un error al procesar tu solicitud. Por favor intenta de nuevo.")