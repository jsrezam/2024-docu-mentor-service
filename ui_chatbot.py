import time
import gradio as gr
from api_consumer import execute_rag_query


def random_response(message, history):
    response = execute_rag_query(url = "http://localhost:8000/run_subprocess_async",query_text= message)
    for i in range(len(response)):
        time.sleep(0.01)
        yield "chatbot: " + response[: i + 1]

ui_chatbot = gr.ChatInterface(random_response, type="messages", autofocus=False)

if __name__ == "__main__":
    ui_chatbot.launch()
