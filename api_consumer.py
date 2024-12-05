import requests
from pydantic import BaseModel
from typing import List

class QueryResponse(BaseModel):
    query_text: str
    response_text: str
    sources: List[str]

class ResponseStructure(BaseModel):
    stdout: QueryResponse
    stderr: str
    returncode: int


def execute_rag_query(url: str,query_text) -> ResponseStructure:
    response = requests.post(url, json={"query_text": query_text})
    response.raise_for_status()
    response = ResponseStructure.model_validate_json(response.text)
    return f"{response.stdout.response_text}\n\nSource:\n\n{response.stdout.sources}" 




# Iterate over the response in chunks and print the output
# for chunk in response.iter_content(chunk_size=1, decode_unicode=True):
#     print(chunk, end="", flush=True)


# import requests

# def test_upload_pdf():
#     url = "http://127.0.0.1:8000/upload-files"
#     # List of files to upload
#     files = [
#         ("files", ("document1.pdf", open("document1.pdf", "rb"), "application/pdf")),
#         ("files", ("document2.pdf", open("document2.pdf", "rb"), "application/pdf")),
#     ]
    
#     # Sending the POST request with files
#     response = requests.post(url, files=files)
    
#     # Print the response from the server
#     print("Status Code:", response.status_code)
#     print("Response JSON:", response.json())

# # Run the test
# test_upload_pdf()


if __name__ == "__main__":
    execute_rag_query("Give me some bullet points about HRC?")
