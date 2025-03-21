# main.py
import os
import argparse
import json
from scripts.extract_text import extract_text_from_folder
from scripts.synthesize_content import generate_job_ad_content, save_generated_content
from scripts.generate_visual import create_job_ad_visual


def main():
    parser = argparse.ArgumentParser(
        description="Process documents from an input folder to generate job ad content and a final visual image."
    )
    parser.add_argument(
        "--folder",
        required=True,
        help="Path to the input folder (e.g., data/documents/) containing PDF, DOCX, and TXT files.",
    )
    parser.add_argument(
        "--output_json",
        required=True,
        help="Path to the output JSON file for generated job ad content (e.g., data/output/generated_content.json).",
    )
    parser.add_argument(
        "--output_image",
        required=True,
        help="Path to the output image file (e.g., data/output/job_ad_visual.png).",
    )
    args = parser.parse_args()

    # Step 1: Extract text from all supported documents in the folder.
    extracted_docs = extract_text_from_folder(args.folder)
    print(f"Extracted text from {len(extracted_docs)} file(s).")

    # Step 2: Combine the text from all documents into a single context.
    # Here we join each document's paragraphs and then join all documents together.
    combined_text = "\n".join(
        ["\n".join(doc.get("paragraphs", [])) for doc in extracted_docs]
    )
    # Prepare the input for the LLM as a dictionary.
    text_data = {"paragraphs": [combined_text]}

    # Generate structured job ad content using the LLM.
    content = generate_job_ad_content(text_data)
    save_generated_content(content, args.output_json)
    print(f"Generated job ad content saved to {args.output_json}")

    # Step 3: Generate a visual for the job ad using the generated content.
    # Use the job title and summary as basis for the image prompt.
    title = content.get("job_title", "Job Ad")
    summary = content.get("summary", "")
    # Create the visual; this function returns the path where the image was saved.
    generated_image_path = create_job_ad_visual(title, summary)

    # Ensure the final image is at the specified output path.
    if os.path.abspath(generated_image_path) != os.path.abspath(args.output_image):
        os.makedirs(os.path.dirname(args.output_image), exist_ok=True)
        os.rename(generated_image_path, args.output_image)
        final_image_path = args.output_image
    else:
        final_image_path = generated_image_path

    print(f"Generated visual saved at {final_image_path}")


if __name__ == "__main__":
    main()
