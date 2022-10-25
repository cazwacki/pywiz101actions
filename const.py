"""Constants for Wizard101"""

WIZ_TYPE = "ice"

class Const:
    """Holds many constants, primarily for graphic elements on screen.
    """

    def __init__(self, wiz_type):
        if wiz_type is None:
            wiz_type = "ice"
        self.FIGHT_SPELL_4_PIPS = wiz_type + '/' + 'p4_spell.png'
        self.FIGHT_SPELL_4_PIPS_BUFFED = wiz_type + '/' + 'p4_spell_buffed.png'
        self.FIGHT_SPELL_BLADE = wiz_type + '/' + 'blade.png'
        self.FIGHT_SPELL_BLADE_BUFFED = wiz_type + '/' + 'blade_buffed.png'

    # 1920x1080 borderless:

    # pyautogui.screenshot('idle.png', region=(1660, 915, 25, 45))
    # pyautogui.screenshot('common/enter_dungeon.png', region=(700, 930, 70, 60))
    # pyautogui.screenshot('common/go_in_dungeon.png', region=(930, 765, 85, 25))
    # pyautogui.screenshot('common/exit_dungeon.png', region=(910, 390, 90, 35))
    # pyautogui.screenshot('common/exit_dungeon_yes.png', region=(940, 680, 60, 30))
    # pyautogui.screenshot('common/exit_dungeon_no.png', region=(1130, 680, 60, 30))
    IDLE = 'common/idle.png'
    ENTER_DUNGEON = 'common/enter_dungeon.png'
    GO_IN_DUNGEON = 'common/go_in_dungeon.png'
    EXIT_DUNGEON = 'common/exit_dungeon.png'
    EXIT_DUNGEON_YES = 'common/exit_dungeon_yes.png'
    EXIT_DUNGEON_NO = 'common/exit_dungeon_no.png'

    # pyautogui.screenshot('common/dialog_done.png', region=(1300, 1040, 100, 25))
    # pyautogui.screenshot('common/dialog_more.png', region=(1300, 1040, 100, 25))
    DIALOG_MORE = 'common/dialog_more.png'
    DIALOG_DONE = 'common/dialog_done.png'

    # pyautogui.screenshot('potion.png', region=(400, 990, 15, 15))
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

if __name__ == "__main__":
    import pyautogui
    import time
    time.sleep(3)
    pyautogui.screenshot('pips_power_1.png', region=(1525, 1055, 15, 12))
