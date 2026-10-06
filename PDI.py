# =================================================================
# == INSTITUTO TECNOLOGICO Y DE ESTUDIOS SUPERIORES DE OCCIDENTE ==
# == ITESO, UNIVERSIDAD JESUITA DE GUADALAJARA                   ==
# ==                                                             ==
# == LABORATORIO DE DESARROLLO DE SOLUCIONES TECNOLÓGICAS        ==
# == Análisis Multimedia basado en Inteligencia Artificial para  ==
# == Soluciones Operativas Empresariales                         ==
# ==                                                             ==
# == TEMA 3                                                      ==
# == Procesamiento Digital de Imágenes empleando OpenCV          ==
# =================================================================


#----- Importación de Librerías -----------------------------------
import io
import cv2
import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from PIL import Image


# -----------------------------------------------------------------
# Configuración general de la página
# -----------------------------------------------------------------
st.set_page_config(
    page_title="Laboratorio de Desarrollo de Soluciones Tecnológicas",
    page_icon="💻",
    layout="wide",
    initial_sidebar_state="expanded")


# -----------------------------------------------------------------
# Configuración CSS (Cascading Style Sheet) - Estilo del Dashboard
# -----------------------------------------------------------------
st.markdown(
    """
    <style>
        .main { background-color: #FAFAFA; }
        h1, h2, h3 { font-weight: 600; color: #1F2933; }
        .stTabs [data-baseweb="tab-list"] { gap: 4px; }
        .stTabs [data-baseweb="tab"] {
            background-color: #F0F2F6;
            border-radius: 8px 8px 0 0;
            padding: 8px 16px;}
        section[data-testid="stSidebar"] {
            background-color: #F4F6F8;
            border-right: 1px solid #E0E0E0;}
        .footer-curso {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            background-color: #9DB6DA;
            border-top: 1px solid #E0E0E0;
            padding: 6px 24px;
            font-size: 0.88rem;
            color: #1A365D;
            text-align: center;
            z-index: 999;}
        .block-container { padding-bottom: 3.5rem;}
    </style>
    """, unsafe_allow_html=True)


# -----------------------------------------------------------------
# Encabezado del Dashboard
# -----------------------------------------------------------------
#----- Lectura y Renderizado del Logotipo -------------------------
Logo = Image.open("./Imagenes/Logo.png").convert("RGB")
st.image(Logo, width=700)

#----- Renderizado del Texto --------------------------------------
st.title("💻 Laboratorio de Desarrollo de Soluciones Tecnológicas ⚙️")
st.subheader(":blue[Operaciones Básicas del Procesamiento Digital de Imágenes en Streamlit]")
st.caption("🌎️ **Ingenierías ITESO - Departamento de Electrónica, Sistemas e Informática (DESI)**")

tab_imrgb, tab_multi, tab_imsar, tab_class, tab_info = st.tabs(
    ["🖼️ Operaciones Básicas RGB",
     "️🛰️ Imágenes Multiespectrales",
     "📡 Imágenes SAR",
     "😃 Clasificador de Rostros",
     "ℹ️ Acerca del Dashboard"])


# ===================================================================
# TABULACIÓN NÚMERO 1 — OPERACIONES BÁSICAS RGB
# ===================================================================
with (tab_imrgb):
    espcol = "Escala de Grises"
    col_ctrl, col_image = st.columns([1, 2.3], gap="large")

    with col_ctrl:
        st.subheader("Operaciones Básicas")

        operacion = st.selectbox(
            "Selecciona el tipo de Operación:",
            ["Mostrar Bandas de la Imagen RGB",
             "Conversiones entre Espacios de Color",
             "Operación de Reflejo",
             "Operación de Rotación",
             "Operación de Reescalamiento",
             "Operación de Umbralización",
             "Detectores de Bordes"], index=0, key="SB1")

        if operacion == "Mostrar Bandas de la Imagen RGB":
            sub_ctrl1, sub_ctrl2 = st.columns([0.3, 5])
            with sub_ctrl2:
                banda = st.radio(
                    "Selecciona la Banda:",
                    options=["Banda Roja (R)", "Banda Verde (G)", "Banda Azul (B)"], index=0)

        if operacion == "Conversiones entre Espacios de Color":
            sub_ctrl1, sub_ctrl2 = st.columns([0.3, 5])
            with sub_ctrl2:
                espcol = st.radio(
                    "Selecciona el Espacio de Color:",
                    options=["Escala de Grises",
                             "BGR (Blue-Green-Red)",
                             "HSV (Hue, Saturation, Value)",
                             "CMYK (Cyan, Magenta, Yellow, Black)",
                             "LAB (Light, GtoR, BtoY)",
                             "YCrCb (Luminance, Chrominance)"], index=0)

        if operacion == "Operación de Reflejo":
            sub_ctrl1, sub_ctrl2 = st.columns([0.3, 5])
            with sub_ctrl2:
                flip = st.radio(
                    "Selecciona el tipo de Reflejo (Flip):",
                    options=["Reflejo Horizontal", "Reflejo Vertical"],  index=0)

        if operacion == "Operación de Rotación":
            sub_ctrl1, sub_ctrl2 = st.columns([0.3, 5])
            with sub_ctrl2:
                ang_rot = st.number_input("Ángulo de Rotación:", min_value=-360, max_value=360, value=0)
                op_cen = st.toggle("Emplear el Centro de la Imagen como Pivote", value=True)
                if op_cen:
                    pass
                else:
                    st.write("Valores del Pixel Pivote:")
                    ren_rot = st.number_input("Pixel en el Renglón:", min_value=1, max_value=256, value=1, step=1) - 1
                    col_rot = st.number_input("Pixel en la Columna:", min_value=1, max_value=256, value=1, step=1) - 1

        if operacion == "Operación de Reescalamiento":
            sub_ctrl1, sub_ctrl2 = st.columns([0.3, 5])
            with sub_ctrl2:
                escala = st.number_input("Porcentaje de Reescalamiento:", min_value=0, max_value=10000,
                                         step=10, value=100)
                suaviza = st.toggle("Aplicar Suavizado al Reescalamiento", value=False)
                if suaviza:
                    wide_g = st.number_input("Valor del Nivel de Suavizado:", min_value=0, max_value=20,
                                             value=12, step=2)

        if operacion == "Operación de Umbralización":
            sub_ctrl1, sub_ctrl2 = st.columns([0.3, 5])
            with sub_ctrl2:
                umbral = st.number_input("Valor del Umbral:", min_value=0, max_value=255, step=1, value=120)

        if operacion == "Detectores de Bordes":
            sub_ctrl1, sub_ctrl2 = st.columns([0.3, 5])
            with sub_ctrl2:
                tipo_bor = st.radio(
                    "Selecciona el Modelo de Detección de Bordes:",
                    options=["Detector de Bordes de Sobel",
                             "Detector de Bordes de Canny"], index=0)
                if tipo_bor == "Detector de Bordes de Sobel":
                    nucleo = st.select_slider("Valor del Núcleo de Sobel:",
                                              options=[1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25],
                                              value=21)
                    sob_X = st.checkbox("Eje X", value=True, key='check1')
                    sob_Y = st.checkbox("Eje Y", value=False, key='check2')
                elif tipo_bor == "Detector de Bordes de Canny":
                    can_umb = st.number_input("Valor del Umbral de Canny:", min_value=0, max_value=255,
                                              step=1, value=80)

        st.divider()

        st.subheader("Imagen de Entrada")
        archivo = st.file_uploader("Sube una Imagen", type=["png", "jpg", "jpeg", "bmp"], key='C1')
        usar_ejemplo = st.checkbox("Usar imagen de ejemplo", value=archivo is None, key='C2')

    # --- Carga de imagen ---
    if archivo is not None and not usar_ejemplo:
        img = np.array(Image.open(archivo).convert("RGB"))
        imgR = img[:, :, 0]
        imgG = img[:, :, 1]
        imgB = img[:, :, 2]
    elif usar_ejemplo:
        img = cv2.cvtColor(cv2.imread("./Imagenes/Lily.jpg"), cv2.COLOR_BGR2RGB)
        imgR = img[:, :, 0]
        imgG = img[:, :, 1]
        imgB = img[:, :, 2]
    else:
        img = None

    with col_image:
        if img is None:
            st.info("Sube una imagen o activa la casilla de imagen de ejemplo para comenzar.")
        else:

            if operacion == "Mostrar Bandas de la Imagen RGB":
                if banda == "Banda Roja (R)":
                    im_res = imgR
                    etiqueta = "**Banda Roja (R) de la Imagen:**"
                    etiqueta_save = "Imagen_BandaR"
                if banda == "Banda Verde (G)":
                    im_res = imgG
                    etiqueta = "**Banda Verde (G) de la Imagen:**"
                    etiqueta_save = "Imagen_BandaG"
                if banda == "Banda Azul (B)":
                    im_res = imgB
                    etiqueta = "**Banda Azul (B) de la Imagen:**"
                    etiqueta_save = "Imagen_BandaB"

            if operacion == "Conversiones entre Espacios de Color":
                if espcol == "BGR (Blue-Green-Red)":
                    im_res = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
                    etiqueta = "**Mapa de Color BGR de la Imagen:**"
                    etiqueta_save = "Imagen_BGR"
                    bgr1, bgr2, bgr3 = st.columns(3)
                    with bgr1:
                        st.markdown("**Canal Azul (B):**")
                        st.image(im_res[:, :, 0], width=300)
                    with bgr2:
                        st.markdown("**Canal Verde (G):**")
                        st.image(im_res[:, :, 1], width=300)
                    with bgr3:
                        st.markdown("**Canal Rojo (R):**")
                        st.image(im_res[:, :, 2], width=300)
                if espcol == "Escala de Grises":
                    im_res = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
                    etiqueta = "**Escala de Grises de la Imagen:**"
                    etiqueta_save = "Imagen_GRAY"
                if espcol == "HSV (Hue, Saturation, Value)":
                    im_res = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
                    etiqueta = "**Mapa de Color HSV de la Imagen:**"
                    etiqueta_save = "Imagen_HSV"
                    hsv1, hsv2, hsv3 = st.columns(3)
                    with hsv1:
                        st.markdown("**Canal de Tono (H):**")
                        st.image(im_res[:, :, 0], width=300)
                    with hsv2:
                        st.markdown("**Canal de Saturación (S):**")
                        st.image(im_res[:, :, 1], width=300)
                    with hsv3:
                        st.markdown("**Canal de Luminosidad (V):**")
                        st.image(im_res[:, :, 2], width=300)
                if espcol == "CMYK (Cyan, Magenta, Yellow, Black)":
                    im_res = Image.fromarray(img).convert('CMYK')
                    im_size = np.asarray(Image.fromarray(img).convert('CMYK'))
                    etiqueta = "**Mapa de Color CMYK de la Imagen:**"
                    etiqueta_save = "Imagen_CMYK"
                    cmyk1, cmyk2, cmyk3, cmyk4 = st.columns(4)
                    with cmyk1:
                        st.markdown("**Canal Cyan (C):**")
                        st.image(im_size[:, :, 0], width=250)
                    with cmyk2:
                        st.markdown("**Canal Magenta (M):**")
                        st.image(im_size[:, :, 1], width=250)
                    with cmyk3:
                        st.markdown("**Canal Amarillo (Y):**")
                        st.image(im_size[:, :, 2], width=250)
                    with cmyk4:
                        st.markdown("**Canal Negro (K):**")
                        st.image(im_size[:, :, 3], width=250)
                if espcol == "LAB (Light, GtoR, BtoY)":
                    im_res = cv2.cvtColor(img, cv2.COLOR_RGB2LAB)
                    etiqueta = "**Mapa de Color LAB de la Imagen:**"
                    etiqueta_save = "Imagen_LAB"
                    lab1, lab2, lab3 = st.columns(3)
                    with lab1:
                        st.markdown("**Canal de Luminosidad (L):**")
                        st.image(im_res[:, :, 0], width=300)
                    with lab2:
                        st.markdown("**Canal de Cromaticidad Verde a Rojo (A):**")
                        st.image(im_res[:, :, 1], width=300)
                    with lab3:
                        st.markdown("**Canal de Cromaticidad Azul a Amarillo (B):**")
                        st.image(im_res[:, :, 2], width=300)
                if espcol == "YCrCb (Luminance, Chrominance)":
                    im_res = cv2.cvtColor(img, cv2.COLOR_RGB2YCrCb)
                    etiqueta = "**Mapa de Color YCrCb de la Imagen:**"
                    etiqueta_save = "Imagen_YCrCb"
                    ycc1, ycc2, ycc3 = st.columns(3)
                    with ycc1:
                        st.markdown("**Canal de Luminancia (Y):**")
                        st.image(im_res[:, :, 0], width=300)
                    with ycc2:
                        st.markdown("**Canal de Crominancia al Rojo (Cr):**")
                        st.image(im_res[:, :, 1], width=300)
                    with ycc3:
                        st.markdown("**Canal de Crominancia al Azul (Cb):**")
                        st.image(im_res[:, :, 2], width=300)

            if operacion == "Operación de Reflejo":
                if flip == "Reflejo Horizontal":
                    im_res = cv2.flip(img, 1)
                    etiqueta = "**Reflejo Horizontal de la Imagen:**"
                    etiqueta_save = "Imagen_FlipH"
                if flip == "Reflejo Vertical":
                    im_res = cv2.flip(img, 0)
                    etiqueta = "**Reflejo Vertical de la Imagen:**"
                    etiqueta_save = "Imagen_FlipV"

            if operacion == "Operación de Rotación":
                def RotarImagen(imagen,
                                angulo,
                                p_base):
                    mat_rot = cv2.getRotationMatrix2D(p_base, angulo, scale=1.0)
                    return cv2.warpAffine(src=imagen, M=mat_rot, dsize=imagen.shape[0:2], flags=cv2.INTER_LINEAR)
                if op_cen:
                    centro = tuple(np.array(img.shape[0:2])/2)
                    etique = "Rotación de la Imagen a " + str(ang_rot) + " Grados Respecto al Centro:"
                    etiqueta = f"**{etique}**"
                else:
                    centro = (ren_rot, col_rot)
                    etique = "Rotación de la Imagen a " + str(ang_rot) + " Grados Respecto al Pixel (" + str(
                        ren_rot+1) + ", " + str(col_rot+1) + "):"
                    etiqueta = f"**{etique}**"
                im_res = RotarImagen(img, ang_rot, centro)
                etiqueta_save = "Imagen_Rot"

            if operacion == "Operación de Reescalamiento":
                def Reescalar(imagen, escala):
                    ancho = int(imagen.shape[1] * escala / 100)
                    alto = int(imagen.shape[0] * escala / 100)
                    dim = (ancho, alto)
                    return cv2.resize(imagen, dim, interpolation=cv2.INTER_AREA)
                im_reescaled = Reescalar(img, escala)
                if suaviza:
                    d = wide_g
                    im_res = cv2.GaussianBlur(im_reescaled, (2 * d + 1, 2 * d + 1), -1)[d:-d, d:-d]
                    etique = "Reescalado de la Imagen al " + str(escala) + "% con Suavizado:"
                    etiqueta = f"**{etique}**"
                else:
                    im_res = im_reescaled
                    etique = "Reescalado de la Imagen al " + str(escala) + "% sin Suavizado:"
                    etiqueta = f"**{etique}**"
                etiqueta_save = "Imagen_Res"

            if operacion == "Operación de Umbralización":
                im_GS = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
                ret, im_res = cv2.threshold(im_GS, umbral, 255, 0)
                etique = "Umbralización de la Imagen con Valor de " + str(umbral) + ":"
                etiqueta = f"**{etique}**"
                etiqueta_save = "Imagen_Umb"

            if operacion == "Detectores de Bordes":
                if tipo_bor == "Detector de Bordes de Sobel":
                    im_GS = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
                    if sob_X and sob_Y is False:
                        im_sob = cv2.Sobel(im_GS, cv2.CV_64F, 1, 0, ksize=nucleo)
                        etique = "Detector de Bordes de Sobel en X con Núcleo de " + str(nucleo) + ":"
                        etiqueta_save = "Imagen_SobX"
                    elif sob_Y and sob_X is False:
                        im_sob = cv2.Sobel(im_GS, cv2.CV_64F, 0, 1, ksize=nucleo)
                        etique = "Detector de Bordes de Sobel en Y con Núcleo de " + str(nucleo) + ":"
                        etiqueta_save = "Imagen_SobY"
                    elif sob_X and sob_Y:
                        im_sob = cv2.Sobel(im_GS, cv2.CV_64F, 1, 1, ksize=nucleo)
                        etique = "Detector de Bordes de Sobel en X y Y con Núcleo de " + str(nucleo) + ":"
                        etiqueta_save = "Imagen_SobXY"
                    else:
                        st.info("¡ERROR!")
                        im_sob = im_GS
                        etique = "Selecciona alguno de los Ejes para aplicar el Detector de Bordes de Sobel."
                        etiqueta_save = "Imagen_GRAY"
                    img_ressob = cv2.resize(im_sob, (img.shape[0], img.shape[1]))
                    im_normsob = cv2.normalize(im_sob, img_ressob, 0, 255, cv2.NORM_MINMAX)
                    im_res = im_normsob.astype(np.uint8)
                    etiqueta = f"**{etique}**"
                elif tipo_bor == "Detector de Bordes de Canny":
                    im_res = cv2.Canny(img, can_umb, (2.5 * can_umb))
                    etique = "Detector de Bordes de Canny con Umbral de " + str(can_umb) + ":"
                    etiqueta = f"**{etique}**"
                    etiqueta_save = "Imagen_Can"

            c1, c2 = st.columns(2)
            with c1:
                st.markdown("**Imagen Original:**")
                st.image(img, width=500)
                st.write("Tamaño de la Imagen:", img.shape)
            with c2:
                st.markdown(etiqueta)
                st.image(im_res, width=500)
                if espcol == "CMYK (Cyan, Magenta, Yellow, Black)":
                    st.write("Tamaño de la Imagen:", im_size.shape)
                    # Guardar Imagen
                    pil_image = im_res
                    buffer = io.BytesIO()
                    pil_image.save(buffer, format="TIFF")
                    buffer_bytes = buffer.getvalue()
                    st.download_button(
                        label="Descargar Imagen",
                        data=buffer_bytes,
                        file_name=etiqueta_save + ".tiff",
                        mime="image/tiff",
                        icon="💾",
                        key='C3')
                else:
                    st.write("Tamaño de la Imagen:", im_res.shape)
                    # Guardar Imagen
                    pil_image = Image.fromarray(im_res)
                    buffer = io.BytesIO()
                    pil_image.save(buffer, format="PNG")
                    buffer_bytes = buffer.getvalue()
                    st.download_button(
                        label="Descargar Imagen",
                        data=buffer_bytes,
                        file_name=etiqueta_save + ".png",
                        mime="image/png",
                        icon="💾",
                        key='C4')


# ===================================================================
# TABULACIÓN NÚMERO 2 — IMÁGENES MULTIESPECTRALES
# ===================================================================
with (tab_multi):
    etiqueta1 = etiqueta2 = ""
    col_ctrl, col_image = st.columns([1, 2.3], gap="large")

    with col_ctrl:
        st.subheader("Imágenes Multiespectrales")
        escena = st.radio(
            "Selecciona la Escena:",
            options=["Zona Metropolitana de Guadalajara - Escena 1",
                     "Zona Metropolitana de Guadalajara - Escena 2",
                     "Zona Metropolitana de Guadalajara - Escena 3",
                     "Zona Metropolitana de Guadalajara - Escena 4"], index=0, key="R1")

        if escena == "Zona Metropolitana de Guadalajara - Escena 1":
            #img_mul = cv2.imread("./SPOT5/GDL01.tiff", cv2.IMREAD_UNCHANGED)
            img_mul = np.asarray(cv2.imread("./SPOT5/GDL01.tiff", cv2.IMREAD_UNCHANGED), dtype=np.uint8)
            img_jpg = cv2.cvtColor(cv2.imread("./SPOT5/GDL01.jpg"), cv2.COLOR_BGR2RGB)
        elif escena == "Zona Metropolitana de Guadalajara - Escena 2":
            img_mul = cv2.imread("./SPOT5/GDL02.tiff", cv2.IMREAD_UNCHANGED)
            img_jpg = cv2.cvtColor(cv2.imread("./SPOT5/GDL02.jpg"), cv2.COLOR_BGR2RGB)
        elif escena == "Zona Metropolitana de Guadalajara - Escena 3":
            img_mul = cv2.imread("./SPOT5/GDL03.tiff", cv2.IMREAD_UNCHANGED)
            img_jpg = cv2.cvtColor(cv2.imread("./SPOT5/GDL03.jpg"), cv2.COLOR_BGR2RGB)
        elif escena == "Zona Metropolitana de Guadalajara - Escena 4":
            img_mul = cv2.imread("./SPOT5/GDL04.tiff", cv2.IMREAD_UNCHANGED)
            img_jpg = cv2.cvtColor(cv2.imread("./SPOT5/GDL04.jpg"), cv2.COLOR_BGR2RGB)
        img_res1 = img_jpg
        img_res2 = img_mul
        st.divider()

        operacion = st.selectbox(
            "Selecciona el tipo de Operación:",
            ["Mostrar Bandas de la Imagen Multiespectral",
             "Combinar 3 Bandas a Color Verdadero",
             "Cálculo del Índice NDVI",
             "Segmentación por Umbral"], index=0, key="SB2")

        if operacion == "Mostrar Bandas de la Imagen Multiespectral":
            pass
        elif operacion == "Combinar 3 Bandas a Color Verdadero":
            sub_ctrl1, sub_ctrl2 = st.columns([0.3, 5])
            with sub_ctrl2:
                combina = st.multiselect("Selecciona las 3 Bandas a Combinar:",
                                         ["Banda XS1: Verde (Green)",
                                          "Banda XS2: Rojo (Red)",
                                          "Banda XS3: Infrarrojo Cercano (NIR)",
                                          "SWIR: Infrarrojo de Onda Corta (SWIR)"],
                                         default=["Banda XS1: Verde (Green)", "Banda XS2: Rojo (Red)",
                                                  "Banda XS3: Infrarrojo Cercano (NIR)"], max_selections=3, key="Mu1")
        elif operacion == "Cálculo del Índice NDVI":
            pass
        elif operacion == "Segmentación por Umbral":
            sub_ctrl1, sub_ctrl2, sub_ctrl3 = st.columns([0.3, 5, 5])
            with sub_ctrl2:
                mul_umb = st.number_input("Valor del Umbral (0 a 1):", min_value=0.0, max_value=1.0, value=0.3)
            with sub_ctrl3:
                mul_pix = st.number_input("Vecindario del Pixel (0 a 1):", min_value=0.0, max_value=1.0, value=1.0)

    with col_image:
        if img_mul is None:
            st.warning("La imagen cargada no tiene 4 canales de banda (XS1, XS2, XS3, SWIR).")
        if operacion == "Mostrar Bandas de la Imagen Multiespectral":
            XS1, XS2, XS3, SWIR = cv2.split(img_mul)
            ba_xs1, ba_xs2, ba_xs3, ba_xs4 = st.columns(4)
            with ba_xs1:
                st.markdown("**Banda XS1: Verde (Green):**")
                st.image(XS1, width=250)
            with ba_xs2:
                st.markdown("**Banda XS2: Rojo (Red):**")
                st.image(XS2, width=250)
            with ba_xs3:
                st.markdown("**Banda XS3: Infrarrojo Cercano (NIR):**")
                st.image(XS3, width=250)
            with ba_xs4:
                st.markdown("**SWIR: Infrarrojo de Onda Corta (SWIR):**")
                st.image(SWIR, width=250)
            img_res1 = img_jpg
            img_res2 = img_mul
            etique1 = "Imagen Multiespectral en Color Verdadero (3 Bandas):"
            etique2 = "Imagen Multiespectral en Color Falso (4 Bandas):"
            etiqueta1 = f"**{etique1}**"
            etiqueta2 = f"**{etique2}**"

        if operacion == "Combinar 3 Bandas a Color Verdadero":
            list_cort = combina.copy()
            for i, n in enumerate(combina):
                if n == "Banda XS1: Verde (Green)":
                    list_cort[i] = "XS1"
                if n == "Banda XS2: Rojo (Red)":
                    list_cort[i] = "XS2"
                if n == "Banda XS3: Infrarrojo Cercano (NIR)":
                    list_cort[i] = "XS3"
                if n == "SWIR: Infrarrojo de Onda Corta (SWIR)":
                    list_cort[i] = "SWIR"
            if len(combina) == 3:
                list_comb = []
                img_comb = np.zeros((img_mul.shape[0], img_mul.shape[1], 3))
                XS1, XS2, XS3, SWIR = cv2.split(img_mul)
                if "Banda XS1: Verde (Green)" in combina:
                    list_comb.append(XS1)
                if "Banda XS2: Rojo (Red)" in combina:
                    list_comb.append(XS2)
                if "Banda XS3: Infrarrojo Cercano (NIR)" in combina:
                    list_comb.append(XS3)
                if "SWIR: Infrarrojo de Onda Corta (SWIR)" in combina:
                    list_comb.append(SWIR)
                img_comb[:, :, 0] = list_comb[0]
                img_comb[:, :, 1] = list_comb[1]
                img_comb[:, :, 2] = list_comb[2]
                img_res2 = img_comb.astype(np.uint8)
                img_res1 = img_jpg
                etique1 = "Imagen Multiespectral en Color Verdadero (3 Bandas):"
                etique2 = "Imagen con Bandas: " + list_cort[0] + ", " + list_cort[1] + ", " + list_cort[2] + ":"
                etiqueta1 = f"**{etique1}**"
                etiqueta2 = f"**{etique2}**"
                etiqueta_save = "Multi_Comb_3Ban"
            if len(combina) != 3:
                img_res2 = img_jpg
                etique1 = "Imagen Multiespectral en Color Verdadero (3 Bandas):"
                etique2 = "Seleccionando Bandas..."
                etiqueta1 = f"**{etique1}**"
                etiqueta2 = f"**{etique2}**"
                etiqueta_save = "Multi_Comb_3Ban"

        if operacion == "Cálculo del Índice NDVI":
            XS1, XS2, XS3, SWIR = cv2.split(img_mul)
            nir = XS3.astype(np.float32)
            red = XS2.astype(np.float32)
            denominador = nir + red
            denominador[denominador == 0] = 0.00001
            ndvi = (nir - red) / denominador
            ndvi_visual = cv2.normalize(ndvi, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
            ndvi_coloreado = cv2.applyColorMap(ndvi_visual, cv2.COLORMAP_JET)
            img_res1 = ndvi_visual
            img_res2 = ndvi_coloreado
            etique1 = "Índice de Vegetación de Diferencia Normalizada (NDVI) Visual:"
            etique2 = "Índice de Vegetación de Diferencia Normalizada (NDVI) Coloreado:"
            etiqueta1 = f"**{etique1}**"
            etiqueta2 = f"**{etique2}**"
            etiqueta_save = "Multi_NDVI_Col"
            etiqueta_save1 = "Multi_NDVI_Vis"

        if operacion == "Segmentación por Umbral":
            XS1, XS2, XS3, SWIR = cv2.split(img_mul)
            nir = XS3.astype(np.float32)
            red = XS2.astype(np.float32)
            denominador = nir + red
            denominador[denominador == 0] = 0.00001
            ndvi = (nir - red) / denominador
            _, mascara_vegetacion = cv2.threshold(ndvi, mul_umb, mul_pix, cv2.THRESH_BINARY)
            img_rees = mascara_vegetacion[:, :] * 255
            img_res2 = img_rees.astype(np.uint8)
            img_res1 = img_jpg
            etique1 = "Imagen Multiespectral en Color Verdadero (3 Bandas):"
            etique2 = "Segmentación por Umbral:"
            etiqueta1 = f"**{etique1}**"
            etiqueta2 = f"**{etique2}**"
            etiqueta_save = "Multi_Umbral"

        c1, c2 = st.columns(2)
        with c1:
            st.markdown(etiqueta1)
            st.image(img_res1, width=500)
            st.write("Tamaño de la Imagen:", img_res1.shape)
            if operacion == "Cálculo del Índice NDVI":
                #Guardar Imagen
                pil_image = Image.fromarray(img_res1)
                buffer = io.BytesIO()
                pil_image.save(buffer, format="PNG")
                buffer_bytes = buffer.getvalue()
                st.download_button(
                    label="Descargar Imagen",
                    data=buffer_bytes,
                    file_name=etiqueta_save1 + ".png",
                    mime="image/png",
                    icon="💾",
                    key='C5')
        with c2:
            st.markdown(etiqueta2)
            st.image(img_res2, width=500)
            st.write("Tamaño de la Imagen:", img_res2.shape)
            if operacion != "Mostrar Bandas de la Imagen Multiespectral":
                #Guardar Imagen
                pil_image = Image.fromarray(img_res2)
                buffer = io.BytesIO()
                pil_image.save(buffer, format="PNG")
                buffer_bytes = buffer.getvalue()
                st.download_button(
                    label="Descargar Imagen",
                    data=buffer_bytes,
                    file_name=etiqueta_save + ".png",
                    mime="image/png",
                    icon="💾",
                    key='C6')


# ===================================================================
# TABULACIÓN NÚMERO 3 — IMÁGENES DE APERTURA SINTÉTICA (SAR)
# ===================================================================
with (tab_imsar):
    col_ctrl, col_image = st.columns([1, 2.3], gap="large")

    with col_ctrl:
        st.subheader("Imágenes de Apertura Sintética")

        operacion = st.selectbox(
            "Selecciona el tipo de Operación:",
            ["Mostrar la Imagen SAR Original",
             "Reducción de Rudio Speckle",
             "Transformación Logarítmica",
             "Realce de Contraste (CLAHE)",
             "Detección de Bordes",
             "Umbralización Adaptativa"], index=0, key="SB5")

        if operacion == "Mostrar la Imagen SAR Original":
            pass
        if operacion == "Reducción de Rudio Speckle":
            sub_ctrl1, sub_ctrl2, sub_ctrl3 = st.columns([0.3, 5, 5])
            with sub_ctrl2:
                sar_sigmaColor = st.number_input("Sigma en Color/Intensidad (0 a 255):",
                                                 min_value=0, max_value=255, value=75)
            with sub_ctrl3:
                sar_sigmaSpace = st.number_input("Sigma en Coordenadas (0 a 255):",
                                                 min_value=0, max_value=255, value=75)
        elif operacion == "Transformación Logarítmica":
            pass
        elif operacion == "Realce de Contraste (CLAHE)":
            pass
        elif operacion == "Detección de Bordes":
            pass
        elif operacion == "Umbralización Adaptativa":
            pass

    with col_image:
        SAR = cv2.imread("./SAR/SAR.tiff", cv2.IMREAD_UNCHANGED)
        img_float = SAR.astype(np.float32)
        img_norm = cv2.normalize(img_float, None, 0, 255, cv2.NORM_MINMAX)
        img_sar = img_norm.astype(np.uint8)
        img_jpg = cv2.cvtColor(cv2.imread("./SAR/SAR.jpg"), cv2.COLOR_BGR2RGB)

        if operacion == "Mostrar la Imagen SAR Original":
            img_res1 = img_jpg
            img_res2 = img_sar
            etique1 = "Imagen de Apertura Sintética en Color Verdadero (3 Bandas):"
            etique2 = "Imagen de Apertura Sintética Original (Pancromática):"
            etiqueta1 = f"**{etique1}**"
            etiqueta2 = f"**{etique2}**"

        if operacion == "Reducción de Rudio Speckle":
            denoised_median = cv2.medianBlur(img_sar, ksize=5)
            denoised_bilateral = cv2.bilateralFilter(img_sar, d=9, sigmaColor=sar_sigmaColor, sigmaSpace=sar_sigmaSpace)
            img_res1 = denoised_median
            img_res2 = denoised_bilateral
            etique1 = "Filtro Mediana:"
            etique2 = "Filtro Bilateral:"
            etiqueta1 = f"**{etique1}**"
            etiqueta2 = f"**{etique2}**"
            etiqueta_save = "SAR_Bil"
            etiqueta_save1 = "SAR_Med"

        if operacion == "Transformación Logarítmica":
            c = 255 / np.log(1 + np.max(img_float))
            log_transformed = c * (np.log(1 + img_float))
            log_transformed = np.uint8(log_transformed)
            img_res1 = img_sar
            img_res2 = log_transformed
            etique1 = "Imagen de Apertura Sintética Original (Pancromática):"
            etique2 = "Transformación Logarítmica:"
            etiqueta1 = f"**{etique1}**"
            etiqueta2 = f"**{etique2}**"
            etiqueta_save = "SAR_Log"

        if operacion == "Realce de Contraste (CLAHE)":
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
            img_enhanced = clahe.apply(img_sar)
            img_res1 = img_sar
            img_res2 = img_enhanced
            etique1 = "Imagen de Apertura Sintética Original (Pancromática):"
            etique2 = "Realce de Contraste CLAHE (Contrast Limited Adaptive Histogram Equalization):"
            etiqueta1 = f"**{etique1}**"
            etiqueta2 = f"**{etique2}**"
            etiqueta_save = "SAR_CLAHE"

        if operacion == "Detección de Bordes":
            denoised_median = cv2.medianBlur(img_sar, ksize=5)
            edges = cv2.Canny(denoised_median, threshold1=10, threshold2=25)
            img_res1 = img_sar
            img_res2 = edges
            etique1 = "Imagen de Apertura Sintética Original (Pancromática):"
            etique2 = "Detección de Bordes:"
            etiqueta1 = f"**{etique1}**"
            etiqueta2 = f"**{etique2}**"
            etiqueta_save = "SAR_Bordes"

        if operacion == "Umbralización Adaptativa":
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
            img_enhanced = clahe.apply(img_sar)
            _, otsu_thresh = cv2.threshold(img_enhanced, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
            img_res1 = img_sar
            img_res2 = otsu_thresh
            etique1 = "Imagen de Apertura Sintética Original (Pancromática):"
            etique2 = "Umbralización para Detección de Cuerpos de Agua:"
            etiqueta1 = f"**{etique1}**"
            etiqueta2 = f"**{etique2}**"
            etiqueta_save = "SAR_Umbral"

        c1, c2 = st.columns(2)
        with c1:
            st.markdown(etiqueta1)
            st.image(img_res1, width=500)
            st.write("Tamaño de la Imagen:", img_res1.shape)
            if operacion == "Reducción de Rudio Speckle":
                #Guardar Imagen
                pil_image = Image.fromarray(img_res1)
                buffer = io.BytesIO()
                pil_image.save(buffer, format="PNG")
                buffer_bytes = buffer.getvalue()
                st.download_button(
                    label="Descargar Imagen",
                    data=buffer_bytes,
                    file_name=etiqueta_save1 + ".png",
                    mime="image/png",
                    icon="💾",
                    key='C7')
        with c2:
            st.markdown(etiqueta2)
            st.image(img_res2, width=500)
            st.write("Tamaño de la Imagen:", img_res2.shape)
            if operacion != "Mostrar la Imagen SAR Original":
                # Guardar Imagen
                pil_image = Image.fromarray(img_res2)
                buffer = io.BytesIO()
                pil_image.save(buffer, format="PNG")
                buffer_bytes = buffer.getvalue()
                st.download_button(
                    label="Descargar Imagen",
                    data=buffer_bytes,
                    file_name=etiqueta_save + ".png",
                    mime="image/png",
                    icon="💾",
                    key='C8')


# ===================================================================
# TABULACIÓN NÚMERO 4 — CLASIFICADOR DE ROSTROS
# ===================================================================
with (tab_class):
    col_ctrl, col_image = st.columns([1, 2.3], gap="large")

    with col_ctrl:
        st.subheader("Clasificador de Rostros")
        imgrupo = st.radio(
            "Selecciona el Grupo:",
            options=["Grupo 1 de Personas",
                     "Grupo 2 de Personas",
                     "Grupo 3 de Personas"], index=0, key="R5")
        if imgrupo == "Grupo 1 de Personas":
            grupo_rgb = cv2.cvtColor(cv2.imread("./Clasifica/GrupoA.jpg"), cv2.COLOR_BGR2RGB)
            grupo_gra = cv2.cvtColor(grupo_rgb, cv2.COLOR_RGB2GRAY)
        if imgrupo == "Grupo 2 de Personas":
            grupo_rgb = cv2.cvtColor(cv2.imread("./Clasifica/GrupoB.jpg"), cv2.COLOR_BGR2RGB)
            grupo_gra = cv2.cvtColor(grupo_rgb, cv2.COLOR_RGB2GRAY)
        if imgrupo == "Grupo 3 de Personas":
            grupo_rgb = cv2.cvtColor(cv2.imread("./Clasifica/GrupoC.jpg"), cv2.COLOR_BGR2RGB)
            grupo_gra = cv2.cvtColor(grupo_rgb, cv2.COLOR_RGB2GRAY)
        st.divider()

        clasifica = st.radio(
            "Selecciona el Tipo de Clasificación:",
            options=["Mostrar la Imagen de Grupo Original",
                     "Detección de Caras",
                     "Detección de Sonrisas",
                     "Detección de Ojos",
                     "Detección de Caras, Sonrisas y Ojos"], index=0, key="R2")

        if clasifica == "Mostrar la Imagen de Grupo Original":
            pass
        if clasifica == "Detección de Caras":
            sub_ctrl1, sub_ctrl2, sub_ctrl3 = st.columns([0.3, 5, 5])
            with sub_ctrl2:
                scale_c = st.number_input("Valor de la Escala (1 a 2):",
                                          min_value=1.0, max_value=2.0, step=1.0, value=1.3)
            with sub_ctrl3:
                minNe_c = st.number_input("Vecindario del Pixel (1 a 20):",
                                          min_value=1, max_value=20, step=1, value=5)
        if clasifica == "Detección de Sonrisas":
            sub_ctrl1, sub_ctrl2, sub_ctrl3 = st.columns([0.3, 5, 5])
            with sub_ctrl2:
                scale_s = st.number_input("Valor de la Escala (1 a 2):",
                                          min_value=1.0, max_value=2.0, step=1.0, value=1.3)
            with sub_ctrl3:
                minNe_s = st.number_input("Vecindario del Pixel (1 a 20):",
                                          min_value=1, max_value=20, step=1, value=15)
        if clasifica == "Detección de Ojos":
            sub_ctrl1, sub_ctrl2, sub_ctrl3 = st.columns([0.3, 5, 5])
            with sub_ctrl2:
                scale_o = st.number_input("Valor de la Escala (1 a 2):",
                                          min_value=1.0, max_value=2.0, step=1.0, value=1.3)
            with sub_ctrl3:
                minNe_o = st.number_input("Vecindario del Pixel (1 a 20):",
                                          min_value=1, max_value=20, step=1, value=1)
        if clasifica == "Detección de Caras, Sonrisas y Ojos":
            sub_ctrl1, sub_ctrl2, sub_ctrl3 = st.columns([0.3, 5, 5])
            with sub_ctrl2:
                scale_c = st.number_input("Caras: Valor de la Escala (1 a 2):",
                                          min_value=1.0, max_value=2.0, step=1.0, value=1.3)
                scale_s = st.number_input("Sonrisas: Valor de la Escala (1 a 2):",
                                          min_value=1.0, max_value=2.0, step=1.0, value=1.3)
                scale_o = st.number_input("Ojos: Valor de la Escala (1 a 2):",
                                          min_value=1.0, max_value=2.0, step=1.0, value=1.3)
            with sub_ctrl3:
                minNe_c = st.number_input("Caras: Vecindario del Pixel (1 a 20):",
                                          min_value=1, max_value=20, step=1, value=5)
                minNe_s = st.number_input("Sonrisas: Vecindario del Pixel (1 a 20):",
                                          min_value=1, max_value=20, step=1, value=15)
                minNe_o = st.number_input("Ojos: Vecindario del Pixel (1 a 20):",
                                          min_value=1, max_value=20, step=1, value=1)

    with col_image:

        if clasifica == "Mostrar la Imagen de Grupo Original":
            sub_or, sub_or2, sub_or3 = st.columns([0.5, 1, 0.5])
            with sub_or2:
                img_res = grupo_rgb
                st.markdown("Imagen de Grupo Original:")
                st.image(img_res, width=500)
                st.write("Tamaño de la Imagen:", img_res.shape)

        if clasifica == "Detección de Caras":
            Grupo = grupo_rgb.copy()
            modelo_caras = cv2.CascadeClassifier('./Clasifica/Modelos/haarcascade_frontalface_default.xml')
            caras = modelo_caras.detectMultiScale(grupo_gra, scale_c, minNe_c)
            for (x, y, w, h) in caras:
                cv2.rectangle(Grupo, (x, y), (x + w, y + h), (255, 0, 0), 2)
            img_res1 = grupo_rgb
            img_res2 = Grupo
            etique1 = "Imagen de Grupo Original:"
            etique2 = "Detección de Caras:"
            etiqueta1 = f"**{etique1}**"
            etiqueta2 = f"**{etique2}**"
            etiqueta_save = "Class_Caras"

        if clasifica == "Detección de Sonrisas":
            Grupo = grupo_rgb.copy()
            modelo_risas = cv2.CascadeClassifier('./Clasifica/Modelos/haarcascade_smile.xml')
            risas = modelo_risas.detectMultiScale(grupo_gra, scale_s, minNe_s)
            for (x, y, w, h) in risas:
                cv2.rectangle(Grupo, (x, y), (x + w, y + h), (0, 255, 0), 2)
            img_res1 = grupo_rgb
            img_res2 = Grupo
            etique1 = "Imagen de Grupo Original:"
            etique2 = "Detección de Sonrisas:"
            etiqueta1 = f"**{etique1}**"
            etiqueta2 = f"**{etique2}**"
            etiqueta_save = "Class_Sonri"

        if clasifica == "Detección de Ojos":
            Grupo = grupo_rgb.copy()
            modelo_ojos = cv2.CascadeClassifier('./Clasifica/Modelos/haarcascade_eye.xml')
            ojos = modelo_ojos.detectMultiScale(grupo_gra, scale_o, minNe_o)
            for (x, y, w, h) in ojos:
                cv2.rectangle(Grupo, (x, y), (x + w, y + h), (255, 255, 255), 2)
            img_res1 = grupo_rgb
            img_res2 = Grupo
            etique1 = "Imagen de Grupo Original:"
            etique2 = "Detección de Ojos:"
            etiqueta1 = f"**{etique1}**"
            etiqueta2 = f"**{etique2}**"
            etiqueta_save = "Class_Ojos"

        if clasifica == "Detección de Caras, Sonrisas y Ojos":
            modelo_caras = cv2.CascadeClassifier('./Clasifica/Modelos/haarcascade_frontalface_default.xml')
            modelo_risas = cv2.CascadeClassifier('./Clasifica/Modelos/haarcascade_smile.xml')
            modelo_ojos = cv2.CascadeClassifier('./Clasifica/Modelos/haarcascade_eye.xml')

            if imgrupo == "Grupo 1 de Personas":
                Grupo_Clas = cv2.cvtColor(cv2.imread("./Clasifica/GrupoA.jpg"), cv2.COLOR_BGR2RGB)
            if imgrupo == "Grupo 2 de Personas":
                Grupo_Clas = cv2.cvtColor(cv2.imread("./Clasifica/GrupoB.jpg"), cv2.COLOR_BGR2RGB)
            if imgrupo == "Grupo 3 de Personas":
                Grupo_Clas = cv2.cvtColor(cv2.imread("./Clasifica/GrupoC.jpg"), cv2.COLOR_BGR2RGB)
            caras = modelo_caras.detectMultiScale(grupo_gra, scale_c, minNe_c)
            for (x, y, w, h) in caras:
                cv2.rectangle(Grupo_Clas, (x, y), (x + w, y + h), (255, 0, 0), 2)

            if imgrupo == "Grupo 1 de Personas":
                Prueba = cv2.cvtColor(cv2.imread("./Clasifica/GrupoA.jpg"), cv2.COLOR_BGR2RGB)
            if imgrupo == "Grupo 2 de Personas":
                Prueba = cv2.cvtColor(cv2.imread("./Clasifica/GrupoB.jpg"), cv2.COLOR_BGR2RGB)
            if imgrupo == "Grupo 3 de Personas":
                Prueba = cv2.cvtColor(cv2.imread("./Clasifica/GrupoC.jpg"), cv2.COLOR_BGR2RGB)
            risas = modelo_risas.detectMultiScale(grupo_gra, scale_s, minNe_s)
            for (x, y, w, h) in risas:
                cv2.rectangle(Prueba, (x, y), (x + w, y + h), (0, 255, 0), 2)
            for (x, y, w, h) in caras:
                for (x_s, y_s, w_s, h_s) in risas:
                    if ((x <= x_s) and (y <= y_s) and (x + w >= x_s + w_s) and (y + h >= y_s + h_s)):
                        cv2.rectangle(Grupo_Clas, (x_s, y_s), (x_s + w_s, y_s + h_s), (0, 255, 0), 2)

            if imgrupo == "Grupo 1 de Personas":
                Prueba = cv2.cvtColor(cv2.imread("./Clasifica/GrupoA.jpg"), cv2.COLOR_BGR2RGB)
            if imgrupo == "Grupo 2 de Personas":
                Prueba = cv2.cvtColor(cv2.imread("./Clasifica/GrupoB.jpg"), cv2.COLOR_BGR2RGB)
            if imgrupo == "Grupo 3 de Personas":
                Prueba = cv2.cvtColor(cv2.imread("./Clasifica/GrupoC.jpg"), cv2.COLOR_BGR2RGB)
            ojos = modelo_ojos.detectMultiScale(grupo_gra, scale_o, minNe_o)
            for (x, y, w, h) in ojos:
                cv2.rectangle(Prueba, (x, y), (x + w, y + h), (255, 255, 255), 2)
            for (x, y, w, h) in caras:
                for (x_s, y_s, w_s, h_s) in ojos:
                    if ((x <= x_s) and (y <= y_s) and (x + w >= x_s + w_s) and (y + h >= y_s + h_s)):
                        cv2.rectangle(Grupo_Clas, (x_s, y_s), (x_s + w_s, y_s + h_s), (255, 255, 255), 2)

            img_res1 = grupo_rgb
            img_res2 = Grupo_Clas
            etique1 = "Imagen de Grupo Original:"
            etique2 = "Detección de Caras, Sonrisas y Ojos:"
            etiqueta1 = f"**{etique1}**"
            etiqueta2 = f"**{etique2}**"
            etiqueta_save = "Class_Todos"

        if clasifica != "Mostrar la Imagen de Grupo Original":
            c1, c2 = st.columns(2)
            with c1:
                st.markdown(etiqueta1)
                st.image(img_res1, width=500)
                st.write("Tamaño de la Imagen:", img_res1.shape)
            with c2:
                st.markdown(etiqueta2)
                st.image(img_res2, width=500)
                st.write("Tamaño de la Imagen:", img_res2.shape)
                # Guardar Imagen
                pil_image = Image.fromarray(img_res2)
                buffer = io.BytesIO()
                pil_image.save(buffer, format="PNG")
                buffer_bytes = buffer.getvalue()
                st.download_button(
                    label="Descargar Imagen",
                    data=buffer_bytes,
                    file_name=etiqueta_save + ".png",
                    mime="image/png",
                    icon="💾",
                    key='C9')


# ===================================================================
# TABULACIÓN NÚMERO 5 — ACERCA DEL DASHBOARD
# ===================================================================
with tab_info:
    st.subheader("Sobre este Dashboard:")
    Banner = Image.open("./Imagenes/Banner.png").convert("RGB")
    st.image(Banner, width=500)
    st.markdown(
        """
        Este Dashboard muestra el uso de la librería **Streamlit** para el
        procesamiento digital de imágenes empleando la librería **OpenCV**.
        Forma parte de los temas del curso "***Laboratorio de Desarrollo de Soluciones
        Tecnológicas***" que aborda el tema "*Análisis Multimedia basado en 
        Inteligencia Artificial para Soluciones Operativas Empresariales*" 
        para alumnos de las Ingenierías del *Instituto Tecnológico y de
        Estudios Superiores de Occidente (ITESO)*.
        
        **Acerca de OpenCV:**
        Para el procesamiento de imágenes y video en Python se empleará la librería OpenCV.
        OpenCV es una librería para Python cuyo principal uso es en el campo de visión por computadora 
        para la detección de rostros y objetos, especialmente en ámbitos como la fotografía, el análisis 
        de imágenes, el desarrollo y mercadeo de productos, así como en aplicaciones de seguridad.
        OpenCV (Open Source Computer Vision) comenzó como un proyecto de investigación en Intel. 
        Actualmente es la biblioteca de visión por computadora más grande en términos de las funciones 
        con las que cuenta. Contiene implementaciones de más de 2,500 algoritmos y está disponible de 
        forma gratuita para fines comerciales y académicos.
        
        **Operaciones básicas en Imágenes RGB:**
        Se implementan algunas operaciones básicas en imágenes **RGB** empleando la librería **OpenCV**,
        entre ellas están:
        * Mostrar Bandas de la Imagen RGB.
        * Conversiones entre Espacios de Color.
            - Escala de Grises.
            - BGR (Blue-Green-Red).
            - HSV (Hue, Saturation, Value).
            - CMYK (Cyan, Magenta, Yellow, Black).
            - LAB (Light, GtoR, BtoY).
            - YCrCb (Luminance, Chrominance).
        * Operación de Reflejo.
        * Operación de Rotación.
        * Operación de Reescalamiento.
        * Operación de Umbralización.
        * Detectores de Bordes.
            - Sobel.
            - Canny.
        
        **Imágenes Multiespectrales:**
        Las Imágenes Multiespectrales aportan información de los colores presentes en una escena dentro 
        del Espectro Visible (EV), y adicionalmente otras bandas cuyo número no pasa de 9, mayormente del infrarrojo. 
        Algunos autores indican que una imagen debe considerarse como Hiperespectral cuando contiene más de 10 bandas 
        de información, aunque otros aumentan dicho número a 20.
        
        Se analizan 4 escenas que corresponden a una Imagen Multiespectral del Área Metropolitana de Guadalajara. 
        Sus características son:
        * Resolución Espacial: 20 metros (modo espectral Hi).
        * Tamaño de la Imagen: (6000 x 6000 x 4) pixeles.
        * Resolución Espectral: 4 bandas.
        
        Las 4 bandas espectrales de la imagen son:
        * Banda XS3: Infrarrojo Cercano (Near Infrared) en modo multiespectral.
        * Banda XS2: Rojo (Red) en modo multiespectral.
        * Banda XS1: Verde (Green) en modo multiespectral.
        * Banda SWIR: Infrarrojo de Onda Corta (Short-Wave Infrared) en modo multiespectral.
        
        Se realizan las siguientes operaciones empleando **OpenCV**:
        * Mostrar Bandas de la Imagen Multiespectral.
        * Combinación de 3 Bandas a Color Verdadero.
        * Cálculo del Índice de Vegetación de Diferencia Normalizada (NDVI).
        * Segmentación por Umbral.
        
        **Imágenes de Apertura Sintética (SAR):**
        Un sistema SAR (por sus siglas en inglés, Synthetic Aperture Radar o Radar de Apertura Sintética) es una 
        tecnología de percepción remota que utiliza un radar montado en una plataforma en movimiento (como un satélite 
        o un avión) para crear imágenes bidimensionales o tridimensionales de alta resolución de la superficie 
        terrestre. 
        
        En los radares convencionales, para obtener una imagen nítida desde el espacio se necesitaría una antena física 
        gigantesca (de varios kilómetros de largo), lo cual es imposible de enviar al espacio. El sistema SAR resuelve 
        esto mediante un truco matemático y físico:
        * A medida que el satélite avanza en su órbita, va emitiendo miles de pulsos de radar por segundo hacia el 
        suelo.
        * El procesador combina todas las señales reflejadas que el satélite captura a lo largo de su trayectoria. 
        * Al simular (sintetizar) que todas esas lecturas fueron hechas por una sola antena enorme, se obtiene una 
        resolución angular altísima como si el satélite tuviera una antena de kilómetros de tamaño.
        
        Las ventajas principales frente a la fotografía óptica son:
        * Visión todo tiempo (24/7): No depende de la luz del sol; el radar emite su propia energía.
        * Penetración de nubes: Las microondas que emite atraviesan nubes, niebla, humo y lluvia fina sin dispersarse.
        * Sensibilidad a la estructura y humedad: En lugar de capturar color, mide la rugosidad física, la geometría 
        de los objetos y el contenido de agua de la superficie.
        
        Las imágenes SAR suelen ser en escala de grises y representan la fuerza del eco que regresa al satélite:
        * Superficies oscuras (Baja reflexión): Zonas muy lisas como agua en calma o carreteras asfálticas. 
        La onda del radar choca y rebota hacia adelante (como una bola de billar), alejándose del satélite.
        * Superficies brillantes (Alta reflexión): Ciudades, edificios, barcos o zonas montañosas rugosas. 
        La onda choca con esquinas rectangulares o paredes (efecto "doble rebote") y regresa directamente hacia 
        la antena del satélite.
        
        Se realizan las siguientes operaciones empleando **OpenCV**:
        * Mostrar la Imagen SAR Original.
        * Reducción de Rudio Speckle.
        * Transformación Logarítmica.
        * Realce de Contraste CLAHE (Contrast Limited Adaptive Histogram Equalization).
        * Detección de Bordes.
        * Umbralización Adaptativa.
        
        **Clasificador de Rostros:**
        Una de las principales aplicaciones de la visión computacional y del procesamiento de imágenes es la 
        detección de objetos, la cual se puede realizar por medio de la Clasificación en Cascada basada en el modelo 
        HAAR (Haar Wavelet), la cual es una metodología efectiva de detección que fue propuesta por Paul Viola y 
        Michael Jones en un artículo del año 2001. 
        
        La Clasificación en Cascada es una aproximación basada en Aprendizaje Máquina (Machine Learning) donde una 
        función en cascada es entrenada a partir de un banco de imágenes con valores positivos y negativos. 
        Posteriormente se emplea para la detección de objetos en otras imágenes. Para ello, **OpenCV** provee un método 
        de entrenamiento con modelos pre-entrenados.  
        
        Se realizan las siguientes operaciones empleando **OpenCV**:
        * Mostrar la Imagen de Grupo Original.
        * Detección de Caras.
        * Detección de Sonrisas.
        * Detección de Ojos.
        * Detección de Caras, Sonrisas y Ojos.
        
        **Interactividad:** 
        El usuario puede seleccionar las imágenes en formato *RGB*, Multiespetral y de Apertura Sintética para
        realizar las diversas operaciones entre ellas, además de clasificar caras, sonrisas y ojos en fotografías
        de grupos de personas. Varias de las operaciones permiten el guardado de la imagen resultante tras haber
        aplicado los diversos métodos de procesamiento digital de imágenes por medio de la librería **OpenCV**.

        **Contenido:**
        - Procesamiento Digital de Imágenes *RGB* y sus operaciones básicas.
        - Procesamiento Digital de Imágenes Multiespectrales.
        - Procesamiento Digidal de Imágenes de Apertura Sintética (SAR).
        - Clasificador de Rostros.
          
        ***Nota:*** Los temas de cada uno de los contenidos se revisaron a detalle en
        las sesiones del curso haciendo uso de **Jupyter Notebook**.

        **Librerías utilizadas:** `streamlit`, `opencv`, `numpy`, `scipy`, `plotly`,
        `pillow`, `io`.
        
        :blue[**Desarrollado por: Dr. Iván Esteban Villalón Turrubiates.
        Departamento de Electrónica, Sistemas e Informática (DESI).
        *villalon@iteso.mx***]
        """)


# ===================================================================
# PIE DE PÁGINA FIJO CON DATOS DEL CURSO
# ===================================================================
st.markdown(f"""
    <div class="footer-curso">
        💻 Dr. Iván Esteban Villalón Turrubiates · Laboratorio de
        Desarrollo de Soluciones Tecnológicas · ITESO ⚙️
    </div>""", unsafe_allow_html=True)


# ===================================================================
# .: FINAL DEL CÓDIGO :.
# ===================================================================
