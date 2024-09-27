import dotenv
from sqlmodel import SQLModel, create_engine
import os
dotenv.load_dotenv()
DATABASE_URL=os.getenv("DATABASE_URL")

engine=create_engine(DATABASE_URL, echo= True)

def create_db_tables():
    SQLModel.metadata.create_all(engine)

