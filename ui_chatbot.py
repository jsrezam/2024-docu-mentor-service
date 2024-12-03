import random
import time
from query_data import query_rag
import gradio as gr


def random_response(message, history):
    response = query_rag(message,stream=False)
    
    for i in range(len(response)):
        time.sleep(0.01)
        yield "You typed: " + response[: i + 1]

ui_chatbot = gr.ChatInterface(random_response, type="messages", autofocus=False)

if __name__ == "__main__":
    ui_chatbot.launch()
