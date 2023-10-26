from fastapi import FastAPI, Request
from fastapi.responses import Response, JSONResponse,FileResponse
from BotPacifico.settings import get_Teams_settings

import sys
import traceback
from datetime import datetime
from http import HTTPStatus
import os

from warnings import warn
import warnings


from botbuilder.core import (
    BotFrameworkAdapterSettings,
    TurnContext,
    BotFrameworkAdapter,
)
from botbuilder.schema import Activity, ActivityTypes

from teams import TeamsBot

import logging


teams_settings = get_Teams_settings()

TEAMS_APP_ID = os.getenv('TEAMS_APP_ID')
if TEAMS_APP_ID == None:
    TEAMS_APP_ID = teams_settings.TEAMS_APP_ID
TEAMS_APP_PASSWORD = os.getenv('TEAMS_APP_PASSWORD')
if TEAMS_APP_PASSWORD == None:
    TEAMS_APP_PASSWORD = teams_settings.TEAMS_APP_PASSWORD
SETTINGS = BotFrameworkAdapterSettings(TEAMS_APP_ID, TEAMS_APP_PASSWORD)
ADAPTER = BotFrameworkAdapter(SETTINGS)

# Catch-all for errors.
async def on_error(context: TurnContext, error: Exception):
    # This check writes out errors to console log .vs. app insights.
    # NOTE: In production environment, you should consider logging this to Azure
    #       application insights.
    print("hay un error1")
    print(f"\n [on_turn_error] unhandled error: {error}", file=sys.stderr)
    traceback.print_exc()
    context_dict = context.activity.as_dict()
    print("hay error 2")
    warn("hay un error mirna! help me ")
    user_name = context_dict["from_property"]["name"]
    print("el user es: ", user_name)
    # Send a message to the user
    await context.send_activity(f"{user_name} podrías darme mas información?")

ADAPTER.on_turn_error = on_error
# Create the Bot
BOT = TeamsBot()
app = FastAPI(title="A powerful API for Pacifico Bot")


@app.post(path='/api/messages')
async def messages(req: Request) -> Response:
    # Main bot message handler.
    context: TurnContext
    if "application/json" in req.headers["Content-Type"]:
        print("encuentro application/json")
        body = await req.json()
        
       #warnings.warn(f"Todo bien por aquí, encontramos el JSON de la app: {body}" )


    else:
        return Response(status=HTTPStatus.UNSUPPORTED_MEDIA_TYPE)
        print("no encuentro application/json")
        #warn("no encuentro el json! mirna, ayuda")
    
    activity = Activity().deserialize(body)
    auth_header = req.headers["Authorization"] if "Authorization" in req.headers else ""

    response = await ADAPTER.process_activity(activity, auth_header, BOT.on_turn)
    if response:
        return JSONResponse(content=response.body, status_code=response.status)
        warn("habemus respuest!")
    return Response(status_code=HTTPStatus.OK)


@app.get(path="/api/images/{image_name}")
async def get_image(image_name:str) -> FileResponse:

    return FileResponse(path=f"database/images/{image_name}",status_code=200)

@app.get("/")
def read_root():
    return {"Hello": "World"}


