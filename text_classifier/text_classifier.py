import openai
import ast
from pathlib import Path
from jinja2 import Template
from functools import lru_cache
from BotPacifico.settings import get_OpenAI_token
import os
from warnings import warn
import warnings
import timeit

openai_settings = get_OpenAI_token()

openai.api_key = os.getenv('OPENAI_TOKEN', default = 'None1')


if(openai.api_key == 'None1'):
    openai.api_key = openai_settings.OPENAI_TOKEN

class TextClassifier:
    
    def __init__(self) -> None:
        pass
    
    
    def get_metadata(self):
        
        return {}
    

    @lru_cache
    def get_template(self) -> Template:

        text = Path("text_classifier/templates/classifier.txt.jinja2").read_text()

        return Template(text)
    

    def render_template(self,template:Template,metadata:dict,message:str) -> str:

        return template.render(**metadata,message=message)
    

    def predict(self,text:str) -> list[int]:

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                    {"role": "user", "content":text}
                ],
            temperature=0.1,
            max_tokens=256,
            top_p=0.9,
            frequency_penalty=0.0,
            presence_penalty=0.0
            )
        warn("usando la IA")       
        return response["choices"][0]["message"]["content"]


    def get_labels(self,message:str) -> dict:

        metadata = self.get_metadata()
        template = self.get_template()
        text = self.render_template(template,metadata,message)
        labels1 = self.predict(text)
        labels = ast.literal_eval(labels1)

        time_metadata = timeit.timeit(lambda: self.get_metadata, number=1)
        warnings.warn(f"time_metadata: {time_metadata}")

        time_template = timeit.timeit(lambda: self.get_template, number=1)
        warnings.warn(f"time_template: {time_template}")

        time_text = timeit.timeit(lambda: self.render_template(template,metadata,message), number=1)
        warnings.warn(f"time_text: {time_text}")

        time_labels1 = timeit.timeit(lambda: self.predict(text), number=1)
        warnings.warn(f"time_labels1: {labels1}")

        time_labels = timeit.timeit(lambda: labels, number=1)
        warnings.warn(f"time_labels: {time_labels}")


        

        return labels

