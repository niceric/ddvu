# -*- coding: utf-8 -*-

import streamlit as st
import openai
import pdfplumber
import logging
import base64
import fitz  # PyMuPDF
from typing import Optional    
from PIL import Image
from streamlit.delta_generator import DeltaGenerator

# Configure your OpenAI API key
openai.api_key = 123 #st.secrets["openai"]["api_key"]

# Configure logging
logging.basicConfig(level=logging.INFO)

# Konvertera loggan till base64
def get_base64_image(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    return encoded_string

# Sökväg logga
logo_path = "matchaid_1.png"
logo_base64 = get_base64_image(logo_path)
background_path = "background.png"
background_base64 = get_base64_image(background_path)

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

st.markdown(
    """
    <style>
    body, .stButton, .stTextInput, h1, h2, h3, h4, h5, h6, p, label, .reportview-container .markdown-text-container {
        color: white !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

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
        color: white;
    }}
    .uploader {{
        text-align: center;
        margin-top: 10px;
        color: white;
    }}
    .text {{
        color: white;
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

# CSS to make text white
st.markdown(
    """
    <style>
    .css-1d391kg p {
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

def read_pdf(file):
    text = ""
    try:
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                text += page.extract_text()
    except Exception as e:
        st.error(f"Fel vid läsning av PDF: {e}")
        logging.error(f"Fel vid läsning av PDF: {e}")
    return text

def pdf_to_images(pdf_bytes):
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    images = []
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)  # number of page
        pix = page.get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        images.append(img)
    return images

def analyze_applications(applications, job_description):
    messages = [
        {
            "role": "system",
            "content": f"Användaren har gett dig {len(applications)} filer som är jobbansökningar och 1 fil som är själva jobbannonsen som ansökningarna är till. \
Ditt uppdrag är att noggrant granska och jämföra innehållet i dessa ansökningsfiler mot kraven specificerade i jobbannonsen för att identifiera de mest lämpliga kandidaterna. Du bör prioritera och utvärdera kandidaterna baserat på följande kriterier i angiven ordning: utbildning, erfarenheter och personliga egenskaper. \
För varje kandidat, plocka fram för- och efternamn, telefonnummer och e-mail. Se till att du enbart använder information direkt tillgänglig från ansökningsdokumenten och jobbannonsen utan att göra antaganden eller lägga till information. \
Vidare måste du specificera om varje kandidat är kvalificerad eller inte kvalificerad baserat på om de uppfyller de specifika yrkeskraven angivna i annonsen, till exempel 'utbildad sjuksköterska'. OM ANSÖKNINGEN INTE HAR RÄTT UTBILDNING ENLIGT ANNONSEN FÅR DE ABSOLUT INTE HAMNA PÅ KVALIFICERAD. \
Var noga med att inte hitta på information eller felaktigt tolka data från dokumenten. Det är avgörande att du baserar dina slutsatser och rankning strikt på de uppgifter som finns i ansökningsfiler och jobbannonsen för att garantera att endast de mest passande kandidaterna väljs ut."
        }
    ]

    for i, application in enumerate(applications):
        messages.append({"role": "user", "content": f"Ansökan {i+1}:\n{application}\n\n"})
    
    messages.append({"role": "user", "content": f"Jobbannons:\n{job_description}\n\n"})
    messages.append({"role": "user", "content": "För varje kandidat, ange följande format:\nNamn: [Full Name]\nTelefon: [Phone Number]\nE-post: [Email Address]\nKvalificerad: Ja/Nej\nFörklaring: [Explanation]\n"})

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=messages,
            max_tokens=1100,
            temperature=0
        )
        return response['choices'][0]['message']['content']
    except openai.error.OpenAIError as e:
        st.error(f"Fel vid API-anrop: {e}")
        logging.error(f"Fel vid API-anrop: {e}")
        return None
    except Exception as e:
        st.error(f"En oväntad fel inträffade: {e}")
        logging.error(f"En oväntad fel inträffade: {e}")
        return None

# Lägg till ett omslagselement med en klass för att applicera CSS-marginal
st.markdown('<div class="main-content">', unsafe_allow_html=True)

display_centered_header("Ladda upp jobbansökningar", level=2, bold=True)
st.markdown('<div class="uploader">', unsafe_allow_html=True)
uploaded_files = st.file_uploader("Välj jobbansökningar (PDF)", accept_multiple_files=True, type=["pdf"])
st.markdown('<div class="text">', unsafe_allow_html=True)

display_centered_header("Ladda upp jobbannonsen", level=2, bold=True)
st.markdown('<div class="uploader">',unsafe_allow_html=True)
job_ad_file = st.file_uploader("Välj jobbannons (PDF)", type=["pdf"])
st.markdown('</div>', unsafe_allow_html=True)

if st.button("Analysera") and uploaded_files and job_ad_file:
    st.write("Analyserar ansökningar, vänligen vänta...")

    # Read job description
    job_description = read_pdf(job_ad_file)

    # Read applications and store the byte content of the PDFs
    applications = []
    application_files = []
    for file in uploaded_files:
        applications.append(read_pdf(file))
        file.seek(0)
        application_files.append(file.read())

    if None not in applications and job_description:
        result = analyze_applications(applications, job_description)
        if result:
            # Parse the result
            candidate_lines = result.strip().split("\n\n")
            candidates = []
            for i, block in enumerate(candidate_lines):
                lines = block.split("\n")
                candidate_info = {"application": applications[i], "file_bytes": application_files[i]}  # Store the original application text and byte content
                for line in lines:
                    if line.startswith("**Namn:**"):
                        candidate_info["name"] = line.replace("**Namn:**", "").strip()
                    elif line.startswith("**Telefon:**"):
                        candidate_info["phone"] = line.replace("**Telefon:**", "").strip()
                    elif line.startswith("**E-post:**"):
                        candidate_info["email"] = line.replace("**E-post:**", "").strip()
                    elif line.startswith("**Kvalificerad:**"):
                        candidate_info["qualified"] = line.replace("**Kvalificerad:**", "").strip().lower() == 'ja'
                    elif line.startswith("**Förklaring:**"):
                        candidate_info["explanation"] = line.replace("**Förklaring:**", "").strip()
                if candidate_info and "name" in candidate_info:  # Ensure that there is a name key in candidate_info
                    candidates.append(candidate_info)

            qualified = [cand for cand in candidates if cand.get('qualified')]
            not_qualified = [cand for cand in candidates if not cand.get('qualified')]

            st.write("Kvalificerade ansökningar")
            for i, candidate in enumerate(qualified, 1):
                with st.expander(f"{i}. {candidate.get('name', 'Ingen namn tillgänglig')}"):
                    st.write(f"Telefon: {candidate.get('phone', 'Ingen telefon tillgänglig')}")
                    st.write(f"E-post: {candidate.get('email', 'Ingen e-post tillgänglig')}")
                    st.write(f"Förklaring: {candidate.get('explanation', 'Ingen förklaring tillgänglig')}")
                    images = pdf_to_images(candidate['file_bytes'])
                    cols = st.columns(3)  # Create 3 columns for displaying images
                    for idx, img in enumerate(images):
                        cols[idx % 3].image(img, caption=f"{candidate.get('name', 'Ingen namn tillgänglig')} - Sida {idx + 1}")

            st.write("Ej kvalificerade ansökningar")
            for i, candidate in enumerate(not_qualified, 1):
                with st.expander(f"{i}. {candidate.get('name', 'Ingen namn tillgänglig')}"):
                    st.write(f"Telefon: {candidate.get('phone', 'Ingen telefon tillgänglig')}")
                    st.write(f"E-post: {candidate.get('email', 'Ingen e-post tillgänglig')}")
                    st.write(f"Förklaring: {candidate.get('explanation', 'Ingen förklaring tillgänglig')}")
                    images = pdf_to_images(candidate['file_bytes'])
                    cols = st.columns(3)  # Create 3 columns for displaying images
                    for idx, img in enumerate(images):
                        cols[idx % 3].image(img, caption=f"{candidate.get('name', 'Ingen namn tillgänglig')} - Sida {idx + 1}")
