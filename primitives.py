"""
Primitive functions to interact with the UI
"""

import logging
import math
import time

import pyautogui
from battle_position import BattlePosition

log = logging.getLogger(__name__)

def find_image(image, confidence=0.95):
    """Try to find the given image on the current screen.

    This wrapper to make it easy to consistently change the parameters to the locateOnScreen call.

    Args:
        image (string): The filename of the image to try to locate on the current screen.

    Return:
        (left, top, width, height) (tuple): a 4-integer tuple

    Raises:
        pyautogui.ImageNotFoundException: Image was not found on the screen.
    """
    return pyautogui.locateOnScreen(image, confidence=confidence)

def move_mouse_to(location):
    """Move the mouse to the given cursor location

    Args:
        location ((int), (int)): Tuple holding the X, Y position on the screen to
            which the mouse should be moved.
    """
    pyautogui.moveTo(location[0], location[1], duration=calc_delay(location),
                     tween=pyautogui.easeOutQuad)

def move_mouse(offset):
    """Move the mouse"""
    current = pyautogui.position()
    destination = (current[0] + offset[0], current[1] + offset[1])
    move_mouse_to(destination)

def find_one_of_images(images, retries=20, delay=0.1, confidence=0.95):
    """Try to find any one of the given images on the current screen.

    Args:
        images (list[string]): A list of image filenames to try to find on the screen.
        retries (int): How many times to try to find any of the images on the screen.
        delay (float): The delay in seconds between each complete scan for images in the list.

    Returns:
        String: The name of the file that was found on the screen or None if none of the
                images were found.
    """
    found = None

    log.info("Looking for one of %s to show up on the screen.", images)
    while retries > 0 and found is None:
        for image in images:
            try:
                location = find_image(image, confidence)
                if location is not None:
                    found = image
                    break
            except pyautogui.ImageNotFoundException:
                pass
        retries -= 1
        time.sleep(delay)
    log.info("Found %s.", found)
    return found

def count_pips(position):
    """Look at the pips at the given position and determine total pips."""
    log.info("Counting pips for %s", position)
    pips_area = pyautogui.screenshot(region=position.pips_position)
    normal_pips = 0
    power_pips = 0
    for pip_number in range(0, 7, 1):
        loc = (10 + math.ceil(22.5 * pip_number), 13)
        pixel = pips_area.getpixel(loc)
        log.debug("pip %d = %s", pip_number, pixel)
        red = pixel[0]
        green = pixel[1]
        blue = pixel[2]
        if red > 210 and green > 210:
            if blue > 185:
                normal_pips += 1
            elif blue > 40 and blue < 70:
                power_pips += 1
            else:
                break
        else:
            break
    log.debug("power_pips=%d", power_pips)
    log.debug("normal_pips=%d", normal_pips)
    result = power_pips * 2 + normal_pips
    log.info("%s has %d pips", position, result)
    return result

def click():
    """Click the mouse"""
    pyautogui.click()

def center_of(x_y_width_height):
    """Find the center of a given bouding box."""
    return pyautogui.center(x_y_width_height)

def safe_click_image(image, confidence=0.95):
    """Safely clicks on the given image on the screen.

    Args:
        image (string): The filename of the image to be clicked upon on the current screen.

    Raises:
        pyautogui.ImageNotFoundException: Image was not found on the screen.
    """
    log.info("Safely clicking %s.", image)
    location = None
    while location is None:
        time.sleep(0.1)
        location = find_image(image, confidence)
    x_loc, y_loc = pyautogui.center(location)
    move_mouse_to((x_loc, y_loc))
    pyautogui.click()

def safe_cast_spell(spell, confidence=0.85):
    """Casts a spell during battle.

    Casts the spell and moves the cursor up out of the way to get rid of the
    magnification effect that happens during battle.

    Args:
        spell (string): The filename of the spell to be clicked upon on the current screen.

    Raises:
        pyautogui.ImageNotFoundException: The spell was not found on the screen.
    """
    safe_click_image(spell, confidence)
    pyautogui.move(0, -200, duration=.1, tween=pyautogui.easeOutQuad)


def hold(button, milliseconds):
    """Press and hold a button for a given amount of time.

    hold is typically used for pressing various movement keys for some amount of time.

    Args:
        button (string): The character to hold ('w', 'a', 's', 'd' as examples)
        milliseconds (int): How long to hold the button down.
    """
    log.info("Pressing %s for %dms", button, milliseconds)
    with pyautogui.hold(button):
        time.sleep(milliseconds/1000.0)

def press(button):
    """Press a key"""
    log.info("Pressing %s", button)
    pyautogui.press(button)

def wait_for_image(image, confidence=0.95):
    """Loops waiting for the given image to show up on the current scrren.

    This function is used to wait while something else happens until the given image appears.
    It should be known that the image will eventually appear on the screen.  For example, when
    a battle is expected to start, calling wait_for_image(CONST.FIGHT_PASS) will wait for all
    of the animation of players and opponents moving to their battle positions and will return
    when the "PASS" button is displayed during the battle screen.

    Args:
        image (string): The filename of the image to wait for.
    """
    log.info("Waiting for %s to show up on the screen.", image)
    image_bounds = None
    while image_bounds is None:
        try:
            image_bounds = find_image(image, confidence)
        except pyautogui.ImageNotFoundException:
            image_bounds = None
        if image_bounds is None:
            time.sleep(0.1)
    log.info("%s found", image)

def calc_delay(destination):
    """Calculate how much delay to use to move from one point on the screen to another point.

    Calculates the distance between the current point and the destination point and how long
    it should take to move between points

    Args:
        destination (x(int), y(int)): The location where the cursor will end up on the screen.

    Returns:
        seconds (float): The number of seconds to use to move from point to point.
    """
    current = pyautogui.position()
    distance = math.sqrt((current[0] - destination[0]) ** 2 + (current[1] - destination[1]) ** 2)
    # corner to corner distance is 2,203
    return distance/2500

def opponent_in_battle(position):
    """Indicates if an opponent is actively in the battle at the given location.

    opponent_in_battle is typically used before launching the main battle logic.  For example,
    while farming couch potatoes, it's not uncommon for the dagger splithoof to come into the
    battle late so a round-one AoE will fail to kill dagger, requiring an extra 2-3 rounds to
    regain pips to cast another AoE spell.  Instead, the scenario checks to see if the dagger
    position is occupied and passes a turn if not, giving time for the position to become occupied.

    Note that this function can be used in the battle to find which positions can be targeted.

    Returns:
        True: The opponent is in the given position
        False: The opponent is not active in the given position.

    TODO: Implementation based upon pips at location > 0.
    """
    return position == BattlePosition.DAGGER or position == BattlePosition.KEY

def battle_position_of(player):
    """Looks through the battle possitions to find the given player name.
    
    The player name should be a screen capture.
    
    Returns:
        BattlePosition: The BattlePosition of the given player
        None: The player was not found in any battle position
    """
    result = None
    log.info("Looking for %s in battle.", player)
    for pos in BattlePosition:
        name_area = pos.name_position
        log.info("%s.name_area = %s", pos, name_area)
        pos_name = pyautogui.screenshot(region=name_area)
        pos_name.save("pos" + str(pos) + ".png")
        try:
            if pyautogui.locate(player, pos_name, confidence=.95) is not None:
                result = pos
                break
        except pyautogui.ImageNotFoundException:
            pass
    return result

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format=(
        "%(asctime)s "
        "%(levelname)s "
        "%(module)s:%(funcName)s:%(lineno)d "
        "%(message)s"))
    print(battle_position_of("wolf.png"))
