import asyncio
import json
import os
import re
import subprocess
from typing import List

import uvicorn
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from query_rag import QueryResponse, query_rag

app = FastAPI()

# Add CORS 
app.add_middleware(    
    CORSMiddleware,    
    allow_origins= ["*"],
    allow_credentials=True,    
    allow_methods=["*"],    
    allow_headers=["*"])

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB limit
ALLOWED_MIME_TYPE = "application/pdf"
UPLOAD_DIR = "data/source"

class SubmitQueryRequest(BaseModel):
    query_text: str

def extract_json(input_text) -> str:
    try:
        json_match = re.search(r'{.*}', input_text, re.DOTALL)
        if json_match:
            json_content = json_match.group()
            # Parse to ensure it's valid JSON
            parsed_json = json.loads(json_content)
            return parsed_json
        else:
            raise ValueError("No JSON content found.")
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON detected: {e}")

@app.post("/chatbot-query")
def submit_query_endpoint(request: SubmitQueryRequest) -> QueryResponse:
    query_response =  query_rag(request.query_text)
    return query_response

@app.post("/upload-files")
async def upload_files(files: List[UploadFile] = File(...)):
    saved_files = []
    for file in files:
        content = await file.read()
        print(f"Filename: {file.filename}, Content-Type: {file.content_type}")
        if len(content) > MAX_FILE_SIZE:
            raise HTTPException(status_code=400, detail=f"File {file.filename} exceeds size limit.")
        if file.content_type != ALLOWED_MIME_TYPE:
            raise HTTPException(
                status_code=400,
                detail=f"File '{file.filename}' is not a valid PDF. Allowed type: {ALLOWED_MIME_TYPE}"
            )
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as f:
            f.write(content)
        saved_files.append({"filename": file.filename, "path": file_path})

    command = ["python", 'db_populate.py']
    process = await asyncio.create_subprocess_exec(
        *command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    return {
        "saved_files": saved_files,
        "stdout": stdout,
        "stderr": stderr.decode(),
        "returncode": process.returncode,
    }

@app.post("/run_subprocess_async/")
async def run_subprocess_async(request: SubmitQueryRequest):
    print(f"\"{request.query_text}\"")
    command = ["python", "query_rag.py", f"\"{request.query_text}\"" ]  # Example long-running command

    # Run the command asynchronously
    process = await asyncio.create_subprocess_exec(
        *command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    extracted_json = extract_json(stdout.decode())
    return {
        "stdout": extracted_json,
        "stderr": stderr.decode(),
        "returncode": process.returncode,
    }

if __name__ == "__main__":
    # Run this as a server directly.
    port = 8000
    print(f"Running the FastAPI server on port {port}.")
    uvicorn.run("app_api_handler:app", host="0.0.0.0", port=port, reload=True)