import json
import os

from langchain_openai import OpenAI

# Load API key from config (assuming OpenAI API key is set as env variable or in config)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


def generate_job_ad_content(text_data: dict) -> dict:
    """Use an LLM to synthesize structured job ad content from extracted text."""
    paragraphs = text_data.get("paragraphs", [])
    # Combine or selectively use paragraphs as context
    context = "\n".join(
        paragraphs[:5]
    )  # (for example, use first 5 paragraphs or full text)
    prompt = (
        "Extract the key details from the job description below and respond in JSON format with keys: "
        "job_title, summary, responsibilities, requirements, qualifications. \n\n"
        f"Job Description:\n{context}\n"
    )
    # Initialize LLM (OpenAI GPT model via LangChain)
    llm = OpenAI(model="gpt-3.5-turbo-instruct")
    result = llm.invoke(prompt)

    # Parse LLM result (assuming it's valid JSON string or close to it)
    try:
        content = json.loads(result)
    except json.JSONDecodeError:
        # If LLM didn't return pure JSON, we might need to clean the result
        # For simplicity, handle basic fixes or use regex to find JSON in the text
        json_str = result[result.find("{") : result.rfind("}") + 1]
        content = json.loads(json_str)
    return content


def save_generated_content(content: dict, output_path: str):
    """Save the generated structured content to a JSON file."""
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(content, f, indent=2)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Generate structured job ad content from text"
    )
    parser.add_argument(
        "--in_json", required=True, help="Path to input JSON (extracted text)"
    )
    parser.add_argument(
        "--out_json", required=True, help="Path to output JSON (structured content)"
    )
    args = parser.parse_args()
    with open(args.in_json, "r", encoding="utf-8") as f:
        text_data = json.load(f)
    content = generate_job_ad_content(text_data)
    save_generated_content(content, args.out_json)
    print(f"Generated content saved to {args.out_json}")
