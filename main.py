# main.py
import argparse
from scripts import extract_text, synthesize_content, generate_visual

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AI Job Ad Template Generator CLI")
    parser.add_argument(
        "--pdf", required=True, help="Path to the input PDF job description"
    )
    parser.add_argument(
        "--output_json",
        default="data/output/generated_content.json",
        help="Path to save the generated job ad content JSON",
    )
    parser.add_argument(
        "--output_image",
        default="data/output/job_ad_visual.png",
        help="Path to save the generated job ad image",
    )
    args = parser.parse_args()

    # Step 1: Extract text from the PDF
    text_data = extract_text.extract_text_from_pdf(args.pdf)
    extract_text.save_text_to_json(text_data, "data/output/extracted_text.json")
    print(f"Text extracted from {args.pdf}")

    # Step 2: Generate structured content using LLM
    content = synthesize_content.generate_job_ad_content(text_data)
    synthesize_content.save_generated_content(content, args.output_json)
    print(f"Structured content generated and saved to {args.output_json}")

    # Step 3: Create a visual for the job ad
    title = content.get("job_title", "Job Ad")
    summary = content.get("summary", "")
    image_path = generate_visual.create_job_ad_visual(title, summary)
    # If generate_visual already saves the file, use returned path; otherwise, save via PIL Image
    print(f"Visual generated and saved to {image_path}")

    print("Job advertisement template generation complete.")
    print(
        f"\nResults:\n- Content JSON: {args.output_json}\n- Visual Image: {image_path}"
    )
