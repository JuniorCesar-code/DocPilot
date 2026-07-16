from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import ast

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def hello():
    return {"message": "DocGen backend is running!"}

@app.post("/upload")
async def upload_file(file: UploadFile):
    # Check if file is a Python file
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