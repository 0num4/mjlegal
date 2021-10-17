import unittest

from mjlegal.mjtypes import TilesUtil
from mjlegal.player_state import PlayerState
from mjlegal.game_state import GameState
from mjlegal.mjtypes import Meld

class TestPlayerState(unittest.TestCase) :
    def test_player_state(self) :
        tiles = TilesUtil.str_to_tiles("789m456p555s1123z")
        ps = PlayerState()
        ps.tiles = tiles

        self.assertEqual(TilesUtil.tiles_to_str(ps.tiles), "789m456p555s1123z")
    
        # tsumogiri
        ps.tsumo("1z")
        ps.dahai("1z")
        self.assertEqual(TilesUtil.tiles_to_str(ps.tiles), "789m456p555s1123z")

        ps.tsumo("5pr")
        ps.dahai("7m")
        ps.tsumo("5mr")
        ps.dahai("8m")
        ps.tsumo("5m")
        ps.dahai("9m")
        ps.tsumo("5m")
        ps.dahai("5p")
        self.assertEqual(TilesUtil.tiles_to_str(ps.tiles), "055m406p555s1123z")
        self.assertEqual(TilesUtil.tiles_to_str(ps.melds), "")

        # pon
        ps.pon("1z", ["1z", "1z"], 1)
        ps.dahai("2z")
        self.assertEqual(TilesUtil.tiles_to_str(ps.tiles), "055m406p555s3z")
        self.assertEqual(ps.melds[0].type, Meld.PON)
        self.assertEqual(TilesUtil.tiles_to_str(ps.melds[0].tiles), "111z")

        # kakan
        ps.tsumo("1z")
        ps.kakan("1z")
        self.assertEqual(TilesUtil.tiles_to_str(ps.tiles), "055m406p555s3z")
        self.assertEqual(ps.melds[0].type, Meld.KAKAN)
        self.assertEqual(TilesUtil.tiles_to_str(ps.melds[0].tiles), "1111z")

        # ankan
        ps.tsumo("0s")
        ps.ankan(["5s","5s","5s","0s"])
        self.assertEqual(TilesUtil.tiles_to_str(ps.tiles), "055m406p3z")
        self.assertEqual(ps.melds[0].type, Meld.KAKAN)
        self.assertEqual(TilesUtil.tiles_to_str(ps.melds[0].tiles), "1111z")
        self.assertEqual(ps.melds[1].type, Meld.ANKAN)
        self.assertEqual(TilesUtil.tiles_to_str(ps.melds[1].tiles), "0555s")
