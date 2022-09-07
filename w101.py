"""
Automate tedious tasks in Wizard 101.
"""
# pip3 install pyautogui opencv-python pillow

import logging
import math
import random
import time
from enum import Enum

import pyautogui

WIZ_TYPE="ice"
SCREEN_OFFSET=(0, 0)

log = logging.getLogger(__name__)

class CONST:
    """Holds many constants, primarily for graphic elements on screen.
    """
    # 1920x1080 borderless:
    # pyautogui.screenshot('idle.png', region=(1660, 915, 25, 45))
    # pyautogui.screenshot('potion.png', region=(400, 990, 15, 15))

    IDLE = 'common/idle.png'
    POTION = 'common/potion.png'

    # pyautogui.screenshot('inventory_start.png', region=(515, 203, 40, 40))
    # pyautogui.screenshot('inventory_start_2.png', region=(1253, 203, 40, 40))
    # pyautogui.screenshot('hats.png', region=(580, 203, 40, 40))
    # pyautogui.screenshot('robes.png', region=(647, 203, 40, 40))
    # pyautogui.screenshot('boots.png', region=(714, 203, 40, 40))
    # pyautogui.screenshot('wands.png', region=(782, 203, 40, 40))
    # pyautogui.screenshot('athames.png', region=(849, 203, 40, 40))
    # pyautogui.screenshot('amulets.png', region=(916, 203, 40, 40))
    # pyautogui.screenshot('rings.png', region=(983, 203, 40, 40))
    # pyautogui.screenshot('pets.png', region=(1051, 203, 40, 40))
    # pyautogui.screenshot('mounts.png', region=(1118, 203, 40, 40))
    # pyautogui.screenshot('decks.png', region=(1186, 203, 40, 40))
    # pyautogui.screenshot('elixir.png', region=(1253, 203, 40, 40))
    # pyautogui.screenshot('equipped.png', region=(964, 415, 28, 28))
    # pyautogui.screenshot('trash.png', region=(1260, 878, 50, 50))
    # pyautogui.screenshot('trash_confirm.png', region=(945, 645, 50, 30))
    # pyautogui.screenshot('finish_pet_improvement.png', region=(575, 890, 150, 35))
    INV_OPEN_CLOSE = 'b'
    INV_START = 'common/inventory_start.png'
    INV_START_2 = 'common/inventory_start_2.png'
    INV_HATS = 'common/hats.png'
    INV_ROBES = 'common/robes.png'
    INV_BOOTS = 'common/boots.png'
    INV_WANDS = 'common/wands.png'
    INV_ATHAMES = 'common/athames.png'
    INV_AMULETS = 'common/amulets.png'
    INV_RINGS = 'common/rings.png'
    INV_PETS = 'common/pets.png'
    INV_MOUNTS = 'common/mounts.png'
    INV_DECKS = 'common/decks.png'
    INV_ELIXIR = 'common/elixir.png'
    INV_EQUIPPED = 'common/equipped.png'
    INV_TRASH = 'common/trash.png'
    INV_TRASH_CONFIRM = 'common/trash_confirm.png'
    INV_FEED_PET = 'common/feed_pet.png'
    INV_FEED_PET_CONFIRM = 'common/feed_pet_confirm.png'
    INV_FINISH_PET_IMPROVEMENT = 'common/finish_pet_improvement.png'

    # possible spell locations:
    # pyautogui.screenshot('a.png', region=(700, 480, 50, 50))
    # pyautogui.screenshot('b.png', region=(790, 480, 50, 50))
    # pyautogui.screenshot('c.png', region=(850, 480, 50, 50))
    # pyautogui.screenshot('d.png', region=(910, 480, 50, 50))
    # pyautogui.screenshot('e.png', region=(935, 480, 50, 50))
    #
    # pips location:
    # pyautogui.screenshot('power_pips_none.png', region=(1527, 1050, 33, 10))
    # pyautogui.screenshot('a_test.png', region=(820, 500, 40, 30))

    # pyautogui.screenshot('fight_pass.png', region=(650, 645, 100, 35))

    FIGHT_PASS = 'common/fight_pass.png'
    FIGHT_POWER_PIPS_0 = 'common/power_pips_none.png'
    FIGHT_POWER_PIPS_1 = 'common/power_pips_one.png'
    FIGHT_POWER_PIPS_2 = 'common/power_pips_two.png'
    FIGHT_SPELL_BUFFER = 'common/spell_buffer.png'
    FIGHT_SPELL_BLADE_BUFFER_1 = 'common/blade_buffer_1.png'
    FIGHT_SPELL_BLADE_BUFFER_2 = 'common/blade_buffer_2.png'
    FIGHT_SPELL_4_PIPS = WIZ_TYPE + '/' + 'p4_spell.png'
    FIGHT_SPELL_4_PIPS_BUFFED = WIZ_TYPE + '/' + 'p4_spell_buffed.png'
    FIGHT_SPELL_BLADE = WIZ_TYPE + '/' + 'blade.png'
    FIGHT_SPELL_BLADE_BUFFED = WIZ_TYPE + '/' + 'blade_buffed.png'
    FIGHT_SPELL_SPIRIT_BLADE = 'common/spirit_blade.png'
    FIGHT_SPELL_SPIRIT_BLADE_BUFFED = 'common/spirit_blade_buffed.png'

class Position(Enum):
    """Describes the different positions on the battle board.

    SUN, EYE, STAR, and MOON represent player positions.
    DAGGER, KEY, RUBY, and SPIRAL represent opponent positions.
    """
    SUN = ((1550, 650), (0, 0))
    EYE = ((1200, 950), (0, 0))
    STAR = ((850, 950), (0, 0))
    MOON = ((500, 950), (0, 0))
    DAGGER = ((500, 950), (0, 0))
    KEY = ((500, 950), (0, 0))
    RUBY = ((500, 950), (0, 0))
    SPIRAL = ((500, 950), (0, 0))

    def __init__(self, click_pos, pip_pos):
        """Initializes the location of various elements of a position.

        Args:
            click_pos (x(int), y(int)): Where to click on the screen to select the entity
                in this location.
            pip_pos (x(int), y(int)): The top-left corner of the position where the entity's
                pips are located.
        """
        self.click_position = (click_pos[0] + SCREEN_OFFSET[0], click_pos[1] + SCREEN_OFFSET[1])
        self.pip_position = (pip_pos[0] + SCREEN_OFFSET[0], pip_pos[1] + SCREEN_OFFSET[1])

    @property
    def click_x(self):
        """The X screen location on which to click to select this position in the battle."""
        return self.click_position[0]

    @property
    def click_y(self):
        """The Y screen location on which to click to select this position in the battle."""
        return self.click_position[1]

    @property
    def click(self):
        """The screen location on which to click to select this position in the battle."""
        return self.click_position

    @property
    def pip_left(self):
        """The X screen location from which to start looking for pips for this position."""
        return self.pip_position[0]

    @property
    def pip_top(self):
        """The Y screen location from which to start looking for pips for this position."""
        return self.pip_position[1]

    @property
    def pips(self):
        """The screen location from which to start looking for pips for this position."""
        return self.pip_position

    def __str__(self):
        return self.name

def find_image(image):
    """Try to find the given image on the current screen.

    This wrapper to make it easy to consistently change the parameters to the locateOnScreen call.

    Args:
        image (string): The filename of the image to try to locate on the current screen.

    Return:
        (left, top, width, height) (tuple): a 4-integer tuple

    Raises:
        pyautogui.ImageNotFoundException: Image was not found on the screen.
    """
    return pyautogui.locateOnScreen(image, confidence=0.90)

def move_mouse_to(location, duration=0.25):
    """Move the mouse to the given cursor location over the given time period

    Args:
        location ((int), (int)): Tuple holding the X, Y position on the screen to
            which the mouse should be moved.
        duration (float): How long (in seconds) it should take to move the mouse from
            it's current location to the new location.
    """
    if duration is None:
        duration = .1 + random.random()/4
    pyautogui.moveTo(location[0], location[1], duration=duration, tween=pyautogui.easeOutQuad)

def find_one_of_images(images, retries=20, delay=0.1):
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
                location = find_image(image)
                if location is not None:
                    found = image
                    break
            except pyautogui.ImageNotFoundException:
                pass
        retries -= 1
        time.sleep(delay)
    log.info("Found %s.", found)
    return found

def safe_click_image(image):
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
        location = find_image(image)
    x_loc, y_loc = pyautogui.center(location)
    move_mouse_to((x_loc, y_loc))
    pyautogui.click()

def safe_cast_spell(spell):
    """Casts a spell during battle.

    Casts the spell and moves the cursor up out of the way to get rid of the
    magnification effect that happens during battle.

    Args:
        spell (string): The filename of the spell to be clicked upon on the current screen.

    Raises:
        pyautogui.ImageNotFoundException: The spell was not found on the screen.
    """
    safe_click_image(spell)
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
        time.sleep(milliseconds/1000)

def wait_for_image(image):
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
            image_bounds = find_image(image)
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

def click_position(position):
    """Click on the given battle position

    Click on a battle position.  Can be a teammate for a beneficial spell such as healing or blades.
    Can be an opponent to target them with a trap or an attack spell.

    Args:
        position (Position): which battle position to click to select
    """
    log.info("Clicking on %s", position)
    pyautogui.moveTo(position.click_x, position.click_y,
                     duration=calc_delay((position.click_x, position.click_y)),
                     tween=pyautogui.easeOutQuad)
    pyautogui.click()

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
    return position == Position.DAGGER or position == Position.KEY

def try_buff(spells):
    """Try to use the buffer spell to buff the spell

    Args:
        spells (buffer(string), target_spell(string)): A tuple of the spell to use to buff
            the spell and the spell to buff.

    Returns:
        True: The target_spell was able to be buffed.
        False: Either the buffer or the target_spell was not found.
    """
    log.info("Using %s to try to buff a spell.", spells)
    result = False
    if len(spells) == 2:
        spell = find_image(spells[1])
        if spell is not None:
            buffer = find_image(spells[0])
            if buffer is not None:
                cast_spells(spells)
                pyautogui.move(0, -100, duration=.1, tween=pyautogui.easeOutQuad)
                # Wait for the buff ripple effect to complete.
                time.sleep(0.4)
                result = True
    else:
        log.error("try_buff: invalid input: the length of the input was %d (%s), expected 2.",
                 len(spells), spells)
        return False
    log.info("able to buff using %s?  %s", spells, result)
    return result

def try_buff_blade(target_blade):
    """Try to buff the given target_blade

    Attempts to use the any of the many blade buffs to buff the target_blade.

    Args:
        target_blade (string): The filename of the blade to buff.

    Returns:
        True: The target_blade was able to be buffed.
        False: Either a buffer or the target_blade was not found.
    """
    result = False
    log.info("Trying to buff %s", target_blade)
    blade = find_image(target_blade)
    if blade is not None:
        buffer = find_image(CONST.FIGHT_SPELL_BLADE_BUFFER_1)
        if buffer is None:
            buffer = find_image(CONST.FIGHT_SPELL_BLADE_BUFFER_2)
        log.info("buffer = %s; blade = %s", buffer, blade)
        if buffer is not None:
            move_mouse_to(pyautogui.center(buffer))
            pyautogui.click()
            move_mouse_to(pyautogui.center(blade))
            pyautogui.click()
            pyautogui.move(0, -100, duration=.1, tween=pyautogui.easeOutQuad)
                # Wait for the buff ripple effect to complete.
            time.sleep(.4)
            result = True
    log.info("Was blade buffed?  %s", result)
    return result

def try_to_blade(position = Position.SUN):
    """Try to cast a blade on wizard at the given position.

    Attempts to buff a blade if possible, and then cast the buffed blade or
    an unbuffed blade if it was not possible to buff one.

    Args:
        position (Position): Which battle position to target with the blade.

    Returns:
        True: It was possible to blade the target position.
        False: It was not possible to cast a blade.
    """
    log.info("Trying to cast a blade.")
    bladed = False
    try_buff_blade(CONST.FIGHT_SPELL_BLADE)
    buffed = find_image(CONST.FIGHT_SPELL_BLADE_BUFFED)
    if  buffed is not None:
        cast_spells([CONST.FIGHT_SPELL_BLADE_BUFFED])
        bladed = True
    else:
        naked = find_image(CONST.FIGHT_SPELL_BLADE)
        if naked is not None:
            cast_spells([CONST.FIGHT_SPELL_BLADE])
            bladed = True
    if bladed:
        click_position(position)
    log.info("able to blade?  %s", bladed)
    return bladed

def cast_spells(spells, target=None):
    """Cast the list of spells on the target, or None if the final spell has no target

    Casts a series of spells on the given target.  When the list contains more than one
    element, it is typically a buffer, the spell to buff, and then the target of the
    buffed spell (or None for an AoE spell.)

    Args:
        spells (list(string)): The spells to cast.
        target (Position, optional): Which possition on the battle field to target with
             the spell. Defaults to None.

    Raises:
        pyautogui.ImageNotFoundException: One of the spells could not be found.
    """
    log.info("Casting %s this turn.", spells)
    for spell in spells:
        safe_cast_spell(spell)
    if target is not None:
        click_position(target)
    else:
        time.sleep(0.1)
        pyautogui.move(0, -100, duration=.1, tween=pyautogui.easeOutQuad)

def inventory_calibrate():
    """Make sure the inventory screen is in a known state.

    inventory_calibrate makes sure that the inventory display is in a known state.  When
    clicking 'b', the backpack opens to the last tab the user was looking at.  Because
    the highlighting of the tab may cause problems with the image search recognition,
    ensure that the current tab displayed is the elixir tab.

    Returns:
        True: The inventory is now on the elixir tab of the backpack.
        False: The inventory could not be calibrated, it is unclear which tab is currently
            displayed.
    """
    log.info("Calibrating inventory.")
    try:
        safe_click_image(CONST.INV_START)
        return True
    except pyautogui.ImageNotFoundException:
        pass
    try:
        safe_click_image(CONST.INV_START_2)
        return True
    except pyautogui.ImageNotFoundException:
        return False

def trash_all_items(category):
    """Throws the non-equipped items in this category in the trash.

    Typically used for pets and mounts, which can not be fed to pets.  For normal equipement,
    using feed_pet_all_items gets some benefit for the item destruction.

    Args:
        category (string): The filename of the backpack tab for which non-equiped items
            will be thrown in the trash.
    """
    log.info("Trashing all %s.", category)
    safe_click_image(category)
    x_loc, y_loc = pyautogui.center(find_image(CONST.INV_EQUIPPED))
    pyautogui.moveTo(x_loc+100, y_loc+50)
    time.sleep(0.1)
    pyautogui.click()

    while find_image(CONST.INV_TRASH):
        try:
            safe_click_image(CONST.INV_TRASH)
        except pyautogui.ImageNotFoundException:
            break
        safe_click_image(CONST.INV_TRASH_CONFIRM)

def feed_pet_all_items(category):
    """Feeds non-equipped items in this category to the current pet.

    Args:
        category (string): The filename of the backpack tab for which non-equiped items
            will be fed to the current pet.
    """
    log.info("Feeding pet all %s.", category)
    safe_click_image(category)
    x_loc, y_loc = pyautogui.center(find_image(CONST.INV_EQUIPPED))
    pyautogui.moveTo(x_loc+100, y_loc+50)
    time.sleep(0.1)
    pyautogui.click()

    while find_image(CONST.INV_FEED_PET):
        try:
            safe_click_image(CONST.INV_FEED_PET)
        except pyautogui.ImageNotFoundException:
            break
        safe_click_image(CONST.INV_FEED_PET_CONFIRM)
        time.sleep(0.25)
        found = find_one_of_images([CONST.INV_FINISH_PET_IMPROVEMENT,
                                    CONST.INV_FEED_PET_CONFIRM,
                                    CONST.INV_PETS])
        if found == CONST.INV_FINISH_PET_IMPROVEMENT:
            safe_click_image(CONST.INV_FINISH_PET_IMPROVEMENT)
            time.sleep(0.1)

def clear_inventory():
    """Get rid of items to avoid filling the backpack.
    """
    # clear inventory of junk
    pyautogui.press(CONST.INV_OPEN_CLOSE)
    if inventory_calibrate():
        feed_pet_all_items(CONST.INV_HATS)
        feed_pet_all_items(CONST.INV_ROBES)
        feed_pet_all_items(CONST.INV_BOOTS)
        feed_pet_all_items(CONST.INV_ATHAMES)
        feed_pet_all_items(CONST.INV_RINGS)
        trash_all_items(CONST.INV_PETS)
        trash_all_items(CONST.INV_MOUNTS)
    pyautogui.press(CONST.INV_OPEN_CLOSE)

def pass_turn(position = Position.SUN):
    """Cannot attack, so pass this turn in battle.

    If the current deck has blades, if the current hand has a blade, cast that instead
    of passing.  If the current hand has a buffer, the blade will be buffed before cast.
    If the current hand does not have any blades in it, the pass button is clicked.

    Args:
        position (Position, optional): The position that should benefit from passing this
            turn. Defaults to Position.SUN.
    """
    if not try_to_blade(position):
        log.info("Passing since could not blade.")
        safe_click_image(CONST.FIGHT_PASS)
        pyautogui.move(0, -100, duration=.1, tween=pyautogui.easeOutQuad)
        time.sleep(1)
    wait_for_image(CONST.FIGHT_PASS)

def fight_4pip_aoe_battle():
    """A 4 pip AoE battle suitable for simple battles.

    Before farming locations using this script, it's assumed that basic buffing of the AoE
    attack card is available, at least the Strong sun school spell is available.  Before this
    time, automated farming is not recommended.  Having a sky iron hasta to ensure a starting
    power pip is highly recommended.

    Balancing the deck for this use is delicate.  There are often situations where opponents
    may survive the first attack.  There needs to be enough cards in the deck for two to
    three attacks, but if there are two many cards in the deck, it's hard to be sure to have
    the one you actually need.  The recommended deck configuration is:
    - two/three attack buffer cards (strong / giant / ...)
    - one blade buffer card (either sharpened blade, level 86 sun school or enchanted armament pet)
    - two blades
    - two/three 4 pip AoE cards
    The pattern will be to cast the attack spell every time the caster has four pips.  At
    the beginning, if there are less than four pips or if key has not yet joined the battle,
    then the script will blade if possible or pass the turn if blades are not available.
    After that, whenever there are four pips, the script will attempt to cast the AoE, and
    the rest of the time either pass or blade.
    """
    log.info("Fighting the battle")
    wait_for_image(CONST.FIGHT_PASS)
    pips = find_one_of_images([CONST.FIGHT_POWER_PIPS_2,
                               CONST.FIGHT_POWER_PIPS_1,
                               CONST.FIGHT_POWER_PIPS_0])
    if not opponent_in_battle(Position.KEY) or \
        pips == CONST.FIGHT_POWER_PIPS_0 or \
        pips == CONST.FIGHT_POWER_PIPS_1:
        pass_turn()
    activity = CONST.FIGHT_PASS
    while activity == CONST.FIGHT_PASS:
        cast_spells([CONST.FIGHT_SPELL_BUFFER,
                     CONST.FIGHT_SPELL_4_PIPS,
                     CONST.FIGHT_SPELL_4_PIPS_BUFFED])
        activity = find_one_of_images([CONST.FIGHT_PASS, CONST.IDLE], 120, .5)
        if activity == CONST.FIGHT_PASS:
            pass_turn()
            # Could have two single pips, one power pip and a single, or two power pips.
            pips = find_one_of_images([CONST.FIGHT_POWER_PIPS_2,
                                       CONST.FIGHT_POWER_PIPS_1,
                                       CONST.FIGHT_POWER_PIPS_0], 1, .1)
            if pips is None or pips == CONST.FIGHT_POWER_PIPS_0 or pips == CONST.FIGHT_POWER_PIPS_1:
                pass_turn()
            # currently not handling the case where we get 3 single pips.  That's stupid
    log.info("Battle complete")

def help_fight_4pip_aoe_battle(position):
    """Helps buff a hitter (at position) using blades.

    To help someone fight a 4pip AoE battle, the expected helping deck can / should be made up
    of blades to buff the player in the given position.  The deck may contain:
    - up to two cards to buff blades (one for the regular blade and one optional for spirit /
      elemental blades)
    - up to two spirit / elemental blades
    - up to two blades that will benefit the other player
    The script attempts to use this order to case spells, any missing spells are skipped:
    - cast the buffed spirit / elemental blade
    - cast the buffed primary blade
    - cast the regular spirit blade
    - cast the regular primary blade
    """
    log.info("Help fighting the battle")
    wait_for_image(CONST.FIGHT_PASS)
    try_buff_blade(CONST.FIGHT_SPELL_SPIRIT_BLADE)
    try_buff_blade(CONST.FIGHT_SPELL_BLADE)
    activity = CONST.FIGHT_PASS
    while activity == CONST.FIGHT_PASS:
        if find_image(CONST.FIGHT_SPELL_SPIRIT_BLADE_BUFFED):
            cast_spells([CONST.FIGHT_SPELL_SPIRIT_BLADE_BUFFED], position)
        elif find_image(CONST.FIGHT_SPELL_BLADE_BUFFED):
            cast_spells([CONST.FIGHT_SPELL_BLADE_BUFFED], position)
        elif find_image(CONST.FIGHT_SPELL_SPIRIT_BLADE):
            cast_spells([CONST.FIGHT_SPELL_SPIRIT_BLADE], position)
        elif find_image(CONST.FIGHT_SPELL_BLADE):
            cast_spells([CONST.FIGHT_SPELL_BLADE], position)
        else:
            pass_turn()
        activity = find_one_of_images([CONST.FIGHT_PASS, CONST.IDLE], 120, .5)
    log.info("Battle complete")

def couchpotato_helper():
    """Logic to help someone farm couch potatoes.

    This scenario waits for a battle to start.  It expects to be in Grizzleheim at
    Savarstaad Pass and battling the Splithoofs.
    """
    while True:
        for _ in range(100):
            help_fight_4pip_aoe_battle(Position.EYE)
            hold('a', 250)
            hold('w', 1000)
        hold('s', 1000)
        hold('d', 250)
        hold('s', 2500)
        clear_inventory()
        hold('w', 2500)
        hold('a', 250)
        hold('w', 1000)

def couchpotatoes():
    """Logic to farm couch potatoes.

    This scenario waits for a battle to start.  It expects to be in Grizzleheim at
    Savarstaad Pass and battling the Splithoofs.
    """
    while True:
        for until_out_of_mana in range(2):
            # 40 battles
            for until_backpack_full in range(40):
                log.info("until_out_of_mana = %d, until_backpack_full = %d",
                         until_out_of_mana, until_backpack_full)
                fight_4pip_aoe_battle()
                hold('a', 250)
                hold('w', 1000)
            hold('s', 1000)
            hold('d', 250)
            hold('s', 2500)
            clear_inventory()
            hold('w', 2500)
            hold('a', 250)
            hold('w', 1000)

        # pop a potion to continue farming -- 320 mana used
        try:
            safe_click_image(CONST.POTION)
        except pyautogui.ImageNotFoundException as no_potions:
            print("No more potions. Guess we're done farming!")
            raise SystemExit from no_potions

def kraken():
    """Logic to farm the Kraken.

    This scenario waits for a battle to start.  It expects to be in triton lane at
    Kraken Isle and battling the Kraken.
    """
    while True:
        for until_out_of_mana in range(6):
            # 40 battles
            for until_backpack_full in range(20):
                log.info("until_out_of_mana = %d, until_backpack_full = %d",
                         until_out_of_mana, until_backpack_full)
                fight_4pip_aoe_battle()
                hold('d', 250)
                hold('w', 1000)
            hold('s', 1000)
            hold('d', 250)
            hold('s', 2500)
            clear_inventory()
            hold('w', 2500)
            hold('a', 250)
            hold('w', 1000)

        # pop a potion to continue farming -- 320 mana used
        try:
            safe_click_image(CONST.POTION)
        except pyautogui.ImageNotFoundException as no_potions:
            print("No more potions. Guess we're done farming!")
            raise SystemExit from no_potions

def rattlebones():
    """Logic to farm Rattlebones Exalted Duels.

    This scenario waits for a battle to start.  It expects to be in Grizzleheim at
    Savarstaad Pass and battling the Splithoofs.
    """
    while True:
        for battles_before_popping_a_potion in range(3):
            # 40 battles
            for battles_before_clearing_inventory in range(40):
                log.info(("battles_before_popping_a_potion = %d, "
                        "battles_before_clearing_inventory = %d"),
                         battles_before_popping_a_potion, battles_before_clearing_inventory)
                fight_4pip_aoe_battle()
                hold('a', 680)
                hold('w', 3000)
                wait_for_image(CONST.IDLE)
                hold('s', 1000)
                wait_for_image(CONST.IDLE)
                hold('w', 2500)
            clear_inventory()

        # pop a potion to continue farming -- 320 mana used
        try:
            safe_click_image(CONST.POTION)
        except pyautogui.ImageNotFoundException as no_potions:
            print("No more potions. Guess we're done farming!")
            raise SystemExit from no_potions

def instructions():
    """Provide basic instructions to the user
    """
    msg = """
1. Set your Wizard101 to be 1920x1080, borderless windowed mode.
2. In combat, take a screenshot of a small part of your card's picture and
   save it in the right folder if the asset doesn't already exist.
3. Clear your inventory as much as possible. Remove ALL hats, robes, boots,
   and mounts you care about (other than what you have equipped) from your
   inventory. Items in these categories get deleted.
"""
    print(msg)
    pyautogui.moveTo(SCREEN_OFFSET[0] + 1920/2, SCREEN_OFFSET[1] + 1080/2)
    msg = """
4. Your mouse has been moved to the monitor where Wizard101 should be placed.
   Please move the window to that monitor.

Press ENTER to start the bot. After hitting ENTER, begin the battle you wish to farm.
"""
    print(msg)
    input()

    #print("Starting in 5 seconds...")
    #time.sleep(5)
    pyautogui.moveTo(SCREEN_OFFSET[0] + 250, SCREEN_OFFSET[1] + 250)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format=(
        "%(asctime)s "
        "%(levelname)s "
        "%(module)s:%(funcName)s:%(lineno)d "
        "%(message)s"))
    instructions()
    kraken()
