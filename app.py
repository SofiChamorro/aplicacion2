import streamlit as st
import os
import time
import glob
from gtts import gTTS
from PIL import Image
import base64

# Configuración de la página
st.set_page_config(page_title="Texto a Audio", layout="centered")

# Estilo personalizado con HTML
st.markdown("""
    <style>
        .stApp {
            background-color: #f0f2f6;
        }
        h1, h2, h3 {
            color: #2c3e50;
        }
        .title-style {
            background-color: #4CAF50;
            padding: 10px;
            border-radius: 10px;
            color: white;
            text-align: center;
        }
        .button-style {
            background-color: #009688 !important;
            color: white !important;
        }
    </style>
""", unsafe_allow_html=True)

# Título principal
st.markdown("<h1 class='title-style'>Conversión de Texto a Audio</h1>", unsafe_allow_html=True)

# Imagen
image = Image.open('gato.png')
st.image(image, width=350)

# Sidebar
with st.sidebar:
    st.subheader("🗣️ Escribe y/o selecciona texto para ser escuchado.")

# Carpeta temporal
try:
    os.mkdir("temp")
except:
    pass

# Fábula
st.subheader("📜 Una pequeña fábula")
st.markdown("""
<div style="background-color:#fff8dc; padding:10px; border-radius:10px;">
¡Ay! —dijo el ratón—. El mundo se hace cada día más pequeño. Al principio era tan grande que le tenía miedo.  
Corría y corría y me alegraba ver esos muros a diestra y siniestra, en la distancia.  
Pero esas paredes se estrechan tan rápido que me encuentro en el último cuarto y ahí en el rincón está  
la trampa sobre la cual debo pasar. Todo lo que debes hacer es cambiar de rumbo —dijo el gato... y se lo comió.  
<br><br><i>— Franz Kafka</i>
</div>
""", unsafe_allow_html=True)

# Entrada de texto
st.markdown("### ✍️ ¿Quieres escucharlo? Copia o escribe el texto:")
text = st.text_area("Texto a convertir en audio:")

# Idioma
option_lang = st.selectbox("Selecciona el lenguaje", ("Español", "English"))
lg = 'es' if option_lang == "Español" else 'en'

# Conversión de texto a voz
def text_to_speech(text, tld, lg):
    tts = gTTS(text, lang=lg)
    try:
        my_file_name = text[0:20].strip().replace(" ", "_")
    except:
        my_file_name = "audio"
    tts.save(f"temp/{my_file_name}.mp3")
    return my_file_name, text

# Botón para convertir a audio
if st.button("🔊 Convertir a Audio"):
    if text.strip() != "":
        result, output_text = text_to_speech(text, 'com', lg)
        audio_path = f"temp/{result}.mp3"
        audio_file = open(audio_path, "rb")
        audio_bytes = audio_file.read()

        st.markdown("### 🎧 Tu audio:")
        st.audio(audio_bytes, format="audio/mp3", start_time=0)

        # Botón de descarga
        with open(audio_path, "rb") as f:
            data = f.read()

        def get_binary_file_downloader_html(bin_file, file_label='File'):
            bin_str = base64.b64encode(data).decode()
            href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}">⬇️ Descargar {file_label}</a>'
            return href

        st.markdown(get_binary_file_downloader_html(audio_path, file_label="archivo de audio"), unsafe_allow_html=True)
    else:
        st.warning("⚠️ Por favor, ingresa un texto para convertir.")

# Limpieza de archivos viejos
def remove_files(n):
    mp3_files = glob.glob("temp/*mp3")
    if len(mp3_files) != 0:
        now = time.time()
        n_days = n * 86400
        for f in mp3_files:
            if os.stat(f).st_mtime < now - n_days:
                os.remove(f)

remove_files(7)
