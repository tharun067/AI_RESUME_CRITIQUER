import streamlit as st
import PyPDF2
import os
import io
from google import genai
from dotenv import load_dotenv

load_dotenv(".env.local")

st.set_page_config(page_title="AI Resume Critiquer", page_icon="📃", layout="centered")
st.title("AI Resume Critiquer 📃")
st.markdown("Upload your resume in PDF format and get AI-powered feedback.")

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

uploaded_file = st.file_uploader("Choose a PDF/TXT file", type=["pdf", "txt"])
job_role = st.text_input("Enter the job role you are applying for(optinal):")

analyze = st.button("Analyze Resume")

def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"
    return text.strip()

def extract_text_from_file(uploaded_file):
    """Extract text from a PDF file."""
    if uploaded_file.type == "application/pdf":
        return extract_text_from_pdf(io.BytesIO(uploaded_file.read()))
    return uploaded_file.read().decode("utf-8")

if analyze and uploaded_file:
    # Only for testing purposes(if not Google api key is set)
    if not GOOGLE_API_KEY:
        st.error("Google API key is not set. Please set  it in the .env file.")
    try:
        file_content = extract_text_from_file(uploaded_file)
        
        if not file_content.strip():
            st.error("The uploaded file is empty or could not be read. Please upload a valid PDF file.")
            st.stop()
        
        prompt = f"""Please analyze this resume and provide constructive feedback.
        Focus on the following aspects:
        1. Content clarity and impact
        2. Skills presentation
        3. Experience description
        4. Specific improvements for {job_role if job_role else 'general job applications'}

        Resume content:
        {file_content}
        
        Please provide your analysis in a clear, structured format with specific recommendations."""

        client = genai.Client(api_key=GOOGLE_API_KEY)
        model = "gemini-2.5-flash"
        chat = client.chats.create(
            model=model,
        )
        response = chat.send_message(
            prompt
        )
        st.markdown("### Analysis Result:")
        st.markdown(response.text)

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
