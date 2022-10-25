"""Fight Splithoof Barbarians to farm couch potatoes."""

import logging

from const import Const
from strategy import Strategy

class FarmCouchPotatoes(Strategy):
    """Farm Couch Potatoes

    Scenario assumes that you are fighting in the front section of the boar camp.

    Scenario clears the following inventory items:
    - Hats
    - Robes
    - Boots
    - Athames
    - Amulets
    - Rings
    - Pets
    - Mounts
    """

    def __init__(self):
        self.log = logging.getLogger(__name__)
        Strategy.__init__(self, __name__, self.log)

    def battle_barbarians(self):
        """Fight barbarians"""
        self.fight_4pip_aoe_battle(True)
        self.turn_left(250)
        self.move_forward(1000)

    def run(self):
        """Run the script"""
        while True:
            for until_out_of_mana in range(4, 0, -1):
                for until_backpack_full in range(25, 0, -1):
                    self.log.info("until_out_of_mana = %d, until_backpack_full = %d",
                             until_out_of_mana, until_backpack_full)
                    self.battle_barbarians()
                self.move_backward(1000)
                self.turn_right(250)
                self.move_backward(2500)
                self.clear_inventory([Const.INV_HATS, Const.INV_ROBES,
                                      Const.INV_BOOTS, Const.INV_ATHAMES,
                                      Const.INV_RINGS])
                self.move_forward(2500)
                self.turn_left(250)
                self.move_forward(1000)
            self.battle_barbarians()
            self.move_backward(1000)
            self.turn_right(250)
            self.move_backward(2500)
            self.use_potion()
            self.move_forward(2500)
            self.turn_left(250)
            self.move_forward(1000)

if __name__ == "__main__":
    import time
    logging.basicConfig(level=logging.DEBUG, format=(
        "%(asctime)s "
        "%(levelname)s "
        "%(module)s:%(funcName)s:%(lineno)d "
        "%(message)s"))
    s = FarmCouchPotatoes()
    time.sleep(3)
    s.run()
