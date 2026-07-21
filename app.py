import streamlit as st
from groq import Groq
from pypdf import PdfReader
from dotenv import load_dotenv
import os

# Load API key
load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

st.title("📄 AI PDF Summarizer")

uploaded_file = st.file_uploader("Upload a PDF", type="pdf")

if uploaded_file:
    reader = PdfReader(uploaded_file)

    text = ""

    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text()

    summary_type = st.selectbox(
        "Choose Summary Type",
        ["Short", "Detailed", "Bullet Points"]
    )

    if st.button("Generate Summary"):
        prompt = f"""
You are an AI PDF summarizer.

Read the following PDF carefully and generate the response in the EXACT order below.

## 1. Short Summary
- Write a concise summary in one paragraph (5-8 sentences).

## 2. Detailed Summary
- Explain all important topics and concepts in detail.
- Cover every major section of the PDF.

## 3. Bullet Point Summary
- List all important points using bullet points.
- Include every important concept.

IMPORTANT:
- Always keep the order exactly as:
  1. Short Summary
  2. Detailed Summary
  3. Bullet Point Summary
- Use clear headings for each section.
- Do not skip any section.

PDF Content:
{text}
"""

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        st.subheader("Summary")
        st.write(response.choices[0].message.content)
