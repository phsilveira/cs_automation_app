from fastapi.responses import JSONResponse
import gradio as gr
from qa import QA
import uvicorn
from fastapi import FastAPI, Header, HTTPException, status
import os
from dotenv import load_dotenv
import logging.config
import time
from uvicorn.config import LOGGING_CONFIG

load_dotenv()

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

last_message = {
    "question": "",
    "created_at": "",
    "answer": "",
    "duration": 0
}

with gr.Blocks() as demo:
    chatbot = gr.Chatbot()
    msg = gr.Textbox()
    clear = gr.ClearButton([msg, chatbot])
    qa = QA('macros.csv')
    chat_history = []
    brand = gr.Textbox()

    def respond(questions, chat_history, brand):
        start_time = time.time()
        
        bot_answer = qa.run_chain(questions, chat_history, brand)
        last_3_messages = [message[1] for message in chat_history[-3:]]

        if len(last_3_messages) > 2:
            if (last_3_messages[0] == last_3_messages[1] == last_3_messages[2]):
                bot_answer = "[Click here](#escalate) to escalate to an agent."
                chat_history.append([questions, bot_answer])
                return bot_answer, chat_history
        
        chat_history.append([questions, bot_answer])

        end_time = time.time()
        duration = end_time - start_time

        last_message["question"] = questions
        last_message["answer"] = bot_answer
        last_message["duration"] = duration
        last_message["created_at"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        return bot_answer, chat_history

    msg.submit(
        respond,
        inputs=[msg, chatbot, brand],
        outputs=[msg, chatbot],
    )


app = FastAPI()
gradio_app = gr.routes.App.create_app(demo)
gradio_app.blocks.config["dev_mode"] = False

@app.middleware("http")
async def authenticate(request, call_next):
    auth_header = request.headers.get("Authorization")
    if auth_header != f"Bearer {os.environ.get('TOKEN')}":
        response = await call_next(request)
        return JSONResponse(content='Invalid authentication token', status_code=status.HTTP_401_UNAUTHORIZED)
    response = await call_next(request)
    return response

@app.get("/health-check")
async def health_check():
    return last_message

app.mount("/", gradio_app)
LOGGING_CONFIG["formatters"]["default"]["fmt"] = "%(asctime)s [%(name)s] %(levelprefix)s %(message)s"
uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get('API_PORT', 8501)))