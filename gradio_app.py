import gradio as gr
import random
import time
from fastapi import FastAPI
import uvicorn
from qa import QA


with gr.Blocks() as demo:
    chatbot = gr.Chatbot()
    msg = gr.Textbox()
    clear = gr.ClearButton([msg, chatbot])
    query_runner = QA(file_path='macros.csv')

    state = gr.State(query_runner)

    def respond(message, chat_history):
        # bot_message = query_runner.run_query(message)['answer']
        bot_message = random.choice(["How are you?", "I love you", "I'm very hungry"])
        chat_history.append((message, bot_message))
        time.sleep(1)
        return "", chat_history

    msg.submit(respond, inputs=[msg, chatbot], outputs=[msg, chatbot], )

demo.launch()

# app = FastAPI()
# gradio_app = gr.routes.App.create_app(demo)
# gradio_app.blocks.config["dev_mode"] = False
# app.mount("/", gradio_app)
# uvicorn.run(app, host="0.0.0.0", port=8000)