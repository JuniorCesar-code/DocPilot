# DocGen — Test Report

## Person 1 — Backend (Maelle)
Date: 26.06.2026

---

## Endpoint: GET /
**What it does:** Checks that the server is running.

| Test | Expected result | Actual result | Status |
|------|----------------|---------------|--------|
| Call GET / | {"message": "DocGen backend is running!"} | {"message": "DocGen backend is running!"} | ✅ Pass |

---

## Endpoint: POST /upload
**What it does:** Accepts a Python file and returns all functions found inside it.

| Test | Expected result | Actual result | Status |
|------|----------------|---------------|--------|
| Upload valid .py with functions | List of functions as JSON | Returns functions correctly | ✅ Pass |
| Upload .txt file | Error message | "Please upload a Python file" | ✅ Pass |
| Upload .java file | Error message | "Please upload a Python file" | ✅ Pass |
| Upload empty .py file | Error message | "The file is empty" | ✅ Pass |
| Upload .py with no functions | Error message | "No functions found in this file" | ✅ Pass |

---

## API Contract for Person 2 (LLM Integration)

POST /generate expects this JSON input:
{
  "name": "function_name",
  "parameters": ["param1", "param2"],
  "style": "Google"
}

Should return:
{
  "docstring": "generated docstring text here"
}

---

## API Contract for Person 3 (Frontend)

Available endpoints:
- POST /upload → send a .py file, receive list of functions
- POST /generate → send a function, receive a docstring (Person 2 builds this)

CORS is enabled — frontend can call these endpoints directly from the browser.

---

## Known limitations
- Only works with .py files (Python only for now)
- Does not extract return types yet
- Does not extract function body, only name and parameters

---

## How to run the backend

1. Install dependencies:
   pip install fastapi uvicorn python-multipart anthropic python-dotenv

2. Start the server:
   py -m uvicorn main:app --reload

3. Test interface available at:
   http://localhost:8000/docs