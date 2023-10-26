from fastapi import FastAPI, Request
from fastapi.responses import Response, JSONResponse,FileResponse
from BotPacifico.settings import get_Teams_settings
from fastapi.responses import FileResponse
import requests

import sys
import traceback
from datetime import datetime
from http import HTTPStatus

from text_classifier.text_classifier import TextClassifier
from context_manager.context_manager import ContextManager
from responser.responser import Responser
from database.client import get_database
from messages.crud import insert_message

import os

text_classifier = TextClassifier()
context_manager = ContextManager()
responser = Responser()
db = get_database()


from botbuilder.core import (
    BotFrameworkAdapterSettings,
    TurnContext,
    BotFrameworkAdapter,
)
from botbuilder.schema import Activity, ActivityTypes

from teams import TeamsBot

teams_settings = get_Teams_settings()
SETTINGS = BotFrameworkAdapterSettings(teams_settings.TEAMS_APP_ID, teams_settings.TEAMS_APP_PASSWORD)
ADAPTER = BotFrameworkAdapter(SETTINGS)

app = FastAPI(title="A powerful API for Pacifico Bot")
# def upload_(file_path: str, upload_url: str) -> bool:
#     try:
#         with open(file_path, "rb") as file:
#             response = requests.put(upload_url, data=file)
#         if response.status_code == 200:
#             return True
#         else:
#             return False
#     except Exception as e:
#         print(f"Error al subir el archivo: {str(e)}")
#         return False

#####
# def is_teams_request(req: Request) -> bool:
#     # Esta función verifica si la solicitud proviene de Microsoft Teams o no.
#     # Puedes personalizar esta lógica según las características que necesites.
#     return "Authorization" in req.headers


# Catch-all for errors.
async def on_error(context: TurnContext, error: Exception):
    # This check writes out errors to console log .vs. app insights.
    # NOTE: In production environment, you should consider logging this to Azure
    #       application insights.
    print(f"\n [on_turn_error] unhandled error: {error}", file=sys.stderr)
    traceback.print_exc()
    context_dict = context.activity.as_dict()
    user_name = context_dict["from_property"]["name"]
    # Send a message to the user
    await context.send_activity(f"{user_name} podrías darme mas información?")

ADAPTER.on_turn_error = on_error
# Create the Bot
BOT = TeamsBot()
app = FastAPI(title="A powerful API for Pacifico Bot")

async def on_message_activity(self, turn_context: TurnContext):

        

        return await turn_context.send_activity(MessageFactory.text(message))

@app.post(path='/api/messages')
async def messages(req: Request) -> Response:
    # # Main bot message handler.
    # if "application/json" in req.headers["Content-Type"]:
    #     body = await req.json()
    # else:
    #     return Response(status=HTTPStatus.UNSUPPORTED_MEDIA_TYPE)
    
    # activity = Activity().deserialize(body)
    # auth_header = req.headers["Authorization"] if "Authorization" in req.headers else ""

    # response = await ADAPTER.process_activity(activity, auth_header, BOT.on_turn)
    # if response:
    #     return JSONResponse(content=response.body, status_code=response.status)
    # return Response(status_code=HTTPStatus.OK)


    # if is_teams_request(req):
    #     # Si la solicitud proviene de Microsoft Teams, procesa la actividad utilizando el BotFrameworkAdapter
    #     if "application/json" in req.headers["Content-Type"]:
    #         #body = await req.json()
    #         body = req.json()
    #         print(body)
    #     else:
    #         return Response(status=HTTPStatus.UNSUPPORTED_MEDIA_TYPE)

    #     activity = Activity().deserialize(body)
    #     auth_header = req.headers["Authorization"] if "Authorization" in req.headers else ""

    #     response = await ADAPTER.process_activity(activity, auth_header, BOT.on_turn)
    #     if response:
    #         return JSONResponse(content=response.body, status_code=response.status)
    #     return Response(status_code=HTTPStatus.OK)
    # else:
    #     # Si la solicitud no proviene de Microsoft Teams, procesa la solicitud directamente en FastAPI.
    #     # Aquí puedes manejar la lógica para procesar la solicitud según tus necesidades.
    #     #print(activity.message)
    #     return JSONResponse(content={"message": activity.text}, status_code=200)
    body = await req.json()
    user_name = "mirna"

    user_message_data = {
            "text":body["message"],
            "date":datetime.utcnow(),
            "user_type":"Employee"
        }
    print( "pregunta", user_message_data["text"] )
    insert_message(db,user_message_data.copy())

    labels = text_classifier.get_labels(body["message"])
    print(labels)
    # message_with_context,images = context_manager.build_context(db,body["message"],labels,user_name)
    message_with_context = context_manager.build_context(db,body["message"],labels,user_name)
    #print("your message with context",message_with_context)
    user_message_data["text"] = responser.predict(message_with_context,user_name)
    #print("este es el texto de user_message", user_message_data["text"])
    user_message_data["date"]= datetime.utcnow()
    #print("este es el date de user_message", user_message_data["date"])
    user_message_data["user_type"] = "IA"
    
    insert_message(db,user_message_data.copy())

    message  = user_message_data["text"]
    # images_urls = [f"https://storage.googleapis.com/pacifico-bot-media/images/{img['nombre']}" for img in images]
    # images_descriptions = [f"**{img['alt']} en Pacifico**" for img in images]

    # for img_url, img_description in zip(images_urls, images_descriptions):
    #         message += f"\n\n{img_description}\n\n"
    #         message += f"![]({img_url})"

    #print(message)
    return JSONResponse(content={"message": message}, status_code=200)
    
@app.route('/prueba')
def hello():
     return 'holi'



@app.get(path="/api/images/{image_name}")
async def get_image(image_name:str) -> FileResponse:
    return FileResponse(path=f"database/images/{image_name}",status_code=200)