# pip3 install pyautogui
# pip3 install opencv-python
# pip3 install pillow

import pyautogui
import time
import random
import logging

wiz_type="ice"

log = logging.getLogger(__name__)

class CONST:
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
    # pyautogui.screenshot('', region=(730, 480, 100, 100))
    # pyautogui.screenshot('', region=(935, 480, 50, 50))
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
    FIGHT_SPELL_BLADE_BUFFER = 'common/blade_buffer.png'
    FIGHT_SPELL_4_PIPS = wiz_type + '/' + 'p4_spell.png'
    FIGHT_SPELL_4_PIPS_BUFFED = wiz_type + '/' + 'p4_spell_buffed.png'
    FIGHT_SPELL_BLADE = wiz_type + '/' + 'blade.png'
    FIGHT_SPELL_BLADE_BUFFED = wiz_type + '/' + 'blade_buffed.png'

def findImage(image):
    return pyautogui.locateOnScreen(image, confidence=0.90)

def moveMouseTo(x, y, duration=0.25):
    if duration == None:
        duration = .1 + random.random()/4
    pyautogui.moveTo(x, y, duration=duration, tween=pyautogui.easeOutQuad)

def findOneOfImage(images, retries=20, delay=0.1):
    found = None
    
    log.info("Looking for one of %s to show up on the screen.", images)
    while retries > 0 and found == None:
        for image in images:
            try:
                location = findImage(image)
                if location != None:
                    found = image
                    break
            except:
                pass
        retries -= 1
        time.sleep(delay)
    log.info("Found %s.", found)
    return found

def safe_click_image(image):
    log.info("Safely clicking %s.", image)
    location = None
    while location == None:
        time.sleep(0.1)
        location = findImage(image)
    x,y = pyautogui.center(location)
    moveMouseTo(x, y)
    pyautogui.click()
    time.sleep(0.1)
    pyautogui.move(0, -100, duration=.1, tween=pyautogui.easeOutQuad)
    
def hold(button, ms):
    log.info("Pressing %s for %dms", button, ms)
    with pyautogui.hold(button):
        time.sleep(ms/1000)

def wait_for_image(image):
    log.info("Waiting for %s to show up on the screen.", image)
    image_bounds = None
    while image_bounds == None:
        try:
            image_bounds = findImage(image)
        except:
            image_bounds = None
        if image_bounds == None:
            time.sleep(0.1)
    log.info("%s found", image)

def click_sun_player():
    log.info("Clicking on the sun player.")
    pyautogui.moveTo(1550, 650, duration=random.random()/2 + 0.25, tween=pyautogui.easeOutQuad)
    pyautogui.click()

def try_buff(spells):
    log.info("Using %s to try to buff a spell.", spells)
    result = False
    if len(spells) == 2:
        buffer = findImage(spells[0])
        spell = findImage(spells[1])
        if buffer != None and spell != None:
            cast_spells(spells)
            time.sleep(0.4)
            result = True
    else:
        log.info("try_buff wants the buffer and the spell, but the length of the input was %d (%s).", len(spells), spells)
        return False
    log.info("able to buff?  %s", result)
    return result

def try_to_blade():
    log.info("Trying to case a blade.")
    bladed = False
    try_buff([CONST.FIGHT_SPELL_BLADE_BUFFER, CONST.FIGHT_SPELL_BLADE])
    buffed = findImage(CONST.FIGHT_SPELL_BLADE_BUFFED)
    if (buffed != None):
        cast_spells([CONST.FIGHT_SPELL_BLADE_BUFFED])
        bladed = True
    else:
        naked = findImage(CONST.FIGHT_SPELL_BLADE)
        if (naked != None):
            cast_spells([CONST.FIGHT_SPELL_BLADE])
            bladed = True
    if bladed:
        click_sun_player()
    log.info("able to blade?  %s", bladed)
    return bladed

def cast_spells(spells):
    log.info("Casting %s this turn.", spells)
    for spell in spells:
        safe_click_image(spell)

def inventory_calibrate():
    log.info("Calibrating inventory.")
    try:
        safe_click_image(CONST.INV_START)
        return True
    except:
        pass
    try:
        safe_click_image(CONST.INV_START_2)
        return True
    except:
        return False

def trash_all_items(category):
    log.info("Trashing all %s.", category)
    safe_click_image(category)
    x, y = pyautogui.center(findImage(CONST.INV_EQUIPPED))
    pyautogui.moveTo(x+100, y+50)
    time.sleep(0.1)
    pyautogui.click()
    
    while(findImage(CONST.INV_TRASH)):    
        try:
            safe_click_image(CONST.INV_TRASH)
        except:
            break
        safe_click_image(CONST.INV_TRASH_CONFIRM)

def feed_pet_all_items(category):
    log.info("Feeding pet all %s.", category)
    safe_click_image(category)
    x, y = pyautogui.center(findImage(CONST.INV_EQUIPPED))
    pyautogui.moveTo(x+100, y+50)
    time.sleep(0.1)
    pyautogui.click()
    
    while(findImage(CONST.INV_FEED_PET)):    
        try:
            safe_click_image(CONST.INV_FEED_PET)
        except:
            break
        safe_click_image(CONST.INV_FEED_PET_CONFIRM)
        time.sleep(0.25)
        found = findOneOfImage([CONST.INV_FINISH_PET_IMPROVEMENT, CONST.INV_FEED_PET_CONFIRM, CONST.INV_PETS])
        if (found == CONST.INV_FINISH_PET_IMPROVEMENT):
            safe_click_image(CONST.INV_FINISH_PET_IMPROVEMENT)
            time.sleep(0.1)

def pass_turn():
    if not try_to_blade():
        log.info("Passing since could blade.")
        safe_click_image(CONST.FIGHT_PASS)
        time.sleep(1)
    wait_for_image(CONST.FIGHT_PASS)

def fight_battle():
    log.info("Fighting the battle")
    wait_for_image(CONST.FIGHT_PASS)
    pips = findOneOfImage([CONST.FIGHT_POWER_PIPS_2, CONST.FIGHT_POWER_PIPS_1, CONST.FIGHT_POWER_PIPS_0])
    if pips == CONST.FIGHT_POWER_PIPS_0 or pips == CONST.FIGHT_POWER_PIPS_1:
        pass_turn()
    activity = CONST.FIGHT_PASS
    while activity == CONST.FIGHT_PASS:
        cast_spells([CONST.FIGHT_SPELL_BUFFER, CONST.FIGHT_SPELL_4_PIPS, CONST.FIGHT_SPELL_4_PIPS_BUFFED])
        activity = findOneOfImage([CONST.FIGHT_PASS, CONST.IDLE], 120, .5)
        if activity == CONST.FIGHT_PASS:
            pass_turn()
            # Could have two single pips, one power pip and a single, or two power pips.
            pips = findOneOfImage([CONST.FIGHT_POWER_PIPS_2, CONST.FIGHT_POWER_PIPS_1, CONST.FIGHT_POWER_PIPS_0], 1, .1)
            match pips:
                case CONST.FIGHT_POWER_PIPS_0:
                    pass_turn()
                case CONST.FIGHT_POWER_PIPS_1:
                    pass_turn()
                case None:
                    pass_turn()
            # currently not handling the case where we get 3 single pips.  That's stupid
    log.info("Battle complete")

def clear_inventory():
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

def couchpotatoes():
    while True:
        for until_out_of_mana in range(2):
            # 40 battles
            for until_backpack_full in range(40):
                log.info("until_out_of_mana = %d, until_backpack_full = %d", until_out_of_mana, until_backpack_full)
                fight_battle()
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
        except:
            print("No more potions. Guess we're done farming!")
            raise SystemExit

def rattlebones():
    while True:
        for a in range(2):
            # 40 battles
            for b in range(40):
                print("a = {}, b = {}".format(a, b))
                fight_battle()
                hold('a', 680)
                hold('w', 3000)
                wait_for_image(IDLE)
                hold('s', 1000)
                wait_for_image(IDLE)
                hold('w', 2500)
            clear_inventory()
            
        # pop a potion to continue farming -- 320 mana used
        try:
            safe_click_image(CONST.POTION)
        except:
            print("No more potions. Guess we're done farming!")
            raise SystemExit
            
def instructions():
    print("1. Set your Wizard101 to be 1920x1080, windowed mode.")
    print("2. In combat, take a screenshot of a small part of your card's picture and save it here as \"spell.png\".")
    print("3. Clear your inventory as much as possible. Remove ALL hats, robes, boots, and mounts you care about (other than what you have equipped) from your inventory. Items in these categories get deleted.")
    pyautogui.moveTo(1920/2,1080/2)
    print("4. Your mouse has been moved to the monitor where Wizard101 should be placed. Please move the window to that monitor.")
    input("Press ENTER to start the bot. After hitting ENTER, begin the battle you wish to farm..")

    #print("Starting in 5 seconds...")
    #time.sleep(5)
    pyautogui.moveTo(250, 250)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(module)s:%(funcName)s:%(lineno)d %(message)s")
    instructions();
    couchpotatoes()