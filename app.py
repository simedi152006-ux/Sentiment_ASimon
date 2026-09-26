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
    page_icon="💭",
    layout="centered"
)


# ---------------------------------------------------------
# ESTILOS
# ---------------------------------------------------------

st.markdown("""
<style>

    /* Fondo */
    .stApp {
        background:
            radial-gradient(circle at 10% 10%, rgba(255, 105, 180, 0.20), transparent 30%),
            radial-gradient(circle at 90% 20%, rgba(100, 149, 237, 0.20), transparent 30%),
            radial-gradient(circle at 50% 90%, rgba(138, 43, 226, 0.18), transparent 35%),
            #100c1c;
        color: white;
    }


    /* Contenedor */
    .main .block-container {
        max-width: 850px;
        padding-top: 3rem;
        padding-bottom: 4rem;
    }


    /* TÍTULO PRINCIPAL */
    .titulo {
        text-align: center;
        font-size: 3.2rem;
        font-weight: 800;
        margin-bottom: 0.2rem;

        color: #FFF1B8;

        text-shadow:
            0 0 10px rgba(255, 241, 184, 0.25);
    }


    /* Subtítulo */
    .subtitulo {
        text-align: center;
        color: #d8cfe5;
        font-size: 1.15rem;
        margin-bottom: 2rem;
    }


    /* Imagen */
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


    /* Resultado */
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

        box-shadow: 0 12px 35px rgba(0,0,0,0.3);
    }


    /* Título de resultados */
    .titulo-resultado {
        text-align: center;
        color: #FFF1B8;
        font-size: 1.4rem;
        font-weight: 700;
        margin-bottom: 20px;
    }


    /* Métricas */
    div[data-testid="stMetric"] {

        background: rgba(255,255,255,0.08);

        border: 1px solid rgba(255,255,255,0.12);

        border-radius: 18px;

        padding: 15px;

        text-align: center;

        box-shadow: 0 5px 20px rgba(0,0,0,0.15);
    }


    div[data-testid="stMetricLabel"] {
        color: #cfc3da !important;
    }


    div[data-testid="stMetricValue"] {
        color: #FFF1B8 !important;
    }


    /* Resultado emocional */
    .emocion {
        text-align: center;

        font-size: 1.8rem;

        font-weight: 700;

        margin-top: 25px;

        color: #ffffff;
    }


    /* VIDEO */
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

        color: #FFF1B8;

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

        color: #FFF1B8;
    }


    section[data-testid="stSidebar"] p {

        color: #d8cfe5;

        line-height: 1.5;
    }


    /* Campo de texto */
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


    /* Separadores */
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

st.markdown(
    '<div class="imagen-principal">',
    unsafe_allow_html=True
)

st.image(
    image,
    width=650
)

st.markdown(
    '</div>',
    unsafe_allow_html=True
)


# ---------------------------------------------------------
# INTRODUCCIÓN
# ---------------------------------------------------------

st.markdown("""
<div class="card">

<h3 style="text-align:center; color:#FFF1B8;">
✨ ¿Cómo funciona?
</h3>

<p style="text-align:center;">
Escribe una frase y descubre si expresa un sentimiento
<b>positivo, negativo o neutral</b>.
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
        **Polaridad:** indica si el sentimiento es positivo,
        negativo o neutral.

        **-1** negativo · **0** neutral · **1** positivo
        """
    )

    st.write(
        """
        **Subjetividad:** indica cuánto expresa opiniones
        o emociones.

        **0** objetivo · **1** subjetivo
        """
    )

    st.divider()

    st.caption("Python · TextBlob · Streamlit")


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

        polarity = round(
            blob.sentiment.polarity,
            2
        )

        subjectivity = round(
            blob.sentiment.subjectivity,
            2
        )


        # -------------------------------------------------
        # RESULTADOS
        # -------------------------------------------------

        st.markdown(
            '<div class="resultado">',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="titulo-resultado">📊 Resultado del análisis</div>',
            unsafe_allow_html=True
        )


        # Métricas con Streamlit
        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                label="🎯 Polaridad",
                value=polarity
            )

        with col2:

            st.metric(
                label="💭 Subjetividad",
                value=subjectivity
            )


        # -------------------------------------------------
        # POSITIVO
        # -------------------------------------------------

        if polarity > 0:

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
        # NEGATIVO
        # -------------------------------------------------

        elif polarity < 0:

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


            # VIDEO

            st.markdown(
                """
                <div class="video-card">

                    <div class="video-titulo">
                        🎬 Un pequeño momento para cambiar el ánimo
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )

            st.video(
                "https://youtu.be/Ch6xdV_ZjdU?si=CVmBBc11GpeAXCMp"
            )


        # -------------------------------------------------
        # NEUTRAL
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
    <p style="
        text-align:center;
        color:#aaa;
        margin-top:20px;
    ">
        💜 Explora tus emociones a través de las palabras
    </p>
    """,
    unsafe_allow_html=True
)
