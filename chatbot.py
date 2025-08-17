from openai import OpenAI
from fastapi import FastAPI, Form, Request
from typing import Annotated
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse


app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def chat_page(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


openai = OpenAI (
    api_key="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",
)

chat_log = [{'role': 'system',
             'content': "You are Brooklyn's Chatbot. She made you in her personal project. She is pretty and awesome. Always keep your responses short, clear, and to the point. "}]

chat_responses = []
@app.post("/", response_class=HTMLResponse)
async def chat(request: Request, user_input: Annotated[str, Form()]):
    chat_log.append({'role' : 'user', 'content' : user_input})
    chat_responses.append(user_input)

    response = openai.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=chat_log,
        temperature=.7
    )
    bot_response = response.choices[0].message.content
    chat_log.append({'role' : 'assistant', 'content' : bot_response})
    chat_responses.append(bot_response)

    return templates.TemplateResponse("home.html", {"request": request, "chat_responses": chat_responses})