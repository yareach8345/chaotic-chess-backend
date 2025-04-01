import os
from typing import Final

from dotenv import load_dotenv
from pydantic import SecretStr

load_dotenv()

MONGODB_CONNECTION_STRING: Final[str] = os.environ.get("MONGODB_CONNECTION_STRING")
GPT_MODEL = os.environ.get("GPT_MODEL")