# backend/server.py
from fastapi import FastAPI
from pydantic import BaseModel
from backend.api.action import perform_click, perform_move
from backend.api.game_state import GameState

app = FastAPI()


class ActionRequest(BaseModel):
    action: str
    x: int
    y: int


# Dummy game state for example purposes
game_state = GameState(health=100, position=(0, 0))


@app.get("/")
def read_root():
    return {"message": "XCOM 2 Automation Backend"}


@app.get("/game_state")
def get_game_state():
    return game_state.get_state()


@app.post("/perform_action/")
def perform_action(request: ActionRequest):
    if request.action == "click":
        return perform_click(request.x, request.y)
    elif request.action == "move":
        return perform_move(request.x, request.y)
    return {"status": "Invalid action"}
