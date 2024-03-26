from pydantic import BaseModel
from fastapi.responses import JSONResponse
from datetime import datetime
import pandas as pd
from excel_process.filter1 import filter_region_week, count_tfv_visits
""" from ia.comment_sentiment_analyzer2 import analyze_comments """
from ia.comment_sentiment_analyzer3 import analyze_comments

conversation_main = {}

def newConversation():
    current_date = datetime.now().strftime('%Y-%m-%d %H:%M')
    conversation = {
        "status": "new",
        "id": "1",
        "date_init": str(current_date),
        "date_updete": str(current_date),
        "date_end": "",
        "messages": []
    }
    return conversation

def addMessageConversation(conversation, message):
    current_date = datetime.now().strftime('%Y-%m-%d %H:%M')
    conversation["messages"].append(message)
    conversation["date_updete"] = str(current_date)
    return conversation

class Message(BaseModel):
    user: str
    message: str
    date: str
    add_type: str
    sequence: int

def clientMessage(message: Message):
    print('client message:', message)
    secuence = message.sequence
    if secuence == 1:
        regional = Regional(regional=message.message)
        return intRegional(regional)
    if secuence == 2:
        week = Week(week=message.message)
        return intWeek(week)
    if secuence == 3:
        if message.message == "si":
            return reqComments()
        if message.message == "no":
            current_date = datetime.now().strftime('%Y-%m-%d %H:%M')
            body = {
                "user": "Bot",
                "message": "Ok, hasta luego",
                "date": str(current_date),
                "add_type": "none"
            }
            conv = addMessageConversation(conversation_main, body)
            print(conv)
            return JSONResponse(status_code=200, content=body)
    current_date = datetime.now().strftime('%Y-%m-%d %H:%M')
    body = {
        "user": "Bot",
        "message": 'No entiendo tu mensaje',
        "date": str(current_date),
        "add_type": "none"
    }
    return JSONResponse(status_code=200, content=body)

def init():
    global conversation_main
    conversation_main = newConversation()
    current_date = datetime.now().strftime('%Y-%m-%d %H:%M')
    body = {
        "user": "Bot",
        "message": """
            ¡Hola Juan! 
            Ingresa el código del regional que deseas consultar
        """,
        "date": str(current_date),
        "add_type": "none"
    }
    conv = addMessageConversation(conversation_main, body)
    print(conv)
    return JSONResponse(status_code=200, content=body)

regional_main = ""

class Regional(BaseModel):
    regional: str

def intRegional(regional: Regional):
    global conversation_main
    global regional_main
    regional_main = regional.regional
    current_date = datetime.now().strftime('%Y-%m-%d %H:%M')
    body = {
        "user": "Bot",
        "message": regional.regional,
        "date": str(current_date),
        "add_type": "none"
    }
    conv = addMessageConversation(conversation_main, body)
    print(conv)
    return reqWeek()

def reqWeek():
    global conversation_main
    current_date = datetime.now().strftime('%Y-%m-%d %H:%M')
    body = {
        "user": "Bot",
        "message": "Ingresa la semana que deseas consultar",
        "date": str(current_date),
        "add_type": "none"
    }
    conv = addMessageConversation(conversation_main, body)
    print(conv)
    return JSONResponse(status_code=200, content=body)

week_main = ""
data_filtered_main = pd.DataFrame()

class Week(BaseModel):
    week: str
    
def intWeek(week: Week):
    global conversation_main
    global regional_main
    global week_main
    global data_filtered_main
    week_main = week.week
    print("Regional: ", regional_main)
    print("Week: ", week_main)
    data_filtered_main = filter_region_week(regional_main, int(week_main))
    data_filtered_main = analyze_comments(data_filtered_main)
    result = count_tfv_visits(data_filtered_main)
    current_date = datetime.now().strftime('%Y-%m-%d %H:%M')
    body = {
        "user": "Bot",
        "message": """
            Te mostraré el resumen de tu consulta para regional {} y semana {}:""".format(regional_main, week_main),
        "date": str(current_date),
        "add_type": "tables",
        "add_data": [result.to_dict(orient="records")],
        "messageEnd": "¿Deseas ver el resumen de comentarios?"
    }
    conv = addMessageConversation(conversation_main, body)
    print(conv)
    return JSONResponse(status_code=200, content=body)

def reqComments():
    global conversation_main
    global data_filtered_main
    current_date = datetime.now().strftime('%Y-%m-%d %H:%M')
    """ comments = analyze_comments(data_filtered_main) """
    comments = data_filtered_main[['Concatenado', 'label', 'score']]
    top_positive_comments, top_negative_comments = filter_top_comments(comments)
    combined_json = create_json(comments, top_positive_comments, top_negative_comments)
    print('combined_json: ')
    print(combined_json)
    body = {
        "user": "Bot",
        "message": """
        Te mostraré los 10 comentarios mas relevates negativos y los 10 mas positivos:""",
        "date": str(current_date),
        "add_type": "tables",
        "add_data": [combined_json['top_positive_comments'],combined_json['top_negative_comments']],
        "messageEnd": "¿Deseas realizar otra consulta?"
    }
    conv = addMessageConversation(conversation_main, body)
    print(conv)
    return JSONResponse(status_code=200, content=body)

def filter_top_comments(comments):
    positive_comments = comments[comments['label'] == 'positive']
    negative_comments = comments[comments['label'] == 'negative']
    top_positive_comments = positive_comments.sort_values(by='score', ascending=False)[['Concatenado', 'label', 'score']].head(10)
    top_negative_comments = negative_comments.sort_values(by='score', ascending=False)[['Concatenado', 'label', 'score']].head(10)
    top_positive_comments['score'] = (top_positive_comments['score'] * 100).round().astype(int).astype(str) + '%'
    top_negative_comments['score'] = (top_negative_comments['score'] * 100).round().astype(int).astype(str) + '%'
    top_positive_comments = top_positive_comments.rename(columns={'Concatenado': 'Comentario'})
    top_negative_comments = top_negative_comments.rename(columns={'Concatenado': 'Comentario'})
    return top_positive_comments, top_negative_comments

def create_json(comments, top_positive_comments, top_negative_comments):
    comments_list = comments.to_dict(orient='records')
    top_positive_comments_list = top_positive_comments.to_dict(orient='records')
    top_negative_comments_list = top_negative_comments.to_dict(orient='records')
    combined_json = {
        'top_negative_comments': top_positive_comments_list,
        'top_positive_comments': top_negative_comments_list
    }
    return combined_json



