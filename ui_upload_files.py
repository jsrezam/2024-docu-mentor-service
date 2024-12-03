# This is a simple Gradio app that allows users to upload files.
import gradio as gr

# Define a function that takes a file and returns a message indicating the file has been uploaded.
def file_uploaded(file):
    return f"File {file.name} has been uploaded!"

# Create a Gradio interface that takes a file input, runs it through the file_uploaded function, and returns output to a textbox.
ui_upload_files = gr.Interface(fn=file_uploaded, inputs="file", outputs="textbox")

# Launch the interface.
if __name__ == "__main__":
    ui_upload_files.launch(show_error=True)