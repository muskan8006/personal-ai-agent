import os
from dotenv import load_dotenv
load_dotenv()
class Config:
    APP_NAME = os.getenv("APP_NAME", "PersonalAI")
    ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
    SECURITY_LEVEL = os.getenv("SECURITY_LEVEL", "high")