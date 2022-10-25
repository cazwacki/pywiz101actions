"""Run the Pagoda of Harmony dungeon."""

import logging

from strategy import Strategy
from const import Const

class BattleKraken(Strategy):
    """Fight the Kraken

    Scenario assumes that you are facing the Kraken on Triton Avenue on Kraken Isle.

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

    def battle_kraken(self):
        """Execute Kraken"""
        self.fight_4pip_aoe_battle(False)
        self.turn_right(250)
        self.move_forward(1000)

    def run(self):
        """Run the script"""
        while True:
            for battles_before_popping_a_potion in range(2, 0, -1):
                # 40 battles
                self.move_forward(1500)
                for battles_before_clearing_inventory in range(50, 0, -1):
                    self.log.info(("battles_before_popping_a_potion = %d, "
                            "battles_before_clearing_inventory = %d"),
                            battles_before_popping_a_potion, battles_before_clearing_inventory)
                    self.battle_kraken()
                self.move_backward(2000)
                self.clear_inventory([Const.INV_HATS, Const.INV_ROBES,
                                    Const.INV_BOOTS, Const.INV_WANDS,
                                    Const.INV_ATHAMES, Const.INV_RINGS,])

                # pop a potion to continue farming -- 400 mana used
                self.use_potion()


if __name__ == "__main__":
    import time
    logging.basicConfig(level=logging.INFO, format=(
        "%(asctime)s "
        "%(levelname)s "
        "%(module)s:%(funcName)s:%(lineno)d "
        "%(message)s"))
    s = BattleKraken()
    time.sleep(3)
    s.run()
