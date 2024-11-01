from fastapi import FastAPI, Header, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from qa import QA
import uvicorn
import os
import ast
from dotenv import load_dotenv
import logging.config
import time
from uvicorn.config import LOGGING_CONFIG
from typing import Any, List, Optional
from pydantic import BaseModel



load_dotenv()

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)

last_message = {
    "question": "",
    "created_at": "",
    "answer": "",
    "duration": 0
}

keyword_trigger_list = [
    "File a Complaint",
    "Lawsuit",
    "I will contact my Lawyers",
    "I will contact my Bank",
    "Call the Police",
    "File Charges",
    "Unauthorized charges",
    "Scammer",
    "I will sue you",
    "I will contact Better Business Bureau",
    "Search Warrant",
    "Police Investigation",
    "I will contact the Police Department",
    "Police Authority",
    "[Country] Police",
    "General's Office",
    "Legal Process",
    "Law Enforcement",
    "Criminal Investigation",
]

qa = QA('macros.csv', 'websites.csv')
chat_history = []

app = FastAPI()

def get_bot_answer(qa, questions, chat_history, brand, payload_dict):
    bot_answer = qa.run_chain(questions, chat_history, brand, payload_dict)
    last_3_messages = [message[1] for message in chat_history[-3:]]

    if len(last_3_messages) > 2:
        if (last_3_messages[0] == last_3_messages[1] == last_3_messages[2]):
            bot_answer = "[Click here](#escalate) to escalate to an agent."
            chat_history.append([questions, bot_answer])

    if any(keyword.lower() in questions.lower() for keyword in keyword_trigger_list):
        bot_answer = "[Click here](#escalate) to escalate to an agent."
        chat_history.append([questions, bot_answer])

    return bot_answer, chat_history

class RespondPayload(BaseModel):
    data: List
    fn_index: int
    session_hash: str

class ResponseModel(BaseModel):
    data: List[Any]
    is_generating: bool
    duration: float
    average_duration: float

@app.middleware("http")
async def authenticate(request, call_next):
    auth_header = request.headers.get("Authorization")
    if auth_header != f"Bearer {os.environ.get('TOKEN')}":
        response = await call_next(request)
        return JSONResponse(content='Invalid authentication token', status_code=status.HTTP_401_UNAUTHORIZED)
    response = await call_next(request)
    return response

@app.post("/run/predict")
async def respond(payload: RespondPayload):
    questions, chat_history, brand, payload = payload.data

    logging.debug(f"🔔 Payload: {[questions, chat_history, brand, payload]}")

    start_time = time.time()

    payload_dict = payload
    
    bot_answer, chat_history = get_bot_answer(qa, questions, chat_history, brand, payload_dict)
    
    chat_history.append([questions, bot_answer])

    end_time = time.time()
    duration = end_time - start_time

    last_message["question"] = questions
    last_message["answer"] = bot_answer
    last_message["duration"] = duration
    last_message["created_at"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    logging.debug(f"Last message: {last_message}")

    return {
        "data": [
            bot_answer,
            chat_history
        ],
        "is_generating": False,
        "duration": duration,
        "average_duration": duration
    }


@app.get("/health-check")
async def health_check():
    return last_message

LOGGING_CONFIG["formatters"]["default"]["fmt"] = "%(asctime)s [%(name)s] %(levelprefix)s %(message)s"
# uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get('API_PORT', 8501)))