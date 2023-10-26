from datetime import date
from pathlib import Path
from jinja2 import Template
from functools import lru_cache
from pymongo.database import Database
from typing import Tuple
import os
from warnings import warn
import warnings

class ContextManager:
    
    def __init__(self) -> None:
        pass
    
    def get_messages(self, db: Database, user_name: str) -> Tuple[list[dict], bool]:
        collection = db["Messages"]
        document_list = list(reversed(list((collection.find()))))
        las_five = document_list[:5] if len(document_list) >= 5 else document_list
        messages = list(reversed(las_five))
        return messages

    def get_topic_level(self, topic:float) -> list[int]:
        topic = [int(s) for s in topic.split('.')]
        return topic

    def get_knowledge(self,db:Database,labels:dict, doc1:str, doc2:str, doc3:str) -> Tuple[dict,list[str]]:
        knowledge = {}
        if doc1!= "" and doc2!="" and doc3!="":

            for topic, subtopics in labels.items():
                topic_level = self.get_topic_level(topic)
                if len(topic_level) == 1:
                    topic_data = db[doc1].find_one({"T1":topic_level[0]}, None)
                    if topic_data is None:
                        warnings.warn(f"No se encontró un documento válido en la base de datos para '{doc1}'.")
        
                if len(topic_level) == 2:
                    topic_data = db[doc1].find_one({"T1":topic_level[0]})
                    topic_data = db[doc2].find_one({"T1":topic_data["_id"], "T2":topic_level[1]})
                        
                if topic_data:
                    topic_id  = topic_data["_id"]
                    subtopics_data = []
                    for subtopic in subtopics:
                        subtopic_level = self.get_topic_level(subtopic)
                        if len(topic_level) == 1 and len(subtopic_level) == 2:
                            subtopic_data = list(db[doc2].find({"T1":topic_id,"T2":subtopic_level[1]}))
            
                        elif len(topic_level) == 1 and len(subtopic_level) == 3:
                            topic_n2 = db[doc2].find_one({"T1":topic_id,"T2":subtopic_level[1]})
                            subtopic_data = list(db[doc3].find({"T2":topic_n2["_id"],"T3":subtopic_level[2]}))
                    
                        elif len(topic_level) == 2 and len(subtopic_level) == 3:
                            subtopic_data = list(db[doc3].find({"T2":topic_id,"T3":subtopic_level[2]}))

                        else:
                            subtopic_data = []
                        
                        subtopics_data.append(subtopic_data)
                        print("este es el subtopic", subtopics_data )
                    knowledge[topic_data["nombre"]]=subtopics_data
        return knowledge
    
    
    
    def get_user_data(self) -> list[dict]:
        return {"Name":"Mirna"}

    @lru_cache
    def get_template(self) -> Template:

        text = Path("context_manager/templates/context.text.jinja2").read_text()

        return Template(text)
    
    def render_template(self,template:Template,metadata:dict,message:str) -> str:

        return template.render(**metadata,message=message)
    
    def build_context(self, db: Database, message: str, labels: dict, user_name: str, doc1:str, doc2:str, doc3:str) -> Tuple[str, list[str]]:
        knowledge = self.get_knowledge(db, labels, doc1, doc2, doc3)    
        messages= self.get_messages(db, user_name)

        print("este es el mensaje", messages)
        warnings.warn(f"este es el mensaje:{messages}")
        metadata = {
            "messages": messages,
            "knowledge": knowledge,
            "user_name": user_name
        }
        template = self.get_template()
        text_with_context = self.render_template(template, metadata, message)
        
      
        return text_with_context
