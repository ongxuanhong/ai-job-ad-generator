import pymupdf
import json


def extract_text_from_pdf(pdf_path: str) -> dict:
    """Extract text from PDF and return as a structured dict with paragraphs."""
    doc = pymupdf.open(pdf_path)
    all_text = []
    for page in doc:
        text = page.get_text().strip()
        if text:
            # Split by double newlines to separate paragraphs
            paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
            all_text.extend(paragraphs)
    doc.close()
    return {"paragraphs": all_text}


def save_text_to_json(text_data: dict, output_path: str):
    """Save extracted text data (dict) to a JSON file."""
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(text_data, f, indent=2)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Extract text from PDF")
    parser.add_argument("--pdf", required=True, help="Path to input PDF file")
    parser.add_argument("--out", required=True, help="Path to output JSON file")
    args = parser.parse_args()
    data = extract_text_from_pdf(args.pdf)
    save_text_to_json(data, args.out)
    print(f"Extracted text saved to {args.out}")
