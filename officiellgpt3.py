# -*- coding: utf-8 -*-

import streamlit as st
import openai
import pdfplumber
import logging
import fitz  # PyMuPDF
from PIL import Image

# Configure your OpenAI API key
openai.api_key = st.secrets["openai"]["api_key"]

# Configure logging
logging.basicConfig(level=logging.INFO)

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
    prompt = f"Användaren har gett dig {len(applications)} filer som är jobbansökningar och 1 fil som är själva jobbannonsen som ansökningarna är till. \
Ditt uppdrag är att noggrant granska och jämföra innehållet i dessa ansökningsfiler mot kraven specificerade i jobbannonsen för att identifiera de mest lämpliga kandidaterna. Du bör prioritera och utvärdera kandidaterna baserat på följande kriterier i angiven ordning: utbildning, erfarenheter och personliga egenskaper. \
För varje kandidat, plocka fram för- och efternamn, telefonnummer och e-mail. Se till att du enbart använder information direkt tillgänglig från ansökningsdokumenten och jobbannonsen utan att göra antaganden eller lägga till information. \
Vidare måste du specificera om varje kandidat är kvalificerad eller inte kvalificerad baserat på om de uppfyller de specifika yrkeskraven angivna i annonsen, till exempel 'utbildad sjuksköterska'. OM ANSÖKNINGEN INTE HAR RÄTT UTBILDNING ENLIGT ANNONSEN FÅR DE ABSOLUT INTE HAMNA PÅ KVALIFICERAD. \
Var noga med att inte hitta på information eller felaktigt tolka data från dokumenten. Det är avgörande att du baserar dina slutsatser och rankning strikt på de uppgifter som finns i ansökningsfiler och jobbannonsen för att garantera att endast de mest passande kandidaterna väljs ut."

    for i, application in enumerate(applications):
        prompt += f"Ansökan {i+1}:\n{application}\n\n"

    prompt += f"Jobbannons:\n{job_description}\n\n"

    prompt += "För varje kandidat, ange följande format:\n"
    prompt += "Namn: [Full Name]\n"
    prompt += "Telefon: [Phone Number]\n"
    prompt += "E-post: [Email Address]\n"
    prompt += "Kvalificerad: Ja/Nej\n"
    prompt += "Förklaring: [Explanation]\n"

    try:
        response = openai.Completion.create(
            engine="gpt-3.5-turbo-instruct",
            prompt=prompt,
            max_tokens=400,
            timeout=30
        )
        return response.choices[0].text
    except openai.error.OpenAIError as e:
        st.error(f"Fel vid API-anrop: {e}")
        logging.error(f"Fel vid API-anrop: {e}")
        return None
    except Exception as e:
        st.error(f"En oväntad fel inträffade: {e}")
        logging.error(f"En oväntad fel inträffade: {e}")
        return None

st.title("Jobbansökning med GPT")

st.header("Ladda upp jobbansökningar")
uploaded_files = st.file_uploader("Välj jobbansökningar (PDF)", accept_multiple_files=True, type=["pdf"])

st.header("Ladda upp jobbannonsen")
job_ad_file = st.file_uploader("Välj jobbannons (PDF)", accept_multiple_files=False, type=["pdf"])

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
                    if line.startswith("Namn:"):
                        candidate_info["name"] = line.replace("Namn: ", "").strip()
                    elif line.startswith("Telefon:"):
                        candidate_info["phone"] = line.replace("Telefon: ", "").strip()
                    elif line.startswith("E-post:"):
                        candidate_info["email"] = line.replace("E-post: ", "").strip()
                    elif line.startswith("Kvalificerad:"):
                        candidate_info["qualified"] = line.replace("Kvalificerad: ", "").strip().lower() == 'ja'
                    elif line.startswith("Förklaring:"):
                        candidate_info["explanation"] = line.replace("Förklaring: ", "").strip()
                if candidate_info:
                    candidates.append(candidate_info)

            qualified = [cand for cand in candidates if cand['qualified']]
            not_qualified = [cand for cand in candidates if not cand['qualified']]

            st.write("Kvalificerade ansökningar")
            for i, candidate in enumerate(qualified, 1):
                with st.expander(f"{i}. {candidate['name']}"):
                    st.write(f"Telefon: {candidate['phone']}")
                    st.write(f"E-post: {candidate['email']}")
                    st.write(f"Förklaring: {candidate['explanation']}")
                    images = pdf_to_images(candidate['file_bytes'])
                    cols = st.columns(3)  # Create 3 columns for displaying images
                    for idx, img in enumerate(images):
                        cols[idx % 3].image(img, caption=f"{candidate['name']} - Sida {idx + 1}")

            st.write("Ej kvalificerade ansökningar")
            for i, candidate in enumerate(not_qualified, 1):
                with st.expander(f"{i}. {candidate['name']}"):
                    st.write(f"Telefon: {candidate['phone']}")
                    st.write(f"E-post: {candidate['email']}")
                    st.write(f"Förklaring: {candidate['explanation']}")
                    images = pdf_to_images(candidate['file_bytes'])
                    cols = st.columns(3)  # Create 3 columns for displaying images
                    for idx, img in enumerate(images):
                        cols[idx % 3].image(img, caption=f"{candidate['name']} - Sida {idx + 1}")
