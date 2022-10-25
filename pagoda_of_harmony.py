"""Run the Pagoda of Harmony dungeon."""

import logging

from strategy import Strategy

class PagodaOfHarmony(Strategy):
    """Run the Pagoda of Harmony dungeon.

    Scenario assumes that you are in Kembraalung Villiage standing on the dungeon entrance.
    """

    def __init__(self):
        self.log = logging.getLogger(__name__)
        Strategy.__init__(self, __name__, self.log)

    def explore_pagoda(self):
        """Trigger dialogs and get to a known starting location."""
        self.log.info("Moving to known location")
        self.move_backward(3000)
        self.do_not_exit_dungeon()
        self.complete_dialog()
        self.log.info("At known location")

    def talk_to_dalai_lamba(self):
        """Go to dalai lambda and talk to him."""
        self.log.info("Going to dalai lamba")
        self.move_forward(1000)
        self.turn_right(600)
        self.move_forward(2000)
        self.log.info("Talking to dalai lamba")
        self.press('x')
        self.complete_dialog()
        self.log.info("Done tlaking to dalai lamba")

    def fight_ice_spirit_monks(self):
        """Go to the center of the pagoda and defeat the ice spirit monks."""
        self.log.info("Turn back towards entrance area")
        self.turn_left(900)
        self.log.info("Go to entrance area")
        self.move_forward(2000)
        self.log.info("Turning towards center")
        self.turn_right(800)
        self.log.info("Interacting with ice monks")
        self.move_forward(2000)
        self.complete_dialog()
        self.move_forward(2000)
        self.log.info("Battling ice monks")
        self.fight_4pip_aoe_battle(True)
        self.complete_dialog()
        self.log.info("Fighting ice monks complete")

    def use_shrine(self):
        """After battle, from eye, go to shrine and use it."""
        self.log.info("Turning towards shrine")
        self.turn_left(150)
        self.move_forward(5000)
        self.press('x')
        self.complete_dialog()
        self.log.info("Using shrine complete")

    def go_from_shrine_to_next_level(self):
        """Go to the next level of the pagoda."""
        self.turn_left(2200)
        self.move_forward(4000)
        self.turn_left(750)
        self.move_forward(7000)

    def fight_fire_spirit_monks(self):
        """Go to the center of the pagoda and defeat the fire spirit monks"""
        self.log.info("Interacting with fire monks")
        self.complete_dialog()
        self.move_forward(4000)
        self.log.info("Battling fire monks")
        self.fight_4pip_aoe_battle(True)
        self.complete_dialog()
        self.log.info("Fighting fire monks complete")

    def run_pagoda_of_harmony(self):
        """Execute the complete pagoda of harmony strategy"""
        self.enter_dungeon()
        self.explore_pagoda()
        self.talk_to_dalai_lamba()
        self.fight_ice_spirit_monks()
        self.use_shrine()
        self.go_from_shrine_to_next_level()
        self.fight_fire_spirit_monks()
        self.use_shrine()
        self.go_from_shrine_to_next_level()

    def run(self):
        """Run the script"""
        while True:
            self.run_pagoda_of_harmony()

if __name__ == "__main__":
    import time
    logging.basicConfig(level=logging.INFO, format=(
        "%(asctime)s "
        "%(levelname)s "
        "%(module)s:%(funcName)s:%(lineno)d "
        "%(message)s"))
    s = PagodaOfHarmony()
    time.sleep(3)
    s.run_pagoda_of_harmony()
