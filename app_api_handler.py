from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel
from query_data import query_rag
from populate_database import main
from fastapi.responses import StreamingResponse
from typing import List
from fastapi.middleware.cors import CORSMiddleware
import subprocess
import os


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
UPLOAD_DIR = "data/"

class QueryRequest(BaseModel):
    text: str

@app.post("/chatbot")
def query(query: QueryRequest):
    query_response = query_rag(query.text)
    return query_response
    # return {"Query Response": query_response}


@app.post("/chatbot-stream")
async def stream_query(query: QueryRequest):
    return StreamingResponse(query_rag(query.text,stream=True), media_type="text/plain")

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
        subprocess.run(["python", 'populate_database.py'])
    return {"saved_files": saved_files}
