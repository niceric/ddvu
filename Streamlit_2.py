# -*- coding: utf-8 -*-

import streamlit as st
import pdfplumber
import logging
import base64      ##bilderna 
from typing import Optional    ##för att texten ska vara sträng eller none 
from streamlit.delta_generator import DeltaGenerator

# Configure logging
logging.basicConfig(level=logging.INFO)

# Konvertera loggan till base64
def get_base64_image(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    return encoded_string

# Centrera rubriken
def display_centered_header(text: str, level: int = 1, container: Optional[DeltaGenerator] = None, bold: bool = False):
    tag = f"h{level}"
    style = 'font-weight: bold;' 
    color = 'color: #BDF347;' 
    if container is not None:
        container.markdown(
            f"<{tag} style='text-align: center; {style} {color}'>{text}</{tag}>",
            unsafe_allow_html=True)
    else:
        st.markdown(
            f"<{tag} style='text-align: center; {style} {color}'>{text}</{tag}>",
            unsafe_allow_html=True)

# Sökväg logga
logo_path = "/MatchAId_1.png"
logo_base64 = get_base64_image(logo_path)
background_path = "/background.png"
background_base64 = get_base64_image(background_path)

# Färger och layout för webbsidan
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{background_base64}");
        background-size: cover;
        display: flex;
        flex-direction: column;
        align-items: center; 
    }}
    .stButton button {{
        background-color: #BDF347;
        color: white;
        font-size: 16px; 
    }}
    .stButton button:hover {{
        background-color: #BDF347;
        color: white;
    }}
    .header {{
        display: flex;
        justify-content: center; 
        margin-top: 50px; 
    }}
    .header img {{
        width: 300px; 
    }}
    .description {{
        text-align: center; 
        margin-top: 70px; 
    }}
    .main-content {{
        display: flex;
        flex-direction: column;
        align-items: center; 
    }}
    .uploader {{
        text-align: center;
        margin-top: 10px;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Lägg till logga
st.markdown(
    f"""
    <div class="header">
        <img src="data:image/png;base64,{logo_base64}" alt="MatchAid Logo"/>
    </div>
    """,
    unsafe_allow_html=True
)

# Beskrivning av tjänsten
st.markdown(
    """
    <div class="description">
        <h3 style='text-align: center; font-weight: bold; color: #BDF347;'>Smartare rekrytering, snabbare resultat</h3>
        <p style='text-align: center; color: white;'>Ladda upp din annons tillsammans med dina kandidaters ansökningar och låt AI analysera fram den främsta kandidaten för tjänsten</p>
    </div>
    """,
    unsafe_allow_html=True
)

# Lägg till ett omslagselement med en klass för att applicera CSS-marginal
st.markdown('<div class="main-content">', unsafe_allow_html=True)

display_centered_header("Ladda upp jobbansökningar", level=2, bold=True)
st.markdown('<div class="uploader">', unsafe_allow_html=True)
uploaded_files = st.file_uploader("Välj jobbansökningar (PDF)", accept_multiple_files=True, type=["pdf"])
st.markdown('</div>', unsafe_allow_html=True)

display_centered_header("Ladda upp jobbannonsen", level=2, bold=True)
st.markdown('<div class="uploader">', unsafe_allow_html=True)
job_ad_file = st.file_uploader("Välj jobbannons (PDF)", type=["pdf"])
st.markdown('</div>', unsafe_allow_html=True)

if st.button("Visa ansökningar") and uploaded_files and job_ad_file:
    display_centered_header("Läser ansökningar, vänligen vänta...", level=3, bold=True)

    applications = [read_pdf(file) for file in uploaded_files]
    job_description = read_pdf(job_ad_file)

    if None not in applications and job_description:
        display_centered_header("Jobbannons:", level=3, bold=True)
        display_centered_header(job_description, level=4)
        for i, application in enumerate(applications):
            display_centered_header(f"Ansökan {i+1}:", level=3, bold=True)
            display_centered_header(application, level=4)

st.markdown('</div>', unsafe_allow_html=True)
