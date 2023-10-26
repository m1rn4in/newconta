# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
from pymongo.database import Database
from botbuilder.core import ActivityHandler, MessageFactory, TurnContext, CardFactory
from botbuilder.schema import ChannelAccount,CardImage,HeroCard,CardAction
from botframework.connector.models import ActionTypes
from datetime import datetime

from text_classifier.text_classifier import TextClassifier
from context_manager.context_manager import ContextManager
from responser.responser import Responser
from database.client import get_database
from messages.crud import insert_message
from warnings import warn
import warnings

text_classifier = TextClassifier()
context_manager = ContextManager()
responser = Responser()
db:Database = get_database()

class TeamsBot(ActivityHandler):
    async def on_members_added_activity(self, 
                                        members_added:list[ChannelAccount], 
                                        turn_context: TurnContext):
        for member in members_added:
            if member.id != turn_context.activity.recipient.id:
                await turn_context.send_activity("Hello and welcome!")
                warn("miembros adicionados")

    async def on_message_activity(self, turn_context: TurnContext):
        context_dict = turn_context.activity.as_dict()
        print("context_dict:", turn_context.activity.from_property)
        user_name_complete = context_dict["from_property"]["name"]
        user_id = turn_context.activity.from_property.id
        user_name = user_name_complete.split(" ")[1]
        user_message_data = {
            "text": turn_context.activity.text,
            "user_type": "Employee",
            "user_name_complete": user_name_complete,
            "user_id": user_id
        }
        a = user_message_data
        warnings.warn(f"pregunta {a}")
        insert_message(db, user_message_data.copy())
        
        labels = text_classifier.get_labels(turn_context.activity.text)
        warnings.warn(f"este es el label: {labels}")
        print(labels)

        user = db.Users.find_one({"user_id": user_id})
        doc1 =""
        doc2 =""
        doc3 =""
        print("este es el usuario", user)
        if user and user['Area'] == "Contabilidad":
            doc1 = "TopicosN1Conta"
            doc2 = "TopicosN2Conta"
            doc3 = "TopicosN3Conta"
        elif user and user['Area'] == "RRHH":
            doc1 = "TopicosN1Rrhh"
            doc2 = "TopicosN2Rrhh"
            doc3 = "TopicosN3Rrhh"
        else:
            print("no hay conocimiento")
        message_with_context = context_manager.build_context(
        db, turn_context.activity.text, labels, user_name_complete, doc1, doc2, doc3)
        warnings.warn(message_with_context)
        print(message_with_context)

        user_message_data["text"] = responser.predict(message_with_context, user_name_complete)
        warn("opein respondiendo:")
        user_message_data["date"]= datetime.utcnow()
        user_message_data["user_type"] = "IA"
        #hi

        insert_message(db, user_message_data.copy())

        message = user_message_data["text"]
        print(message)
        warnings.warn(f"este es el mensaje {message}")

        await turn_context.send_activity(MessageFactory.text(message))
