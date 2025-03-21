# Automated Document-Driven Advertisement Template Generator

An end-to-end modular system that extracts structured text from PDF job descriptions, synthesizes job advertisement content using an LLM, and generates accompanying visual templates using Fal.ai's image generation API. The project is designed for CLI execution and structured for easy extension and maintenance.

## Tech Stack

- **PyMuPDF**: Used for structured text extraction from PDF files.
- **LangChain (with OpenAI)**: Utilized for content synthesis (LLM processing) to generate structured JSON outputs from extracted text.
- **Fal.ai**: Employed to generate job advertisement visuals using their recraft-v3 API.
- **Python**: Primary programming language.
- **UnitTest/pytest**: For testing core functionalities.

## Project Structure

```
ai_job_ad_generator/
├── config/
│   └── settings.yaml         # Configuration file (API keys, model parameters, etc.)
├── data/
│   ├── samples/              # Sample input PDFs (e.g., job description PDFs)
│   └── output/               # Generated outputs: extracted text (JSON), synthesized content, images
├── scripts/
│   ├── __init__.py
│   ├── extract_text.py       # Module for PDF text extraction using PyMuPDF
│   ├── synthesize_content.py # Module for LLM processing with LangChain & OpenAI
│   └── generate_visual.py    # Module for generating visuals using Fal.ai's API
├── tests/                    # Unit tests for core functionalities
│   ├── test_extract_text.py
│   ├── test_synthesize_content.py
│   └── test_generate_visual.py
└── main.py                   # CLI entry point tying all modules together
```

## Setup and Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/ai_job_ad_generator.git
   cd ai_job_ad_generator
   ```

2. **Create a Virtual Environment and Install Dependencies:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use: venv\Scripts\activate
   pip install -r requirements.txt
   ```
   
   *Example `requirements.txt`:*
   ```
   pymupdf
   langchain
   openai
   requests
   python-dotenv
   pytest
   ```

3. **Configuration:**

   - **API Keys:**  
     Create a `.env` file or update `config/settings.yaml` with your API keys:
     - `OPENAI_API_KEY` for OpenAI access (used in content synthesis)
     - `FALAI_API_KEY` for Fal.ai's recraft-v3 image generation API

   - For example, using a `.env` file:
     ```
     OPENAI_API_KEY=your_openai_api_key
     FALAI_API_KEY=your_falai_api_key
     ```

## Usage

### CLI Execution

The system is designed to run as a CLI tool. Use the main entry point `main.py` to perform the full pipeline (PDF text extraction → LLM content synthesis → Visual generation).

```bash
python main.py --pdf data/samples/sample_job_description.pdf \
    --output_json data/output/generated_content.json \
    --output_image data/output/job_ad_visual.png
```

- **`--pdf`**: Path to the input PDF file containing the job description.
- **`--output_json`**: File path where the synthesized job ad content (JSON) will be saved.
- **`--output_image`**: File path where the generated visual image will be saved.

### Module Details

- **Data Extraction & Preprocessing (`scripts/extract_text.py`)**:  
  Uses PyMuPDF to extract and clean text from PDF files. Output is stored in JSON format.

- **Content Synthesis (LLM Processing) (`scripts/synthesize_content.py`)**:  
  Uses LangChain with OpenAI’s GPT (e.g., gpt-3.5-turbo) to convert extracted text into structured JSON content containing job title, summary, responsibilities, requirements, and qualifications.

- **Visual Template Creation (`scripts/generate_visual.py`)**:  
  Calls the Fal.ai recraft-v3 API to generate an image based on a prompt derived from the job title and summary. The generated image is stored locally.

## Testing

Unit tests are provided in the `tests/` directory. To run the tests using `pytest`:

```bash
pytest tests/
```

Tests cover the core functionalities for text extraction, content synthesis, and visual generation.

## Extending the Project

- **Adding More File Formats:**  
  Extend the data extraction module to handle additional file types (e.g., DOCX, HTML).

- **Enhancing Content Synthesis:**  
  Integrate more advanced LLM workflows using LlamaIndex, LangGraph, or CrewAI for improved content structuring.

- **Improving Visual Generation:**  
  Replace the placeholder functions with direct integration of a local Stable Diffusion pipeline or additional Fal.ai features.

## Acknowledgements

- [PyMuPDF](https://pymupdf.readthedocs.io/) for robust PDF text extraction.
- [LangChain](https://github.com/langchain-ai/langchain) and OpenAI for seamless LLM integration.
- [Fal.ai](https://fal.ai/) for innovative image generation capabilities.