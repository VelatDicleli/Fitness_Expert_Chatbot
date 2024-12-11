import uvicorn
from function.workflow import chatbot
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"], 
)



from pydantic import BaseModel

class ChatMessage(BaseModel):
    message: str


@app.post("/chat")
def chat(message: ChatMessage):
    answer = chatbot(message=message.message)
    return answer

