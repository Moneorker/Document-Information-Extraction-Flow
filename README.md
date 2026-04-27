# Document Information Extraction Flow

Document Information Extraction Flow is a small document-processing app for extracting structured information from PDF files. It combines OCR from PaddleOCR with an LLM-based post-processing step, then writes the result into plain text files based on predefined templates.

The project currently provides a Gradio web UI for:

- Single PDF extraction
- Batch PDF extraction
- Template-based field mapping
- Combined text export for multiple document categories

## Supported Document Types

The current templates support:

- Passport
- Application form
- Transcript
- Diploma / certificate
- English language test documents

Template files are stored in [templates](/E:/projects/FYP/flow/templates).

## How It Works

1. Upload one or more PDF files.
2. The app copies uploaded files into the local `uploads/` directory.
3. PaddleOCR extracts text and layout-related content from the document.
4. A prompt is built from the matching JSON template.
5. The LLM returns structured JSON.
6. The extracted fields are saved to `.txt` files in `output/`.

## Project Structure

```text
flow/
├─ app.py
├─ extract_v_0_4.py
├─ templates/
├─ uploads/
├─ output/
└─ README.md
```

## Requirements

This repository currently depends on:

- Python 3.10+
- [Gradio](https://gradio.app/)
- [OpenAI Python SDK](https://github.com/openai/openai-python)
- [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR)

You will also need access to a compatible LLM endpoint. The code is currently set up to use DashScope-compatible OpenAI-style chat completions.

## Environment Variables

Before running the app, set the following environment variables:

```powershell
$env:DASHSCOPE_API_KEY="your_api_key"
$env:DASHSCOPE_MODEL="qwen3-8b"
$env:DASHSCOPE_BASE_URL="https://dashscope.aliyuncs.com/compatible-mode/v1"
```

Only `DASHSCOPE_API_KEY` is required if you want to use the current defaults for model and base URL.

## Installation

Create and activate a virtual environment, then install dependencies:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install gradio openai paddleocr
```

Depending on your PaddleOCR setup, you may also need extra runtime dependencies required by PaddlePaddle on your machine.

## Run the Web App

Start the Gradio app with:

```powershell
python app.py
```

By default, the app runs on:

- `http://0.0.0.0:7860`

## Output Format

For a single file, the app generates a `.txt` result similar to:

```text
#passport
name: John Doe
date of birth: 2000-01-01
passport number: X1234567
```

For batch processing, the app produces a combined output file with one section per supported document type.

## Template Design

Templates are JSON files with:

- `doc_type`
- `fields`

`fields` can be either:

- A simple list of field names
- A list of objects with `name`, `section`, and `note`

This lets the LLM use extra hints for harder forms such as application documents.

## Notes

- Template matching is filename-based.
- Files that do not match any template will raise an error.
- Output and uploads directories are ignored by Git through `.gitignore`.
- The current codebase does not yet include a locked dependency file such as `requirements.txt`.

## Future Improvements

- Add `requirements.txt` or `pyproject.toml`
- Improve template matching beyond filename keywords
- Add JSON / CSV export
- Add better multilingual UI text handling
- Add tests and sample documents

## License

No license file is included yet. Add a license before publishing for broader reuse.
