from .base import *
import os
from dotenv import load_dotenv
load_dotenv(dotenv_path=os.path.join(BASE_DIR, ".env"))

SECRET_KEY = os.getenv("SECRET_KEY")
DEBUG = os.getenv("DEBUG")

ALLOWED_HOSTS = ["*"]




CORS_ALLOW_ALL_ORIGINS = True

CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    "http://localhost:8000",
    "http://127.0.0.1:8000",

    "https://20.55.77.52",
    "https://localhost:3020",
    "http://localhost:3020",
    "https://998c-2405-201-5003-2178-aee6-a616-8f9e-f422.ngrok-free.app",
 
    
    

]

CORS_ALLOW_HEADERS = [
    "ngrok-skip-browser-warning",
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
    # "access-control-allow-origin",
    "Authorization",
    
]
