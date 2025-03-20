# scripts/generate_visual.py
import os
from datetime import datetime

import fal_client
import requests


def on_queue_update(update):
    if isinstance(update, fal_client.InProgress):
        for log in update.logs:
            print(log["message"])


def generate_image_with_falai(prompt: str) -> (bytes, str):
    """
    Calls the fal-ai/recraft-v3 API using fal_client.subscribe with the given prompt.
    Returns the binary image data along with the file extension.
    """
    result = fal_client.subscribe(
        "fal-ai/recraft-v3",
        arguments={
            "prompt": prompt,
            "image_size": "square_hd",
            "style": "realistic_image",
            "colors": [],
        },
        with_logs=True,
        on_queue_update=on_queue_update,
    )

    images = result.get("images", [])
    if not images:
        raise ValueError("No images returned from the API.")

    image_info = images[0]
    image_url = image_info.get("url")
    file_name = image_info.get("file_name", "image.webp")
    extension = file_name.split(".")[-1]

    # Download the generated image from the provided URL
    image_response = requests.get(image_url)
    image_response.raise_for_status()

    return image_response.content, extension


def create_job_ad_visual(title: str, summary: str) -> str:
    """
    Generate a visual (image) for the job ad using the fal-ai/recraft-v3 API via fal_client.
    Constructs a prompt from the provided title and summary, downloads the resulting image,
    and saves it locally.
    """
    prompt_text = (
        "Generate a visual (image) for the job ad based on the title and summary.\n"
        f"Professional job advertisement poster for {title} role. {summary}"
    )

    image_content, extension = generate_image_with_falai(prompt_text)

    # Save the image with a timestamped filename to avoid conflicts
    os.makedirs("data/output", exist_ok=True)
    image_filename = (
        f"job_ad_visual_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{extension}"
    )
    image_path = os.path.join("data/output", image_filename)

    with open(image_path, "wb") as f:
        f.write(image_content)

    return image_path


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Generate a visual for the job ad using fal-ai/recraft-v3 API via fal_client"
    )
    parser.add_argument("--title", required=True, help="Job title for the ad")
    parser.add_argument(
        "--summary", required=True, help="Job summary or description snippet for the ad"
    )
    args = parser.parse_args()

    path = create_job_ad_visual(args.title, args.summary)
    print(f"Generated visual saved at {path}")
