import os
import ast
from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI  # Nutzung des OpenAI-Clients für AcademicCloud

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class GenerateRequest(BaseModel):
    name: str
    parameters: list[str]
    style: str

# Konfiguration des Clients mit dem AcademicCloud-Endpunkt
client = OpenAI(
    base_url="https://chat-ai.academiccloud.de/v1",
    api_key=os.environ.get("OPENAI_API_KEY")
)

@app.get("/")
def hello():
    return {"message": "DocGen-Backend läuft erfolgreich auf der AcademicCloud!"}

@app.post("/upload")
async def upload_file(file: UploadFile):
    if not file.filename.endswith(".py"):
        raise HTTPException(status_code=400, detail="Bitte laden Sie nur eine Python-Datei (.py) hoch.")

    content = await file.read()
    if len(content) == 0:
        raise HTTPException(status_code=400, detail="Die hochgeladene Datei ist leer.")

    code = content.decode("utf-8")

    try:
        tree = ast.parse(code)
    except SyntaxError:
        raise HTTPException(status_code=400, detail="Ungültige Python-Datei (Syntaxfehler).")

    functions = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            params = [arg.arg for arg in node.args.args]
            functions.append({
                "name": node.name,
                "parameters": params,
                "line": node.lineno
            })

    return {
        "filename": file.filename,
        "functions_found": len(functions),
        "functions": functions
    }

@app.post("/generate")
async def generate_docstring(request: GenerateRequest):
    params_str = ", ".join(request.parameters) if request.parameters else "keine Parameter"
    
    prompt = (
        f"Du bist ein Experte für Python-Dokumentation.\n"
        f"Generiere ausschließlich den Docstring für die folgende Funktion im '{request.style}'-Stil.\n\n"
        f"Funktionsdetails:\n"
        f"- Name: {request.name}\n"
        f"- Parameter: {params_str}\n\n"
        f"Strikte Anweisungen:\n"
        f"1. Gib keinen Funktionscode zurück, sondern nur den Docstring in dreifachen Anführungszeichen (z. B. \"\"\" dein Docstring \"\"\").\n"
        f"2. Schreibe keine Erklärungen oder Begrüßungen außerhalb des Docstrings.\n"
        f"3. Verfasse die Beschreibungen der Parameter und Rückgabewerte auf Deutsch."
    )

    try:
        # LLM-Aufruf über AcademicCloud mit dem funktionierenden Modell
        response = client.chat.completions.create(
            model="qwen3-coder-next",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
        )
        
        generated_docstring = response.choices[0].message.content.strip()
        
        # Bereinigung von Markdown-Codeblöcken, falls das LLM welche generiert
        if generated_docstring.startswith("```"):
            lines = generated_docstring.splitlines()
            if lines[0].startswith("```"):
                lines.pop(0)
            if lines and lines[-1].startswith("```"):
                lines.pop()
            generated_docstring = "\n".join(lines).strip()
            
        return {"docstring": generated_docstring}

    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"AcademicCloud-Fehler: {str(e)}. Bitte API-Schlüssel überprüfen."
        )