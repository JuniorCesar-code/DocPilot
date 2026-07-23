from fastapi import FastAPI, UploadFile
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import ast
import os
from dotenv import load_dotenv
load_dotenv()  # ← add this right below the imports
from openai import OpenAI

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── GWDG Chat AI client ────────────────────────────────────────────────────────

client = OpenAI(
    api_key=os.environ.get("GWDG_API_KEY", ""),
    base_url="https://chat-ai.academiccloud.de/v1",
)
MODEL = "meta-llama-3.1-8b-instruct"


def generate_docstring(func_name: str, params: list[str], source_code: str) -> str:
    """Call the GWDG LLM and return a PEP 257 docstring for the given function. 
    
    Return ONLY the docstring text (without the triple quotes), nothing else.
    
    Function name : func_name
    Parameters    : params
    Source code   : source_code
    
    The function generates a PEP 257-compliant docstring based on the provided function name, parameters, and source code.
    
    Parameters
    ----------
    func_name : type
        Beschreibung von func_name.
    params : type
        Beschreibung von params.
    source_code : type
        Beschreibung von source_code.
    
    Returns
    -------
    type
        Beschreibung.
    """
    """Call the GWDG LLM and return a PEP 257 docstring for the given function."""
    prompt = (
        f"Write a concise PEP 257-compliant Python docstring for the following function.\n"
        f"Return ONLY the docstring text (without the triple quotes), nothing else.\n\n"
        f"Function name : {func_name}\n"
        f"Parameters    : {', '.join(params) if params else 'none'}\n\n"
        f"Source code:\n{source_code}"
    )
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert Python developer. "
                        "You write clear, accurate PEP 257-compliant docstrings."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
            max_tokens=300,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"[Docstring generation failed: {e}]"


def extract_function_source(code: str, node: ast.FunctionDef) -> str:
    """Extract the raw source lines for a single function node.
    
    Parameters
    ----------
    code : type
        Beschreibung von code.
    node : type
        Beschreibung von node.
    
    Returns
    -------
    type
        Beschreibung.
    """
    """Extract the raw source lines for a single function node."""
    lines = code.splitlines()
    # end_lineno is available in Python 3.8+
    end = getattr(node, "end_lineno", node.lineno + 10)
    return "\n".join(lines[node.lineno - 1 : end])


# ── Routes ─────────────────────────────────────────────────────────────────────

@app.get("/")
def hello():
    """Returns a dictionary with a message indicating the status of the DocPilot backend.
    
    Returns
    -------
    type
        Beschreibung.
    """
    return {"message": "DocPilot backend is running!"}

@app.get("/ui")
def serve_ui():
    """Serve the frontend UI.
    
    Serves the frontend UI by returning a FileResponse object pointing to the Frontend_Docpilot.html file.
    
    Returns
    -------
    type
        Beschreibung.
    """
    return FileResponse("../frontend/Frontend_Docpilot.html")



@app.post("/upload")
async def upload_file(file: UploadFile):
    # ── Validation ────────────────────────────────────────────────────────────
    if not file.filename.endswith(".py"):
        return {"error": "Please upload a Python file (.py only)"}

    content = await file.read()

    if len(content) == 0:
        return {"error": "The file is empty"}

    code = content.decode("utf-8")

    try:
        tree = ast.parse(code)
    except SyntaxError:
        return {"error": "Invalid Python file"}

    # ── Extract functions & generate docstrings ───────────────────────────────
    functions = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            params = [arg.arg for arg in node.args.args]
            source = extract_function_source(code, node)
            docstring = generate_docstring(node.name, params, source)

            functions.append({
                "name": node.name,
                "parameters": params,
                "line": node.lineno,
                "generated_docstring": docstring,
            })

    return {
        "filename": file.filename,
        "functions_found": len(functions),
        "functions": functions,
    }