# backend/api/game_state.py
# Example of how you could structure the game state, like monitoring health, positions, etc.


class GameState:
    def __init__(self, health, position):
        self.health = health
        self.position = position

    def update_state(self, new_health, new_position):
        self.health = new_health
        self.position = new_position

    def get_state(self):
        return {"health": self.health, "position": self.position}
