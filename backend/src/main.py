from fastapi import FastAPI, Depends, status, HTTPException
from fastapi.requests import Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

# DB functions
from models import get_db, DataFetcher
from models import create_db
from schema import QuestionAnswerResponse
from sqlalchemy.orm import Session

from llama_cpp import Llama
import os

model_path = os.path.join(os.path.dirname(__file__), "../models", "qwen2.5-coder-7b.gguf")
model_path = os.path.abspath(model_path)


llm = Llama(
    model_path=model_path,
    n_ctx=8192,
    n_gpu_layers=35,
    n_threads=8
)

app = FastAPI(root_path='/api')

# list of allowed origins
origins = [
    "http://localhost:5173",
    "http://vcm-45508.vm.duke.edu"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return JSONResponse(
        content = {"message": "Hello world!"}
    )

@app.on_event("startup")
def on_startup():
    create_db()

@app.get("/prompt", response_model = QuestionAnswerResponse)
def query_model_with_prompt(query: str, db: Session = Depends(get_db)):
    """
    Query endpoint for prompting Qwen 2.5 7B
    """
    modified_query = f"Q: {query} Keep it concise. A:"
    existing_qa = DataFetcher.get_answer_if_exists(db, prompt = modified_query)
    if existing_qa is not None:
        return existing_qa
    output = llm(modified_query, max_tokens = None)
    output_text = output['choices'][0]['text']

    new_qa = DataFetcher.insert_question_answer_pair(db, prompt = modified_query, answer = output_text)
    return new_qa
    # return JSONResponse(
    #     content = { "message": output_text }
    # )
