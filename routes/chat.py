from fastapi import APIRouter
from controllers.chat import init, filter_option_main, intWeek, reqTopComments, clientMessage

chat = APIRouter()

chat.get("/chat/init")(init)
chat.post("/chat/filter_option_main/")(filter_option_main)
chat.post("/chat/intWeek/")(intWeek)
chat.post("/chat/reqTopComments/")(reqTopComments)
chat.post("/chat/clientMessage/")(clientMessage)