import pyautogui


def move_unit_to_cursor(x, y):
    """Simulate moving the unit to the cursor's position."""
    pyautogui.click(x, y)  # Simulate a click at the given coordinates
    return {"status": "Unit moved to position", "coordinates": {"x": x, "y": y}}


def interact_with_objects(x, y):
    """Simulate interacting with an object."""
    pyautogui.click(x, y)  # Simulate click to interact
    return {"status": "Interacted with object", "coordinates": {"x": x, "y": y}}


def end_turn():
    """Simulate the end turn action."""
    pyautogui.press("enter")  # Simulate pressing Enter to end the turn
    return {"status": "Turn ended"}


def activate_overwatch():
    """Simulate activating overwatch."""
    pyautogui.press("y")  # Simulate pressing Y for overwatch
    return {"status": "Overwatch activated"}


def activate_ability(ability_key):
    """Simulate activating an ability."""
    pyautogui.press(
        str(ability_key)
    )  # Simulate pressing the number key for the ability
    return {"status": f"Ability {ability_key} activated"}


def reload_weapon():
    """Simulate reloading the weapon."""
    pyautogui.press("r")  # Simulate pressing R to reload
    return {"status": "Weapon reloaded"}
