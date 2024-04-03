from fastapi import APIRouter
from controllers.chat import init, intRegional, intWeek, reqTopComments, clientMessage

chat = APIRouter()

chat.get("/chat/init")(init)
chat.post("/chat/intRegional/")(intRegional)
chat.post("/chat/intWeek/")(intWeek)
chat.post("/chat/reqTopComments/")(reqTopComments)
chat.post("/chat/clientMessage/")(clientMessage)