import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    TOKEN_REQUEST = os.getenv("TOKEN_REQUEST", "helloinitoken")