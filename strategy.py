"""Base class with many building blocks for creating strategies / scripts."""

import logging
import time
from pyautogui import ImageNotFoundException

import primitives
from const import Const
from battle_position import BattlePosition

_pet_food_categories=[
    Const.INV_HATS, Const.INV_ROBES, Const.INV_BOOTS,
    Const.INV_WANDS, Const.INV_ATHAMES, Const.INV_AMULETS, Const.INV_RINGS,]
_trash_categories=[Const.INV_PETS, Const.INV_MOUNTS]

class Strategy:
    """Base class with methods to build more complex behaviors."""
    def __init__(self, name, logger):
        self.strategy_name = name
        self.log = logger
        self.common_equipment_categories=[
            Const.INV_HATS, Const.INV_ROBES, Const.INV_BOOTS,
            Const.INV_WANDS, Const.INV_ATHAMES, Const.INV_AMULETS, Const.INV_RINGS,
            Const.INV_PETS, Const.INV_MOUNTS,
        ]

    def move_forward(self, duration):
        """Move forward ('w') for some milliseconds"""
        primitives.hold('w', duration)

    def move_backward(self, duration):
        """Move backward ('s') for some milliseconds"""
        primitives.hold('s', duration)

    def turn_left(self, duration):
        """Turn left ('a') for some milliseconds"""
        primitives.hold('a', duration)

    def turn_right(self, duration):
        """Turn right ('d') for some milliseconds"""
        primitives.hold('d', duration)

    def press(self, key):
        """Press the given key on the keyboard"""
        primitives.press(key)

    def click_position(self, position):
        """Click on the given battle position

        Click on a battle position.  Can be a teammate for a beneficial spell such as
        healing or blades.  Can be an opponent to target them with a trap or an attack spell.

        Args:
            position (Position): which battle position to click to select
        """
        self.log.info("Clicking on %s", position)
        primitives.move_mouse_to((position.click_x, position.click_y))
        primitives.click()

    def inventory_calibrate(self):
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
        self.log.info("Calibrating inventory.")
        try:
            primitives.safe_click_image(Const.INV_START)
            return True
        except ImageNotFoundException:
            pass
        try:
            primitives.safe_click_image(Const.INV_START_2)
            return True
        except ImageNotFoundException:
            return False

    def trash_all_items(self, category):
        """Throws the non-equipped items in this category in the trash.

        Typically used for pets and mounts, which can not be fed to pets.  For normal equipement,
        using feed_pet_all_items gets some benefit for the item destruction.

        Args:
            category (string): The filename of the backpack tab for which non-equiped items
                will be thrown in the trash.
        """
        self.log.info("Trashing all %s.", category)
        primitives.safe_click_image(category)
        primitives.move_mouse((0, -200))
        x_loc, y_loc = primitives.center_of(primitives.find_image(Const.INV_EQUIPPED))
        primitives.move_mouse_to((x_loc+100, y_loc+50))
        time.sleep(0.1)
        primitives.click()

        while primitives.find_image(Const.INV_TRASH):
            try:
                primitives.safe_click_image(Const.INV_TRASH)
            except ImageNotFoundException:
                break
            primitives.safe_click_image(Const.INV_TRASH_CONFIRM)
            time.sleep(0.25)

    def count_pips(self, position):
        """Count how many pips the given position has available."""
        return primitives.count_pips(position)

    def feed_pet_all_items(self, category):
        """Feeds non-equipped items in this category to the current pet.

        Args:
            category (string): The filename of the backpack tab for which non-equiped items
                will be fed to the current pet.
        """
        self.log.info("Feeding pet all %s.", category)
        primitives.safe_click_image(category)
        primitives.move_mouse((0, -200))
        x_loc, y_loc = primitives.center_of(primitives.find_image(Const.INV_EQUIPPED))
        primitives.move_mouse_to((x_loc+100, y_loc+50))
        time.sleep(0.1)
        primitives.click()

        while primitives.find_image(Const.INV_FEED_PET):
            try:
                primitives.safe_click_image(Const.INV_FEED_PET)
            except ImageNotFoundException:
                break
            primitives.safe_click_image(Const.INV_FEED_PET_CONFIRM)
            time.sleep(0.25)
            found = primitives.find_one_of_images([Const.INV_FINISH_PET_IMPROVEMENT,
                                        Const.INV_FEED_PET_CONFIRM,
                                        Const.INV_PETS])
            if found == Const.INV_FINISH_PET_IMPROVEMENT:
                primitives.safe_click_image(Const.INV_FINISH_PET_IMPROVEMENT)
                time.sleep(0.1)

    def clear_inventory(self, categories):
        """Get rid of items to avoid filling the backpack.
        """
        # clear inventory of junk
        primitives.press(Const.INV_OPEN_CLOSE)
        if self.inventory_calibrate():
            for category in categories:
                if category in _pet_food_categories:
                    self.feed_pet_all_items(category)
                elif category in _trash_categories:
                    self.trash_all_items(category)
                else:
                    self.log.error("Cannot determine how to clear %s", category)
        primitives.press(Const.INV_OPEN_CLOSE)

    def use_potion(self):
        """Try to use a potion
        
        If we cannot use a potion, the script is forced to exit.
        """
        try:
            primitives.safe_click_image(Const.POTION)
        except ImageNotFoundException as no_potions:
            print("No more potions. Guess we're done farming!")
            raise SystemExit from no_potions

    def am_in_battle(self):
        """Looks for an indication that the battle is progressing

        If the "PASS" button is visilble, for sure the battle is not over.
        If IDLE, DIALOG_DONE, or DIALOG_MORE is found, then the battle is over.
        """
        indicators = [Const.FIGHT_PASS, Const.IDLE, Const.DIALOG_MORE, Const.DIALOG_DONE]
        found = primitives.find_one_of_images(indicators, 120, .5)
        result = found == Const.FIGHT_PASS
        self.log.info("Found = %s, returning %s", found, result)
        return result

    def be_a_leach_in_battle(self):
        """Just pass every turn"""
        self.log.info("Leaching in the battle")
        primitives.wait_for_image(Const.FIGHT_PASS)
        while self.am_in_battle():
            primitives.safe_click_image(Const.FIGHT_PASS)
            primitives.move_mouse((0, -100))
            time.sleep(1)
        self.log.info("Battle complete")

    def be_a_leach(self, trash=None):
        """Just pass every turn and let someone else do the fighting to leach loot from the fight.

        This scenario waits for a battle to start.  Clicks pass until the battle ends,
        moves a little, and then does it all again.

        Args:
            trash (list(string)): List of inventory items (found in Const) that can be disposed
                of automatically.  By default, it disposes all common equipment types.
        """
        if trash is None:
            trash = self.common_equipment_categories

        while True:
            for until_out_of_mana in range(60000):
                for until_backpack_full in range(15):
                    self.log.info("until_out_of_mana = %d, until_backpack_full = %d",
                            until_out_of_mana, until_backpack_full)
                    self.be_a_leach_in_battle()
                    primitives.hold('w', 300)
                    primitives.hold('s', 100)
                primitives.hold('s', 2000)
                self.clear_inventory(trash)
                primitives.hold('w', 1500)

    def enter_dungeon(self):
        """Enter an instance dungeon.

        Verify that the X is on the screen.
        Press the X.
        Wait for 12 seconds.
        Wait for idle.

        Return:
            True (boolean): Successfully entered the dungeon.
            False (booelan): Failed to enter the dungeon.
        """
        result = False
        if primitives.find_one_of_images([Const.ENTER_DUNGEON], 50):
            primitives.hold('x', 100)
            time.sleep(0.1)
            if primitives.find_one_of_images([Const.GO_IN_DUNGEON], 10):
                primitives.safe_click_image(Const.GO_IN_DUNGEON)
            time.sleep(12)
            primitives.wait_for_image(Const.IDLE)
            result = True
        return result

    def do_not_exit_dungeon(self):
        """If prompted to exit the dungeon, pick no."""
        result = False
        if primitives.find_one_of_images([Const.EXIT_DUNGEON], 50):
            primitives.safe_click_image(Const.EXIT_DUNGEON_NO)
            result = True
        return result

    def complete_dialog(self):
        """Press space to move through the dialog until complete."""
        found = primitives.find_one_of_images([Const.DIALOG_MORE, Const.DIALOG_DONE], 5)
        while found is not None:
            primitives.press(' ')
            time.sleep(.1)
            found = primitives.find_one_of_images([Const.DIALOG_MORE, Const.DIALOG_DONE], 1)
            if found == Const.DIALOG_DONE:
                primitives.press(' ')
                time.sleep(.1)
                break

    def try_buff(self, spells):
        """Try to use the buffer spell to buff the spell

        Args:
            spells (buffer(string), target_spell(string)): A tuple of the spell to use to buff
                the spell and the spell to buff.

        Returns:
            True: The target_spell was able to be buffed.
            False: Either the buffer or the target_spell was not found.
        """
        self.log.info("Using %s to try to buff a spell.", spells)
        result = False
        if len(spells) == 2:
            spell = primitives.find_image(spells[1])
            if spell is not None:
                buffer = primitives.find_image(spells[0])
                if buffer is not None:
                    self.cast_spells(spells)
                    primitives.move_mouse((0, -100))
                    # Wait for the buff ripple effect to complete.
                    time.sleep(0.4)
                    result = True
        else:
            self.log.error("invalid input: the length of the input was %d (%s), expected 2.",
                            len(spells), spells)
            return False
        self.log.info("able to buff using %s?  %s", spells, result)
        return result

    def try_buff_blade(self, target_blade):
        """Try to buff the given target_blade

        Attempts to use the any of the many blade buffs to buff the target_blade.

        Args:
            target_blade (string): The filename of the blade to buff.

        Returns:
            True: The target_blade was able to be buffed.
            False: Either a buffer or the target_blade was not found.
        """
        result = False
        self.log.info("Trying to buff %s", target_blade)
        blade = primitives.find_image(target_blade)
        if blade is not None:
            buffer = primitives.find_image(Const.FIGHT_SPELL_BLADE_BUFFER_1, 0.85)
            if buffer is None:
                buffer = primitives.find_image(Const.FIGHT_SPELL_BLADE_BUFFER_2, 0.85)
            self.log.info("buffer = %s; blade = %s", buffer, blade)
            if buffer is not None:
                primitives.move_mouse_to(primitives.center_of(buffer))
                primitives.click()
                primitives.move_mouse((0, -200))
                primitives.safe_click_image(target_blade, 0.85)
                primitives.move_mouse((0, -200))
                    # Wait for the buff ripple effect to complete.
                time.sleep(.4)
                result = True
            else:
                self.log.debug("buffer is not found.")
        else:
            self.log.debug("blade is not found.")
        self.log.info("Was blade buffed?  %s", result)
        return result

    def try_to_blade(self, position = BattlePosition.SUN):
        """Try to cast a blade on wizard at the given position.

        Attempts to buff a blade if possible, and then cast the buffed blade or
        an unbuffed blade if it was not possible to buff one.

        Args:
            position (Position): Which battle position to target with the blade.

        Returns:
            True: It was possible to blade the target position.
            False: It was not possible to cast a blade.
        """
        self.log.info("Trying to cast a blade.")
        bladed = False
        self.try_buff_blade(Const.FIGHT_SPELL_BLADE)
        primitives.move_mouse((0, -250))
        time.sleep(0.25)
        buffed = primitives.find_image(Const.FIGHT_SPELL_BLADE_BUFFED)
        if  buffed is not None:
            self.cast_spells([Const.FIGHT_SPELL_BLADE_BUFFED])
            bladed = True
        else:
            naked = primitives.find_image(Const.FIGHT_SPELL_BLADE)
            if naked is not None:
                self.cast_spells([Const.FIGHT_SPELL_BLADE])
                bladed = True
        if bladed:
            self.click_position(position)
        self.log.info("able to blade?  %s", bladed)
        return bladed

    def cast_spells(self, spells, target=None):
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
        self.log.info("Casting %s this turn.", spells)
        for spell in spells:
            primitives.safe_cast_spell(spell)
            time.sleep(0.2)
        if target is not None:
            self.click_position(target)
        else:
            time.sleep(0.1)
            primitives.move_mouse((0, -150))

    def blade_or_pass(self, position = BattlePosition.SUN):
        """Cannot attack, so pass this turn in battle.

        If the current deck has blades, if the current hand has a blade, cast that instead
        of passing.  If the current hand has a buffer, the blade will be buffed before cast.
        If the current hand does not have any blades in it, the pass button is clicked.

        Args:
            position (Position, optional): The position that should benefit from passing this
                turn. Defaults to Position.SUN.
        """
        if not self.try_to_blade(position):
            self.log.info("Passing since could not blade.")
            primitives.safe_click_image(Const.FIGHT_PASS)
            primitives.move_mouse((0, -100))
            time.sleep(1)

    def pass_turn(self):
        """Pass the turn"""
        primitives.safe_click_image(Const.FIGHT_PASS)
        primitives.move_mouse((0, -100))
        time.sleep(1)

    def fight_simple_7pip_aoe_battle(self, need_key, player_name):
        """Fight a simple 7 pip AoE battle.
        
        Blade until 7 pips and then cast 7 pip spell.
        """
        position = primitives.battle_position_of(player_name)
        if position is None:
            self.log.info("Guessing position...")
            position = BattlePosition.SUN
        self.log.info("Fighting the battle from %s", position)
        primitives.wait_for_image(Const.FIGHT_PASS)
        pips = self.count_pips(position)
        if need_key:
            key_pips = self.count_pips(BattlePosition.KEY)
        else:
            key_pips = 5
        if key_pips == 0 or pips < 4:
            self.blade_or_pass(position)
            primitives.wait_for_image(Const.FIGHT_PASS)


    def fight_4pip_aoe_battle(self, need_key, position = BattlePosition.SUN):
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
        - one blade buffer card (either sharpened blade, level 86 sun school or enchanted
          armament pet)
        - two blades
        - two/three 4 pip AoE cards
        The pattern will be to cast the attack spell every time the caster has four pips.  At
        the beginning, if there are less than four pips or if key has not yet joined the battle,
        then the script will blade if possible or pass the turn if blades are not available.
        After that, whenever there are four pips, the script will attempt to cast the AoE, and
        the rest of the time either pass or blade.
        """
        self.log.info("Fighting the battle from %s", position)
        primitives.wait_for_image(Const.FIGHT_PASS)
        pips = self.count_pips(position)
        if need_key:
            key_pips = self.count_pips(BattlePosition.KEY)
        else:
            key_pips = 5
        if key_pips == 0 or pips < 4:
            self.blade_or_pass(position)
            primitives.wait_for_image(Const.FIGHT_PASS)
        while self.am_in_battle():
            self.cast_spells([Const.FIGHT_SPELL_BUFFER,
                                Const.FIGHT_SPELL_4_PIPS,
                                Const.FIGHT_SPELL_4_PIPS_BUFFED])
            time.sleep(.1)
            if self.am_in_battle():
                while self.count_pips(position) < 4:
                    self.blade_or_pass(position)
                    primitives.wait_for_image(Const.FIGHT_PASS)
        self.log.info("Battle complete")

    def help_fight_4pip_aoe_battle(self, position):
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
        self.log.info("Help fighting the battle")
        primitives.wait_for_image(Const.FIGHT_PASS)
        self.try_buff_blade(Const.FIGHT_SPELL_SPIRIT_BLADE)
        self.try_buff_blade(Const.FIGHT_SPELL_BLADE)
        activity = Const.FIGHT_PASS
        while activity == Const.FIGHT_PASS:
            if primitives.find_image(Const.FIGHT_SPELL_SPIRIT_BLADE_BUFFED):
                self.cast_spells([Const.FIGHT_SPELL_SPIRIT_BLADE_BUFFED], position)
            elif primitives.find_image(Const.FIGHT_SPELL_BLADE_BUFFED):
                self.cast_spells([Const.FIGHT_SPELL_BLADE_BUFFED], position)
            elif primitives.find_image(Const.FIGHT_SPELL_SPIRIT_BLADE):
                self.cast_spells([Const.FIGHT_SPELL_SPIRIT_BLADE], position)
            elif primitives.find_image(Const.FIGHT_SPELL_BLADE):
                self.cast_spells([Const.FIGHT_SPELL_BLADE], position)
            else:
                self.pass_turn()
                primitives.wait_for_image(Const.FIGHT_PASS)
            activity = primitives.find_one_of_images([Const.FIGHT_PASS, Const.IDLE], 120, .5)
            self.log.info("Current activity = {}", activity)
        self.log.info("Battle complete")

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format=(
        "%(asctime)s "
        "%(levelname)s "
        "%(module)s:%(funcName)s:%(lineno)d "
        "%(message)s"))
    #time.sleep(3)
    s = Strategy("test", logging.getLogger("test"))
    s.try_buff_blade(Const.FIGHT_SPELL_BLADE)
    #s.clear_inventory([Const.INV_HATS, Const.INV_ROBES,
    #                                  Const.INV_BOOTS, Const.INV_RINGS])
