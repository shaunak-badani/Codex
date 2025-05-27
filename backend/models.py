from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from schema import Base, User, QuestionAnswer
import os

# DATABASE_URL = "postgresql://postgres:password@localhost:5432/app_db"
POSTGRES_USERNAME=os.getenv('POSTGRESQL_USERNAME')
POSTGRESQL_PASSWORD=os.getenv('POSTGRESQL_PASSWORD')
POSTGRESQL_URL=os.getenv('POSTGRESQL_URL')
POSTGRESQL_DBNAME=os.getenv('POSTGRESQL_DBNAME')
DATABASE_URL = f"postgresql://{POSTGRES_USERNAME}:{POSTGRESQL_PASSWORD}@{POSTGRESQL_URL}/{POSTGRESQL_DBNAME}"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class DataFetcher:


    @classmethod
    def get_answer_if_exists(cls, db, *, prompt):
        answer = db.query(QuestionAnswer).filter_by(question = prompt).first()
        return answer
    
    @classmethod
    def insert_question_answer_pair(cls, db, *, prompt, answer):
        if prompt is None:
            raise ValueError("Prompt cannot be none!")
        qa = QuestionAnswer(question = prompt, answer = answer)
        db.add(qa)
        db.commit()
        return qa