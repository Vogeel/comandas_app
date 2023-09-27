from dotenv import load_dotenv
import os

# Carrega o arquivo .env
load_dotenv(".env")

# Configurações da APP
HOST = os.getenv("HOST")
PORT = os.getenv("PORT")
DEBUG = os.getenv("DEBUG")