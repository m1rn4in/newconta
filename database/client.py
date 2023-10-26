from pymongo import MongoClient
from BotPacifico.settings import get_database_string_conection_local, get_database_string_conection_nube
import os 
from warnings import warn
import warnings
from bson import ObjectId
#CONNECTION_STRING = get_database_string_conection_local()

#CONNECTION_STRING = os.getenv('AZURE_COSMOS_CONNECTIONSTRING_AI')
#CONNECTION_STRING = os.environ['AZURE_COSMOS_CONNECTIONSTRING_IA']
# if CONNECTION_STRING== None:
#     CONNECTION_STRING = get_database_string_conection_nube()
# print("esta es la base de db: " , CONNECTION_STRING)
# warnings.warn(f"esta es la base de db: {CONNECTION_STRING}")
def get_database():
    client = MongoClient("mongodb://aiinetum-dbserver:S6RliF1tRF6xd0CK0lFe5U0O2MNJ7MeBCEcZj6eQSlMkLxDKhM5CuogYb63RsU4PaST8ZQ55hH8RACDbOnHdEQ==@aiinetum-dbserver.mongo.cosmos.azure.com:10255/?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000&appName=@aiinetum-dbserver@")
    #print("esta es la conection", CONNECTION_STRING)
    #client = MongoClient(CONNECTION_STRING)
    warn("se conecto bien la db:")
    
    return client['dbaiinetumdesa']
