"""Run the Pagoda of Harmony dungeon."""

import logging

from strategy import Strategy

class BattleLordNightshade(Strategy):
    """Fight Lord Nightshade

    Scenario assumes that you are in the haunted cave at Stormdrain Tower
    standing on the dungeon entrance.
    """

    def __init__(self):
        self.log = logging.getLogger(__name__)
        Strategy.__init__(self, __name__, self.log)

    def battle_lord_nightshade(self):
        """Execute Lord Nightshade"""
        self.enter_dungeon()
        self.move_forward(1500)
        self.fight_4pip_aoe_battle()
        self.turn_left(650)
        self.move_forward(2000)

    def run(self):
        """Run the script"""
        while True:
            self.battle_lord_nightshade()

if __name__ == "__main__":
    import time
    logging.basicConfig(level=logging.INFO, format=(
        "%(asctime)s "
        "%(levelname)s "
        "%(module)s:%(funcName)s:%(lineno)d "
        "%(message)s"))
    s = BattleLordNightshade()
    time.sleep(3)
    s.run()
