from textblob import TextBlob
import pandas as pd
import streamlit as st
from PIL import Image
from googletrans import Translator
from streamlit_lottie import st_lottie
import json


# ---------------------------------------------------------
# CONFIGURACIÓN
# ---------------------------------------------------------

st.set_page_config(
    page_title="Análisis de Sentimiento",
    layout="centered"
)


# ---------------------------------------------------------
# ESTILOS VISUALES
# ---------------------------------------------------------

st.markdown("""
<style>

    /* Fondo general */
    .stApp {
        background:
            radial-gradient(circle at 10% 10%, rgba(255, 105, 180, 0.20), transparent 30%),
            radial-gradient(circle at 90% 20%, rgba(100, 149, 237, 0.20), transparent 30%),
            radial-gradient(circle at 50% 90%, rgba(138, 43, 226, 0.18), transparent 35%),
            #100c1c;
        color: white;
    }

    /* Contenedor principal */
    .main .block-container {
        max-width: 850px;
        padding-top: 3rem;
        padding-bottom: 4rem;
    }

    /* Título */
    .titulo {
        text-align: center;
        font-size: 3.2rem;
        font-weight: 800;
        margin-bottom: 0.2rem;
        background: linear-gradient(90deg, #ff7eb3, #c77dff, #70d6ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .subtitulo {
        text-align: center;
        color: #d8cfe5;
        font-size: 1.15rem;
        margin-bottom: 2rem;
    }

    /* Imagen principal */
    .imagen-principal {
        display: flex;
        justify-content: center;
        margin: 1rem 0 2rem 0;
    }

    /* Tarjetas */
    .card {
        background: rgba(255,255,255,0.08);
        border: 1px solid rgba(255,255,255,0.15);
        border-radius: 24px;
        padding: 25px;
        margin: 20px 0;
        box-shadow: 0 10px 35px rgba(0,0,0,0.25);
        backdrop-filter: blur(12px);
    }

    /* Tarjeta del resultado */
    .resultado {
        background: linear-gradient(
            135deg,
            rgba(199,125,255,0.18),
            rgba(112,214,255,0.12)
        );
        border: 1px solid rgba(255,255,255,0.18);
        border-radius: 24px;
        padding: 25px;
        margin-top: 25px;
        text-align: center;
        box-shadow: 0 12px 35px rgba(0,0,0,0.3);
    }

    /* Métricas */
    .metricas {
        display: flex;
        justify-content: center;
        gap: 25px;
        margin-top: 20px;
    }

    .metrica {
        background: rgba(255,255,255,0.08);
        border-radius: 18px;
        padding: 18px 30px;
        min-width: 180px;
        text-align: center;
    }

    .metrica-titulo {
        color: #cfc3da;
        font-size: 0.9rem;
    }

    .metrica-valor {
        color: #ffffff;
        font-size: 1.8rem;
        font-weight: 700;
    }

    /* Resultado emocional */
    .emocion {
        font-size: 1.8rem;
        font-weight: 700;
        margin-top: 10px;
    }

    /* Video */
    .video-card {
        background: linear-gradient(
            135deg,
            rgba(255, 70, 100, 0.14),
            rgba(120, 70, 200, 0.14)
        );
        border: 1px solid rgba(255,255,255,0.15);
        border-radius: 24px;
        padding: 20px;
        margin-top: 25px;
        box-shadow: 0 12px 35px rgba(0,0,0,0.3);
    }

    .video-titulo {
        text-align: center;
        color: #ffffff;
        font-size: 1.3rem;
        font-weight: 700;
        margin-bottom: 15px;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(
            180deg,
            #171025,
            #211438,
            #151020
        );
        border-right: 1px solid rgba(255,255,255,0.1);
    }

    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #e4b5ff;
    }

    section[data-testid="stSidebar"] p {
        color: #d8cfe5;
        line-height: 1.6;
    }

    /* Input */
    div[data-baseweb="input"] {
        background-color: rgba(255,255,255,0.08);
        border-radius: 14px;
        border: 1px solid rgba(255,255,255,0.18);
    }

    div[data-baseweb="input"] input {
        color: white !important;
    }

    div[data-baseweb="input"] input::placeholder {
        color: #bcb2c8 !important;
    }

    /* Expander */
    div[data-testid="stExpander"] {
        background: rgba(255,255,255,0.06);
        border: 1px solid rgba(255,255,255,0.15);
        border-radius: 20px;
        overflow: hidden;
    }

    /* Texto */
    p, label {
        color: #eee8f4;
    }

    /* Separador */
    hr {
        border-color: rgba(255,255,255,0.12);
    }

</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# ENCABEZADO
# ---------------------------------------------------------

st.markdown(
    '<div class="titulo">💭 Análisis de Sentimiento</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitulo">Descubre las emociones detrás de tus palabras</div>',
    unsafe_allow_html=True
)


# ---------------------------------------------------------
# IMAGEN PRINCIPAL
# ---------------------------------------------------------

image = Image.open('EMOCIONES.png')

st.markdown('<div class="imagen-principal">', unsafe_allow_html=True)
st.image(image, width=650)
st.markdown('</div>', unsafe_allow_html=True)


# ---------------------------------------------------------
# INTRODUCCIÓN
# ---------------------------------------------------------

st.markdown("""
<div class="card">

<h3 style="text-align:center;">✨ ¿Cómo funciona?</h3>

<p style="text-align:center;">
Escribe una frase y nuestro sistema analizará el sentimiento presente
en ella. El resultado tendrá en cuenta la <b>polaridad</b> y la
<b>subjetividad</b> del texto.
</p>

</div>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------

with st.sidebar:

    st.markdown("## 🧠 Sobre el análisis")

    st.write(
        """
        **Polaridad**

        Indica si el sentimiento expresado en el texto es positivo,
        negativo o neutral.

        Su valor oscila entre **-1 y 1**:

        🔴 -1 → Muy negativo

        ⚪ 0 → Neutral

        🟢 1 → Muy positivo
        """
    )

    st.divider()

    st.write(
        """
        **Subjetividad**

        Mide cuánto del contenido corresponde a opiniones,
        emociones o creencias frente a información objetiva.

        Su valor va de **0 a 1**:

        📘 0 → Objetivo

        💭 1 → Subjetivo
        """
    )

    st.divider()

    st.caption("Proyecto realizado con Python + Streamlit")


# ---------------------------------------------------------
# ANALIZADOR
# ---------------------------------------------------------

with st.expander("🔍 Analizar un texto", expanded=True):

    st.markdown(
        "### ✍️ Escribe una frase"
    )

    text = st.text_input(
        "",
        placeholder="Ejemplo: Hoy estoy muy feliz porque salió el sol ☀️"
    )

    if text:

        translator = Translator()

        translation = translator.translate(
            text,
            src="es",
            dest="en"
        )

        trans_text = translation.text

        blob = TextBlob(trans_text)

        polarity = round(blob.sentiment.polarity, 2)
        subjectivity = round(blob.sentiment.subjectivity, 2)

        # -------------------------------------------------
        # MÉTRICAS
        # -------------------------------------------------

        st.markdown(
            '<div class="resultado">',
            unsafe_allow_html=True
        )

        st.markdown("### 📊 Resultado del análisis")

        st.markdown(
            f"""
            <div class="metricas">

                <div class="metrica">
                    <div class="metrica-titulo">
                        Polaridad
                    </div>

                    <div class="metrica-valor">
                        {polarity}
                    </div>
                </div>

                <div class="metrica">
                    <div class="metrica-titulo">
                        Subjetividad
                    </div>

                    <div class="metrica-valor">
                        {subjectivity}
                    </div>
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

        # -------------------------------------------------
        # SENTIMIENTO POSITIVO
        # -------------------------------------------------

        if polarity > 0.0 and polarity <= 1.0:

            st.markdown(
                '<div class="emocion">💖 Es un sentimiento Positivo</div>',
                unsafe_allow_html=True
            )

            with open('Happy.json') as source:
                animation = json.load(source)

            st_lottie(
                animation,
                width=350,
                key="happy_animation"
            )


        # -------------------------------------------------
        # SENTIMIENTO NEGATIVO
        # -------------------------------------------------

        elif polarity >= -1 and polarity <= 0:

            st.markdown(
                '<div class="emocion">💙 Es un sentimiento Negativo</div>',
                unsafe_allow_html=True
            )

            with open('Sad.json') as source:
                animation = json.load(source)

            st_lottie(
                animation,
                width=350,
                key="sad_animation"
            )

            # -------------------------------------------------
            # VIDEO
            # -------------------------------------------------

            st.markdown("""
            <div class="video-card">

                <div class="video-titulo">
                    🎬 Un pequeño momento para cambiar el ánimo
                </div>

            </div>
            """, unsafe_allow_html=True)

            st.video(
                "https://youtu.be/Ch6xdV_ZjdU?si=CVmBBc11GpeAXCMp"
            )


        # -------------------------------------------------
        # SENTIMIENTO NEUTRAL
        # -------------------------------------------------

        else:

            st.markdown(
                '<div class="emocion">🤍 Es un sentimiento Neutral</div>',
                unsafe_allow_html=True
            )

            with open('Neutral.json') as source:
                animation = json.load(source)

            st_lottie(
                animation,
                width=350,
                key="neutral_animation"
            )

        st.markdown(
            '</div>',
            unsafe_allow_html=True
        )


# ---------------------------------------------------------
# PIE DE PÁGINA
# ---------------------------------------------------------

st.markdown("---")

st.markdown(
    """
    <p style="text-align:center; color:#aaa;">
        💜 Explora tus emociones a través de las palabras
    </p>
    """,
    unsafe_allow_html=True
)


