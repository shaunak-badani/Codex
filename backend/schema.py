from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base
from pydantic import BaseModel

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique = True)

    def __repr__(self):
        return f"<User id={self.id} name={self.name}>"
    
    class Config:
        orm_mode = True


class QuestionAnswer(Base):
    __tablename__ = "question_answers"
    id = Column(Integer, primary_key=True)
    question = Column(String, nullable=False, unique = True)
    answer = Column(String, nullable=False, unique = True)

    def __repr__(self):
        return f"<QuestionAnswer id={self.id} question={self.question}, answer={self.answer}>"
    
    class Config:
        orm_mode = True


class QuestionAnswerResponse(BaseModel):
    id: int
    question: str
    answer: str

    class Config:
        orm_mode = True
