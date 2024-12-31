from .base import *
import os
from dotenv import load_dotenv
load_dotenv(dotenv_path=os.path.join(BASE_DIR, ".env"))

SECRET_KEY = os.getenv("SECRET_KEY")
DEBUG = os.getenv("DEBUG")

ALLOWED_HOSTS = ["*"]


