from fastapi import Depends, FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .sym_spell import get_sym_spell
from .config import Config


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


async def verify_token(x_token_req: str = Header(...)):
    if x_token_req != Config.TOKEN_REQUEST:
        raise HTTPException(status_code=400, detail="X-Token-Req header invalid")


sym_spell = None

@app.on_event("startup")
async def load_data():
    global sym_spell
    sym_spell = await get_sym_spell()

@app.get("/get-here")
def get_here():
    return { "status": "up" }
    
@app.get("/", dependencies=[Depends(verify_token)])
def main_app(input: str = None):
    if input:
        suggestions = sym_spell.lookup_compound(input, max_edit_distance=2)
        return { "result": suggestions[0].term + " " }
    return { "error": "input string" }
