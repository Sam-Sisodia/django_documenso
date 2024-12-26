import os
from pathlib import Path
from django.core.exceptions import ImproperlyConfigured

from dotenv import load_dotenv

load_dotenv()
mode = os.getenv("ENVIRONMENT")
print(f"The running mode is : {mode}")

if not mode:
    raise ImproperlyConfigured("No Mode specified for use of project")

if mode == "dev":
    from .development import *
elif mode == "production":
   from settings import production
else:
    raise ImproperlyConfigured(
        "Specify MODE in env_web file, that in which mode you are starting the project"
        " development/production mode"
    )