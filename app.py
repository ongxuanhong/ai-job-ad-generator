import streamlit as st
import os
from tempfile import NamedTemporaryFile
from PIL import Image

# Import our project modules
from scripts.extract_text import extract_text_from_file
from scripts.synthesize_content import generate_job_ad_content
from scripts.generate_visual import create_job_ad_visual

st.title("AI-Powered Job Advertisement Generator")
st.write("Upload your documents (PDF, DOCX, TXT) to generate a job advertisement.")

# File uploader: allows multiple files
uploaded_files = st.file_uploader(
    "Choose files", type=["pdf", "docx", "txt"], accept_multiple_files=True
)

if uploaded_files:
    all_paragraphs = []
    st.subheader("File Processing Status")
    for uploaded_file in uploaded_files:
        # Save the uploaded file to a temporary file so our extraction module can process it
        suffix = os.path.splitext(uploaded_file.name)[1]
        with NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
            tmp_file.write(uploaded_file.read())
            tmp_file_path = tmp_file.name

        try:
            result = extract_text_from_file(tmp_file_path)
            st.success(f"Extracted text from: {uploaded_file.name}")
            # Append extracted paragraphs to the global list
            all_paragraphs.extend(result.get("paragraphs", []))
        except Exception as e:
            st.error(f"Error processing {uploaded_file.name}: {e}")
        finally:
            os.unlink(tmp_file_path)  # Remove temporary file

    if all_paragraphs:
        st.subheader("Generating Job Ad Content")
        combined_text = "\n".join(all_paragraphs)
        # Prepare the text_data input as expected by the synthesis module
        text_data = {"paragraphs": [combined_text]}
        # Generate structured job ad content (JSON) using the LLM
        content = generate_job_ad_content(text_data)
        st.json(content)

        st.subheader("Generating Visual Template")
        title = content.get("job_title", "Job Ad")
        summary = content.get("summary", "")
        # Generate visual using the job title and summary
        image_path = create_job_ad_visual(title, summary)
        st.write(f"Generated visual saved at: {image_path}")

        try:
            image = Image.open(image_path)
            st.image(image, caption="Generated Job Ad Visual")
        except Exception as e:
            st.error(f"Error displaying image: {e}")
    else:
        st.error("No text was extracted from the uploaded files.")
