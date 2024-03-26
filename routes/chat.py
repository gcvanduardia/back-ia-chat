from fastapi import APIRouter
from controllers.chat import init, intRegional, intWeek, reqComments, clientMessage

chat = APIRouter()

chat.get("/chat/init")(init)
chat.post("/chat/intRegional/")(intRegional)
chat.post("/chat/intWeek/")(intWeek)
chat.post("/chat/reqComments/")(reqComments)
chat.post("/chat/clientMessage/")(clientMessage)