import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DATA_DIR = Path(__file__).parent.parent / "data"
STORAGE_DIR = Path(__file__).parent.parent / "storage"
