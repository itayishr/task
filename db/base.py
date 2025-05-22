from dotenv import load_dotenv
load_dotenv()
import os
from databases import Database
from sqlalchemy import MetaData, create_engine

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://entro:entro@db:5432/entro_db")

database = Database(DATABASE_URL)
metadata = MetaData()

engine = create_engine(DATABASE_URL)