import unittest
import json
from mjlegal.game_state import GameState
from mjlegal.player_state import PlayerState
from mjlegal.possible_action import PossibleActionGenerator
from mjlegal.mjai import MjaiLoader
from mjlegal.hand_tool import HandTool
from mjlegal.mjtypes import Tile, TilesUtil
from mjlegal.mjtypes import ActionType
from mjlegal.action import Action
from mahjong.hand_calculating.divider import HandDivider


class TestTile(unittest.TestCase) :
    def test_tile_5p(self) :
        self.assertEqual(Tile.from_str("0p").to_mjai_str(), "5pr")

