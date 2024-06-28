from dotenv import load_dotenv
load_dotenv()  # Load all the environment variables from .env

import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Load Gemini pro vision model
model = genai.GenerativeModel('gemini-1.5-pro')

def get_gemini_response(input, image, user_prompt):
    response = model.generate_content([input, image[0], user_prompt])
    return response.text

def input_image_details(uploaded_file):
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Initialize Streamlit app
st.set_page_config(page_title="MultiLanguage Image Extractor")

# Main layout with two columns
col1, col2 = st.columns([2, 1])  # Adjusted column ratios

# Column 1: Image upload and display
with col1:
    st.header("Upload and View Image")
    uploaded_file = st.file_uploader("Choose an image of your choice...", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)

# Divider between columns
st.markdown("---")

# Column 2: Input and response
with col2:
    st.header("Input and Response Section")
    input_prompt = st.text_area("Input Prompt:", height=250, key="input")
    if st.button("Tell me about the image"):
        if input_prompt.strip() == "":
            st.warning("Please provide an input prompt.")
        elif uploaded_file is None:
            st.warning("Please upload an image.")
        else:
            try:
                with st.spinner('Processing...'):
                    image_data = input_image_details(uploaded_file)
                    response = get_gemini_response(input_prompt, image_data, input_prompt)
                st.success("Here is the information extracted from the image:")
                st.write(response)
            except Exception as e:
                st.error(f"An error occurred: {e}")

# Layout improvements
st.markdown("""
    <style>
    .stTextInput {
        background-color: #f5f5f5;
        border: 1px solid #ccc;
        border-radius: 5px;
        padding: 10px;
        margin-bottom: 10px;
    }
    .stButton {
        background-color: #4A90E2;
        color: white;
        padding: 10px 20px;
        border: none;
        border-radius: 5px;
        cursor: pointer;
    }
    .stButton:hover {
        background-color: #357EBD;
    }
    hr {
        border: 0;
        height: 1px;
        background: #ccc;
        margin: 20px 0;
    }
    </style>
""", unsafe_allow_html=True)

# Footer
st.markdown("<p style='text-align: center; color: #888;'>MultiLanguage Image Extractor helps you extract and understand details from invoices in various languages using advanced AI models.</p>", unsafe_allow_html=True)
