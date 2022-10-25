"""Constants about the battle positions."""
from enum import Enum

screen_offset=(0, 0)

PIP_WIDTH=160
PIP_HEIGHT=27
NAME_WIDTH=100
NAME_HEIGHT=27

class BattlePosition(Enum):
    """Describes the different positions on the battle board.

    SUN, EYE, STAR, and MOON represent player positions.
    DAGGER, KEY, RUBY, and SPIRAL represent opponent positions.
    """
    SUN = ((1550, 650), (1520, 1042), (1525, 987))
    EYE = ((1250, 900), (1105, 1042), (1110, 987))
    STAR = ((675, 900), (690, 1042), (695, 987))
    MOON = ((375, 650), (0, 1042), (0, 987))
    DAGGER = ((500, 950), (155, 0), (0, 0))
    KEY = ((500, 950), (580, 0), (0, 0))
    RUBY = ((500, 950), (1010, 0), (0, 0))
    SPIRAL = ((500, 950), (1432, 0), (0, 0))

    def __init__(self, click_pos, pip_pos, name_pos):
        """Initializes the location of various elements of a position.

        Args:
            click_pos (x(int), y(int)): Where to click on the screen to select the entity
                in this location.
            pip_pos (x(int), y(int)): The top-left corner of the position where the entity's
                pips are located.
        """
        self.click_position = (click_pos[0] + screen_offset[0], click_pos[1] + screen_offset[1])
        self.pip_pos = (pip_pos[0] + screen_offset[0], pip_pos[1] + screen_offset[1])
        self.name_pos = (name_pos[0] + screen_offset[0], name_pos[1] + screen_offset[1])

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
        return self.pip_pos[0]

    @property
    def pip_top(self):
        """The Y screen location from which to start looking for pips for this position."""
        return self.pip_pos[1]

    @property
    def pips_position(self):
        """The screen region from which to start looking for pips for this position."""
        return (self.pip_pos[0], self.pip_pos[1], PIP_WIDTH, PIP_HEIGHT)

    @property
    def name_position(self):
        """The screen region from which to start looking for pips for this position."""
        return (self.name_pos[0], self.name_pos[1], NAME_WIDTH, NAME_HEIGHT)

    def __str__(self):
        return self.name
