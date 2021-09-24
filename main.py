from dependency import get_sym_spell

from typing import Optional
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://103.226.138.132:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class DataInput(BaseModel):
    value: str

sym_spell = None

@app.on_event("startup")
async def load_data():
    global sym_spell
    sym_spell = await get_sym_spell()

@app.get("/")
def read_root():
    return {"message": "Looks like you're lost. Use POST instead."}

@app.post("/")
async def main_app(input: DataInput):
    suggestions = sym_spell.lookup_compound(input.value, max_edit_distance=2)
    return { "result": suggestions[0].term + " "}