import os
import json
import fitz  # PyMuPDF for PDF extraction
import docx  # python-docx for DOCX extraction
from typing import List, Dict


def extract_text_from_pdf(pdf_path: str) -> List[str]:
    """
    Extract text from a PDF file using PyMuPDF.

    Args:
        pdf_path (str): Path to the PDF file.

    Returns:
        List[str]: List of extracted paragraphs.
    """
    paragraphs = []
    doc = fitz.open(pdf_path)
    for page in doc:
        text = page.get_text().strip()
        if text:
            # Split by double newlines to separate paragraphs
            paras = [p.strip() for p in text.split("\n\n") if p.strip()]
            paragraphs.extend(paras)
    doc.close()
    return paragraphs


def extract_text_from_docx(docx_path: str) -> List[str]:
    """
    Extract text from a DOCX file using python-docx.

    Args:
        docx_path (str): Path to the DOCX file.

    Returns:
        List[str]: List of paragraphs extracted from the document.
    """
    doc = docx.Document(docx_path)
    paragraphs = [para.text.strip() for para in doc.paragraphs if para.text.strip()]
    return paragraphs


def extract_text_from_txt(txt_path: str) -> List[str]:
    """
    Extract text from a TXT file.

    Args:
        txt_path (str): Path to the TXT file.

    Returns:
        List[str]: List of paragraphs, split by double newlines.
    """
    with open(txt_path, "r", encoding="utf-8") as f:
        content = f.read().strip()
    paragraphs = [p.strip() for p in content.split("\n\n") if p.strip()]
    return paragraphs


def extract_text_from_file(file_path: str) -> Dict[str, List[str]]:
    """
    Determine the file type based on extension and extract text accordingly.

    Supported formats: .pdf, .docx, .txt

    Args:
        file_path (str): Path to the input file.

    Returns:
        Dict[str, List[str]]: A dictionary containing 'file_name' and 'paragraphs'.

    Raises:
        ValueError: If the file format is not supported.
    """
    _, ext = os.path.splitext(file_path)
    ext = ext.lower()
    if ext == ".pdf":
        paragraphs = extract_text_from_pdf(file_path)
    elif ext == ".docx":
        paragraphs = extract_text_from_docx(file_path)
    elif ext == ".txt":
        paragraphs = extract_text_from_txt(file_path)
    else:
        raise ValueError(f"Unsupported file format: {ext}")

    return {"file_name": os.path.basename(file_path), "paragraphs": paragraphs}


def extract_text_from_folder(folder_path: str) -> List[Dict[str, List[str]]]:
    """
    Walk through a folder and extract text from all supported files.

    Supported formats: .pdf, .docx, .txt

    Args:
        folder_path (str): Path to the folder containing input files.

    Returns:
        List[Dict[str, List[str]]]: List of dictionaries for each file with its name and paragraphs.
    """
    extracted = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith((".pdf", ".docx", ".txt")):
                file_path = os.path.join(root, file)
                try:
                    result = extract_text_from_file(file_path)
                    extracted.append(result)
                except Exception as e:
                    print(f"Error extracting {file_path}: {e}")
    return extracted


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Extract text from files (.pdf, .docx, .txt) in a given folder and save as JSON"
    )
    parser.add_argument(
        "--folder", required=True, help="Path to the folder with input files"
    )
    parser.add_argument("--out", required=True, help="Path to the output JSON file")
    args = parser.parse_args()

    results = extract_text_from_folder(args.folder)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print(f"Extracted text saved to {args.out}")
