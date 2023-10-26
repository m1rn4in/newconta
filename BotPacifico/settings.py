
from fastapi_mail import ConnectionConfig
from functools import lru_cache
from pydantic import BaseSettings
from pydantic import EmailStr
import os
from dotenv import load_dotenv
load_dotenv()

class BotpacificoSettings(BaseSettings):
    BACKEND_HOST:str
    APP_TOKEN:str
    class Config:
        env_file =".env"

@lru_cache()
def get_BotPacifico_settings():
    return BotpacificoSettings()


class TokensConfig(BaseSettings):
    SECRET_KEY:str
    JMV_ALGORITHM:str
    TIME_DELTA:int
    class Config:
        env_file = ".env"

@lru_cache()
def get_tokens_config()->TokensConfig:
    return TokensConfig()

class EmailsSettings(BaseSettings):
    MAIL_USERNAME:str
    MAIL_PASSWORD:str
    MAIL_FROM:EmailStr
    MAIL_FROM_NAME:str
    MAIL_PORT:int
    MAIL_SERVER:str
    MAIL_TLS:bool
    MAIL_SSL:bool
    TEMPLATE_FOLDER:str

    class Config:
        env_file = ".env"

@lru_cache()
def get_email_settings():
    email_settings=EmailsSettings()
    return ConnectionConfig(**email_settings.dict())


class DatabaseSettings(BaseSettings):
    AZURE_DB_USER:str
    AZURE_DB_TOKEN:str
    DATABASE_HOST:str
    DATABASE_PORT:str
    DATABASE_NAME:str
    class Config:
        env_file = ".env"

@lru_cache()
def get_database_string_conection_local():
    database_settings = DatabaseSettings()

    conection_string = "mongodb+srv://user:password@dbaiinetumdesa.fm9fqxf.mongodb.net/"
        
    conection_string = conection_string.replace("user", database_settings.DATABASE_USER) \
                                        .replace("password", database_settings.DATABASE_PASSWORD) \
                                        .replace("host", database_settings.DATABASE_HOST) \
                                        .replace("port", database_settings.DATABASE_PORT) \
                                        .replace("database_name", database_settings.DATABASE_NAME)
    
    # conection_string = "mongodb://user:password@host:port/database_name"
   
    return conection_string

def get_database_string_conection_nube():
    database_settings = DatabaseSettings()

    #conection_string = os.getenv('AZURE_COSMOS_CONNECTIONSTRING_AI')

    conection_string = "mongodb://user:host==@auser.mongo.cosmos.azure.com:10255/?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000&appName=@auser@"

    # conection_string = "mongodb://user:password@host:port/database_name" 
    conection_string = conection_string.replace("user", database_settings.AZURE_DB_USER) \
                                        .replace("password", database_settings.AZURE_DB_TOKEN) \
                                        .replace("host", database_settings.DATABASE_HOST) 
    
    

    
    return conection_string
    

   

class OpenAISettings(BaseSettings):
    OPENAI_TOKEN:str
    class Config:
        env_file = ".env"

def get_OpenAI_token() -> OpenAISettings:
    return OpenAISettings()


class TeamsSettings(BaseSettings):
    TEAMS_APP_ID:str
    TEAMS_APP_PASSWORD:str
    class Config:
        env_file = ".env"

def get_Teams_settings() -> TeamsSettings:
    return TeamsSettings()
0
