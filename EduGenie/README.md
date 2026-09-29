# EduGenie — Google Gemini Powered Learning Assistant

EduGenie is a lightweight FastAPI web application based on the supplied project document. It provides:

- Question answering (`/qa`)
- Beginner-friendly concept explanation (`/explain`)
- Three-question MCQ generation (`/quiz`)
- Educational summarization (`/summarize`)
- Beginner-to-advanced learning recommendations (`/learn/recommendations`)

The original document specifies FastAPI, HTML/CSS, Gemini, and a LaMini-Flan-T5 local explanation option. The implementation keeps that architecture but uses Google's current `google-genai` Python SDK and a configurable Gemini model. The default model can be changed in `.env` without editing application code.

## Project structure

```text
EduGenie/
├── main.py
├── config.py
├── gemini_client.py
├── prompts.py
├── qna.py
├── explanation_module.py
├── quiz_module.py
├── summary_module.py
├── learning_path.py
├── requirements.txt
├── requirements-local.txt
├── .env.example
├── README.md
├── templates/
│   └── index.html
├── static/
│   ├── app.js
│   └── style.css
└── tests/
    ├── test_api.py
    └── test_quiz_module.py
```

## VS Code setup

### 1. Install Python

Use Python 3.10 or newer. Verify:

```bash
python --version
```

On Windows, `py --version` is also useful.

### 2. Open the project

In VS Code, open the `EduGenie` folder.

### 3. Create a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 4. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 5. Configure Gemini

Copy `.env.example` to `.env` and put your Google AI Studio Gemini API key in `GEMINI_API_KEY`.

Example:

```env
GEMINI_API_KEY=your_real_key_here
GEMINI_MODEL=gemini-3.8-flash
EXPLANATION_PROVIDER=gemini
```

Never commit `.env` or expose the API key in frontend JavaScript.

## Run

```bash
uvicorn main:app --reload
```

Open:

```text
http://127.0.0.1:8000
```

Health check:

```text
http://127.0.0.1:8000/health
```

## Test

With the virtual environment active:

```bash
pytest -q
```

The tests cover the health endpoint, frontend loading, and quiz JSON validation.

## API examples

Question answering:

```bash
curl -X POST http://127.0.0.1:8000/qa \
  -H "Content-Type: application/json" \
  -d '{"text":"Which is the largest ocean?"}'
```

Quiz:

```bash
curl -X POST http://127.0.0.1:8000/quiz \
  -H "Content-Type: application/json" \
  -d '{"text":"The Pythagoras theorem relates the sides of a right triangle."}'
```

## Optional local LaMini explanation

The project document proposes LaMini-Flan-T5-783M for concept explanation. To enable that option, install:

```bash
pip install -r requirements-local.txt
```

Then set:

```env
EXPLANATION_PROVIDER=local
LOCAL_EXPLANATION_MODEL=MBZUAI/LaMini-Flan-T5-783M
```

The first local request downloads the model from Hugging Face and can require substantial disk space/RAM. The rest of the application can continue using Gemini.

## Troubleshooting

### `GEMINI_API_KEY is not configured`

Make sure the file is named `.env`, is in the project root beside `main.py`, and contains a valid key.

### Gemini model access error

Change `GEMINI_MODEL` to a model currently available to your Google AI Studio/API account. The code does not require a source-code change for this.

### PowerShell will not activate `.venv`

You can either activate from a Command Prompt with `.venv\\Scripts\\activate.bat`, or configure your PowerShell execution policy according to your organization's/device policy.

### Local LaMini is slow

That is expected on CPU. Keep `EXPLANATION_PROVIDER=gemini` for the easiest setup.

## Security notes

- API keys stay on the backend.
- `.env` is ignored by Git.
- User input is sent to the configured Gemini provider for generation.
- This is an educational assistant, so generated answers should still be checked for important academic claims.
