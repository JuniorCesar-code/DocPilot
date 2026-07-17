# 📄 DocPilot — KI-gestützter Docstring Generator

DocPilot is an AI-powered web application that automatically generates Python docstrings from uploaded `.py` files. It uses a FastAPI backend connected to the GWDG Chat AI LLM API (AcademicCloud) and a responsive single-page HTML frontend.

---

## 🗂️ Project Structure

```
DocPilot/
├── Backend/
│   ├── main.py              # FastAPI backend — API routes + LLM integration
│   ├── requirements.txt     # Python dependencies
│   ├── .env                 # API key (never commit this!)
│   └── .env.example         # Template for the .env file
└── frontend/
    └── Frontend_Docpilot.html  # Single-page frontend UI
```

---

## ⚙️ How It Works

1. The user uploads a `.py` file via the web interface
2. The backend parses the file using Python's `ast` module and extracts all functions
3. For each function, the source code and parameters are sent to the GWDG LLM API
4. The LLM generates a PEP 257-compliant docstring
5. The frontend rebuilds the full Python file with docstrings inserted and offers a download

---

## 🚀 Getting Started

### Prerequisites

- Python 3.11 or 3.12 (recommended)
- A GWDG / AcademicCloud account with API access to the KISSKI LLM service
- Git

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd DocPilot
```

### 2. Create and activate a virtual environment

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS / Linux
python -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
cd Backend
pip install -r requirements.txt
```

### 4. Configure your API key

Create a `.env` file inside the `Backend/` folder:

```bash
cp .env.example .env
```

Then open `.env` and fill in your GWDG API key:

```
GWDG_API_KEY=your-api-key-here
```

> To get an API key, request access at [https://kisski.gwdg.de](https://kisski.gwdg.de) under **LLM Service → Book**.

### 5. Start the backend

```bash
cd Backend
uvicorn main:app --reload
```

### 6. Open the application

Open your browser and go to:

```
http://127.0.0.1:8000/ui
```

---

## 🔌 API Endpoints

| Method | Endpoint  | Description |
|--------|-----------|-------------|
| GET    | `/`       | Health check — confirms the backend is running |
| GET    | `/ui`     | Serves the frontend HTML interface |
| POST   | `/upload` | Accepts a `.py` file and returns generated docstrings |

### POST `/upload` — Request

- Content-Type: `multipart/form-data`
- Body: a `.py` file under the key `file`

### POST `/upload` — Response

```json
{
  "filename": "example.py",
  "functions_found": 2,
  "functions": [
    {
      "name": "add",
      "parameters": ["a", "b"],
      "line": 1,
      "generated_docstring": "Return the sum of a and b."
    }
  ]
}
```

---

## 🎨 Frontend Features

- **Drag & drop** or click-to-browse file upload (`.py` files only)
- **Three docstring styles** selectable via cards:
  - Google style (`Args / Returns`)
  - NumPy style (`Parameters` section)
  - Sphinx style (`:param :returns`)
- **Side-by-side view** of original code and generated documentation
- **Download button** — exports the fully documented `.py` file
- **Fully responsive** — stacks vertically on mobile screens

---

## 🤖 LLM Integration

DocPilot connects to the **GWDG Chat AI API**, which is OpenAI-compatible and hosted by the GWDG data center in Germany.

| Setting     | Value |
|-------------|-------|
| Base URL    | `https://chat-ai.academiccloud.de/v1` |
| Model       | `meta-llama-3.1-8b-instruct` |
| Temperature | `0.2` (focused, deterministic output) |
| Max tokens  | `300` per docstring |

The prompt instructs the model to return only the docstring text — no triple quotes, no extra explanation.

---

## 🔒 Security Notes

- The API key is loaded from a `.env` file using `python-dotenv` — it is never hardcoded
- `.env` is listed in `.gitignore` and must never be committed to version control
- CORS is enabled for all origins (`*`) — restrict this in production

---

## 📦 Dependencies

```
fastapi
uvicorn
openai
python-dotenv
python-multipart
```

Install all with:
```bash
pip install -r requirements.txt
```

---

## 📖 Background

DocPilot was developed as part of the **AI in Software Engineering** course at Universität Duisburg-Essen (SS 2026). It demonstrates the practical integration of large language models into a developer tooling workflow via a lightweight web service architecture.

The LLM infrastructure is provided by [KISSKI](https://kisski.gwdg.de) — the KI-Servicezentrum for sensitive and critical infrastructures, operated by GWDG.

---

## 📄 License

This project was created for academic purposes at Universität Duisburg-Essen.
