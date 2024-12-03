# import requests

# url = "http://localhost:8000/chatbot-stream"

# # Send a GET request with stream=True to handle the response incrementally
# response = requests.post(url,json={"text": "how could I play this game ?"}, stream=True)

# # Iterate over the response in chunks and print the output
# for chunk in response.iter_content(chunk_size=1, decode_unicode=True):
#     print(chunk, end="", flush=True)

import requests

def test_upload_pdf():
    url = "http://127.0.0.1:8000/upload-files"
    # List of files to upload
    files = [
        ("files", ("document1.pdf", open("document1.pdf", "rb"), "application/pdf")),
        ("files", ("document2.pdf", open("document2.pdf", "rb"), "application/pdf")),
    ]
    
    # Sending the POST request with files
    response = requests.post(url, files=files)
    
    # Print the response from the server
    print("Status Code:", response.status_code)
    print("Response JSON:", response.json())

# Run the test
test_upload_pdf()
