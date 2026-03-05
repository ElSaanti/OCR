import streamlit as st
import cv2
import numpy as np
import pytesseract
from PIL import Image


st.title("Reconocimiento óptico de Caracteres")

# --- EXPANDER DE USO ---
with st.expander("📖 Cómo usar el OCR", expanded=True):
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
        1. **Captura**: Haz clic en el botón de la cámara para tomar una foto del texto.
        2. **Filtro**: Si el texto es difícil de leer, prueba activar el filtro en la barra lateral.
        3. **Resultado**: El texto detectado aparecerá mágicamente debajo de la foto.
        """)
    with col2:
        try:
            # Insertamos tu imagen aquí
            st.image(Image.open('traductor.jpg'), use_container_width=True)
        except:
            st.write("🖼️")

st.divider()

img_file_buffer = st.camera_input("Toma una Foto")

with st.sidebar:
    st.subheader("Configuración")
    filtro = st.radio("Aplicar Filtro", ('Con Filtro', 'Sin Filtro'), index=1)

if img_file_buffer is not None:
    # To read image file buffer with OpenCV:
    bytes_data = img_file_buffer.getvalue()
    cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
    
    if filtro == 'Con Filtro':
        cv2_img = cv2.bitwise_not(cv2_img)
    else:
        cv2_img = cv2_img
        
    img_rgb = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)
    text = pytesseract.image_to_string(img_rgb)
    
    if text.strip():
        st.subheader("Texto detectado:")
        st.info(text)
    else:
        st.warning("No se detectó texto. Intenta acercar más la cámara o mejorar la iluminación.")
