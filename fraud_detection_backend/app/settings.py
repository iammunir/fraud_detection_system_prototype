from dotenv import load_dotenv
import os
from os.path import join, dirname

dotenv_path = join(dirname(__file__), '..', '.env')

if os.path.exists(dotenv_path):
    load_dotenv()

class Config:
    RETHINK_HOST = os.getenv('RETHINK_HOST')
    RETHINK_PORT = int(os.getenv('RETHINK_PORT'))
    RETHINK_DB = os.getenv('RETHINK_DB')
    POSTGRES_URI = f"postgresql+psycopg2://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
    CELERY_BROKER = f"redis://{':' + os.getenv('REDIS_PASSWORD') + '@' if os.getenv('REDIS_PASSWORD') else ''}{os.getenv('REDIS_HOST')}:{os.getenv('REDIS_PORT')}/{os.getenv('REDIS_DB_BROKER')}"
    CELERY_BACKEND = f"redis://{':' + os.getenv('REDIS_PASSWORD') + '@' if os.getenv('REDIS_PASSWORD') else ''}{os.getenv('REDIS_HOST')}:{os.getenv('REDIS_PORT')}/{os.getenv('REDIS_DB_BACKEND')}"