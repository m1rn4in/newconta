from fastapi import APIRouter,Depends
from fastapi.responses import RedirectResponse
from BotPacifico.settings import BotpacificoSettings,get_BotPacifico_settings

# BotPacifico_routes= APIRouter()

# @BotPacifico_routes.get(path="/",
#                         include_in_schema=False)
# def documentation(BotPacifico_settings:BotpacificoSettings=Depends(get_BotPacifico_settings)):
#     return RedirectResponse(url=BotPacifico_settings.BACKEND_HOST +"/docs/")