from backend.automation import actions, screen_capture


def get_game_state():
    """Capture and process the game state."""
    screenshot = screen_capture.capture_screen()
    game_state = screen_capture.extract_game_state(screenshot)
    return game_state


def take_action(action_name, x=None, y=None, ability_key=None):
    """Determine and perform actions based on game state."""
    game_state = get_game_state()

    if action_name == "move":
        return actions.move_unit_to_cursor(x, y)
    elif action_name == "interact":
        return actions.interact_with_objects(x, y)
    elif action_name == "end_turn":
        return actions.end_turn()
    elif action_name == "overwatch":
        return actions.activate_overwatch()
    elif action_name == "ability":
        return actions.activate_ability(ability_key)
    elif action_name == "reload":
        return actions.reload_weapon()
    else:
        return {"status": "Unknown action"}
