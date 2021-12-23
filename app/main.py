from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from .dependency import get_sym_spell


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class DataInput(BaseModel):
    string: str

sym_spell = None

@app.on_event("startup")
async def load_data():
    global sym_spell
    sym_spell = await get_sym_spell()

@app.post("/")
def main_app(input: DataInput):
    suggestions = sym_spell.lookup_compound(input.string, max_edit_distance=2)
    return { "result": suggestions[0].term + " " }

@app.get("/get-here")
def get_here():
    return { "status": "up" }