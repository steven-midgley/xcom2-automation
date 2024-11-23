import pyautogui
import time


class XCOM2Actions:
    def __init__(self):
        pass

    # Movement controls
    def move(self, direction):
        directions = {"up": "w", "down": "s", "left": "a", "right": "d"}
        if direction in directions:
            pyautogui.keyDown(directions[direction])
            pyautogui.keyUp(directions[direction])
            time.sleep(1.5)

    # Camera controls
    def rotate_camera(self, direction):
        rotations = {"left": "q", "right": "e"}
        if direction in rotations:
            pyautogui.keyDown(rotations[direction])
            pyautogui.keyUp(rotations[direction])
            time.sleep(0.75)

    def zoom_camera(self, action):
        zooms = {"in": "+", "out": "-"}
        if action in zooms:
            pyautogui.press(zooms[action])

    # Tactical actions
    def tactical_action(self, action):
        actions = {
            "overwatch": "y",
            "reload": "r",
            "fire_weapon": "f",
            "throw_grenade": "g",
            "hunker_down": "h",
            "ability_1": "1",
            "ability_2": "2",
            "ability_3": "3",
            "ability_4": "4",
            "ability_5": "5",
            "ability_6": "6",
        }
        if action in actions:
            pyautogui.press(actions[action])

    # Interface commands
    def interface_command(self, command):
        commands = {
            "end_turn": "end",
            "escape_menu": "esc",
            "confirm_action": "enter",
            "toggle_inventory": "i",
            "toggle_mission_info": "m",
            "select_next_unit": "tab",
            "select_previous_unit": "shift+tab",
        }
        if command in commands:
            pyautogui.press(commands[command])

    # Squad management commands
    def manage_squad(self, action):
        squad_actions = {
            "cycle_soldiers_forward": "tab",
            "cycle_soldiers_backward": "shift+tab",
            "use_soldier_1": "f1",
            "use_soldier_2": "f2",
            "use_soldier_3": "f3",
            "use_soldier_4": "f4",
            "use_soldier_5": "f5",
            "use_soldier_6": "f6",
        }
        if action in squad_actions:
            pyautogui.press(squad_actions[action])
