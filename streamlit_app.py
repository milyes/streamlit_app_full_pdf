import fitz
print(fitz.__doc__.splitlines()[0])
# → 'PyMuPDF 1.24.x: Python bindings for MuPDF – a lightweight PDF viewer & toolkit'


import pytesseract
from PIL import Image
import io
import streamlit as st
from fpdf import FPDF

st.set_page_config(page_title="TOCH OCR PDF", layout="wide")
st.title("TOCH OCR PDF – Démo complète avec export PDF")

uploaded_file = st.file_uploader("Sélectionnez un fichier PDF", type="pdf")

def extract_text_from_pdf(file):
    text_output = []
    pdf_doc = fitz.open(stream=file.read(), filetype="pdf")
    for page_num in range(len(pdf_doc)):
        page = pdf_doc.load_page(page_num)
        pix = page.get_pixmap()
        img_data = pix.tobytes("png")
        image = Image.open(io.BytesIO(img_data))
        text = pytesseract.image_to_string(image)
        text_output.append(text)
    return "\n\n".join(text_output)

def generate_pdf(text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)
    for line in text.splitlines():
        pdf.multi_cell(0, 10, line)
    output = io.BytesIO()
    pdf.output(output)
    output.seek(0)
    return output

if uploaded_file:
    st.info("Analyse OCR en cours...")
    extracted_text = extract_text_from_pdf(uploaded_file)

    st.subheader("Texte extrait :")
    st.text_area("Résultat OCR", extracted_text, height=400)

    st.download_button("Télécharger le texte en .txt", extracted_text, file_name="ocr_result.txt")

    pdf_data = generate_pdf(extracted_text)
    st.download_button("Télécharger en PDF", pdf_data, file_name="ocr_result.pdf")
