import gradio as gr
from fastapi import FastAPI
import uvicorn
from qa import QA
import os

with gr.Blocks() as demo:
    chatbot = gr.Chatbot()
    msg = gr.Textbox()
    clear = gr.ClearButton([msg, chatbot])
    query_runner = QA(file_path='macros.csv')

    def respond(message, chat_history):
        bot_message = query_runner.run_query(message)['answer']
        chat_history.append((message, bot_message))
        return "", chat_history

    msg.submit(respond, inputs=[msg, chatbot], outputs=[msg, chatbot], )

app = FastAPI()
gradio_app = gr.routes.App.create_app(demo)
gradio_app.blocks.config["dev_mode"] = False
app.mount("/", gradio_app)
uvicorn.run(app, host="0.0.0.0", port=os.environ['API_PORT'])