# Automated Document-Driven Advertisement Template Generator

An end-to-end modular system that processes documents (PDF, DOCX, TXT) from a specified folder, extracts structured text, synthesizes job advertisement content using a large language model via LangChain/OpenAI, and generates a complementary visual using Fal.ai's recraft-v3 API. The final output is a structured JSON file for the job ad content and a single generated image saved at a user-specified location.

## Tech Stack

- **PyMuPDF**: For structured text extraction from PDF files.
- **python-docx**: For reading DOCX files.
- **Built-in Python I/O**: For handling TXT files.
- **LangChain & OpenAI**: For LLM-based content synthesis (converting extracted text into structured JSON).
- **Fal.ai**: For generating job advertisement visuals via the recraft-v3 API.
- **Python**: Primary programming language.
- **Unit Testing (pytest)**: For testing core functionalities.

## Project Structure

```
ai_job_ad_generator/
├── data/
│   ├── documents/            # Input folder containing job description files (.pdf, .docx, .txt)
│   └── output/               # Folder for output JSON and generated images
├── scripts/
│   ├── __init__.py
│   ├── extract_text.py       # Module to extract text from PDFs, DOCX, and TXT files
│   ├── synthesize_content.py # Module to synthesize job ad content via LangChain/OpenAI
│   └── generate_visual.py    # Module to generate visuals using Fal.ai API
├── tests/                    # Unit tests for core functionalities
│   ├── test_extract_text.py
│   ├── test_synthesize_content.py
│   └── test_generate_visual.py
└── main.py                   # CLI entry point to execute the full pipeline
```

## Setup and Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/ongxuanhong/ai-job-ad-generator.git
   cd ai_job_ad_generator
   ```

2. **Create a Virtual Environment and Install Dependencies:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

   *Example `requirements.txt`:*
   ```
   pymupdf
   python-docx
   langchain
   openai
   requests
   python-dotenv
   pytest
   ```

3. **Configuration:**

   - **API Keys:**  
     Export environment variables with your API keys:
     - `OPENAI_API_KEY` for OpenAI access (used in content synthesis).
     - `FAL_KEY` for Fal.ai’s recraft-v3 image generation API.

   - Example:
     ```
     export OPENAI_API_KEY=your_openai_api_key
     export FAL_KEY=your_falai_api_key
     ```

## Usage

### CLI Execution

The system is executed via the CLI using **main.py**. This process involves:

1. **Step 1 – Extraction:**  
   The script scans an input folder (e.g., `data/documents/`) and extracts text from all supported file types (PDF, DOCX, TXT).

2. **Step 2 – Content Synthesis:**  
   It combines the extracted text into a single context and passes it to the LLM (via LangChain/OpenAI) to generate structured job advertisement content in JSON format.

3. **Step 3 – Visual Generation:**  
   Based on the synthesized job title and summary, the script generates one final visual image using Fal.ai’s recraft-v3 API. The image is saved at the specified output path.

**Run the CLI with:**

```bash
python main.py --folder data/documents/ \
    --output_json data/output/generated_content.json \
    --output_image data/output/job_ad_visual.png
```

- **`--folder`**: Directory containing your input documents.
- **`--output_json`**: File path to save the synthesized job ad content in JSON format.
- **`--output_image`**: File path for the final generated visual image.

### Module Details

- **Data Extraction & Preprocessing (`scripts/extract_text.py`):**  
  Uses PyMuPDF, python-docx, and Python’s built-in I/O to extract text from PDFs, DOCX, and TXT files. The output is a JSON structure with file names and lists of paragraphs.

- **Content Synthesis (LLM Processing) (`scripts/synthesize_content.py`):**  
  Utilizes LangChain with OpenAI's GPT (e.g., gpt-3.5-turbo-instruct) to transform the extracted text into structured content with keys like `job_title`, `summary`, `responsibilities`, etc. The output is in JSON format.

- **Visual Template Creation (`scripts/generate_visual.py`):**  
  Leverages the Fal.ai recraft-v3 API to generate an image based on a prompt (constructed from the job title and summary). The generated image is stored locally.

## Testing

Unit tests are available in the **tests/** directory. To run tests using pytest:

```bash
pytest tests/
```

Tests cover:
- Text extraction functionality.
- LLM-based content synthesis.
- Visual generation process.

## Extending the Project

- **Adding More File Formats:**  
  Extend `scripts/extract_text.py` to support additional file types as needed.

- **Enhancing Content Synthesis:**  
  Incorporate other LLM frameworks (e.g., LlamaIndex, LangGraph, CrewAI) for more advanced processing.

- **Improving Visual Generation:**  
  Integrate a local Stable Diffusion pipeline or additional Fal.ai functionalities to refine visual outputs.