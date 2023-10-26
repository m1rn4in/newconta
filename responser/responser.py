import openai
from BotPacifico.settings import get_OpenAI_token
from warnings import warn
import warnings

openai_settings = get_OpenAI_token()
openai.api_key = openai_settings.OPENAI_TOKEN

class Responser:
    
    def __init__(self) -> None:
        pass
    
    def predict(self,text:str,username:str) -> str:

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                    {"role": "user", "content":text}
                ],
            max_tokens = 512,
            stop = f"{username}:"
            )
        a= response["choices"][0]["message"]["content"]

        warn("openai presente")
                    
        return response["choices"][0]["message"]["content"]

