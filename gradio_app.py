from fastapi.responses import JSONResponse
import gradio as gr
from qa import QA
import uvicorn
from fastapi import FastAPI, Header, HTTPException, status
import os
from dotenv import load_dotenv

load_dotenv()


with gr.Blocks() as demo:
    chatbot = gr.Chatbot()
    msg = gr.Textbox()
    clear = gr.ClearButton([msg, chatbot])
    qa = QA('macros.csv')
    chat_history = []
    
    def respond(questions, chat_history):
        bot_answer = qa.run_chain(questions, chat_history)
        chat_history.append([questions, bot_answer])
        return "", chat_history

    msg.submit(
        respond,
        inputs=[msg, chatbot],
        outputs=[msg, chatbot],
    )


app = FastAPI()
gradio_app = gr.routes.App.create_app(demo)
gradio_app.blocks.config["dev_mode"] = False

@app.middleware("http")
async def authenticate(request, call_next):
    auth_header = request.headers.get("Authorization")
    if auth_header != f"Bearer {os.getenv('TOKEN')}":
        response = await call_next(request)
        return JSONResponse(content='Invalid authentication token', status_code=status.HTTP_401_UNAUTHORIZED)
    response = await call_next(request)
    return response

app.mount("/", gradio_app)
uvicorn.run(app, host="0.0.0.0", port=int(os.getenv('API_PORT', 8000)))
