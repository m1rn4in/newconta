
#Python

#Message
from messages.schemas import MessageCreate, MessageUpdate
from pymongo.database import Database

def insert_message(db:Database, message:dict):

    db["Messages"].insert_one(message)
