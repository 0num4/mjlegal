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

def loadGameStateFromMjai(logs) :
    mjl = MjaiLoader()
    for record in logs :
        mjl.action(record)
    return mjl.game

class TestPossibleAction(unittest.TestCase) :
    def test_possible_dahai(self) :
        mjai_log = [{"type":"start_game","names":["shanten","shanten","shanten"]},
                    {"type":"start_kyoku","bakaze":"E","kyoku":1,"honba":0,"kyotaku":0,"oya":0,"dora_marker":"8p","tehais":[["9m","1p","4p","5p","8p","9p","1s","2s","4s","5s","E","F","C"],["9m","1p","2p","3s","3s","3s","7s","8s","9s","S","W","P","P"],["1m","1p","4p","6p","7p","1s","2s","4s","4s","7s","7s","S","S"]]},
                    {"type":"tsumo","actor":0,"pai":"8s"}]
        game_state = loadGameStateFromMjai(mjai_log)

        pag = PossibleActionGenerator()
        dahais = pag.possible_action_dahai(game_state)
        
        expect = [{"type": "dahai", "actor": 0, "pai": "9m", "tsumogiri": False}, 
                {"type": "dahai", "actor": 0, "pai": "1p", "tsumogiri": False}, {"type": "dahai", "actor": 0, "pai": "4p", "tsumogiri": False}, 
                {"type": "dahai", "actor": 0, "pai": "5p", "tsumogiri": False}, {"type": "dahai", "actor": 0, "pai": "8p", "tsumogiri": False}, 
                {"type": "dahai", "actor": 0, "pai": "9p", "tsumogiri": False}, {"type": "dahai", "actor": 0, "pai": "1s", "tsumogiri": False},
                {"type": "dahai", "actor": 0, "pai": "2s", "tsumogiri": False}, {"type": "dahai", "actor": 0, "pai": "4s", "tsumogiri": False}, 
                {"type": "dahai", "actor": 0, "pai": "5s", "tsumogiri": False}, {"type": "dahai", "actor": 0, "pai": "1z", "tsumogiri": False}, 
                {"type": "dahai", "actor": 0, "pai": "6z", "tsumogiri": False}, {"type": "dahai", "actor": 0, "pai": "7z", "tsumogiri": False}, 
                {"type": "dahai", "actor": 0, "pai": "8s", "tsumogiri": True}]
        
        dahais_mjai = [act.to_mjai() for act in dahais]
        dahais_json = json.dumps(dahais_mjai)
        expect_json = json.dumps(expect)
        self.assertEqual(dahais_json, expect_json)

    def test_possible_dahai_kuikae(self) :
        mjai_log = [{"type":"start_game","names":["shanten","shanten","shanten"]},
                    {"type":"start_kyoku","bakaze":"E","kyoku":1,"honba":0,"kyotaku":0,"oya":0,"dora_marker":"8p",
                        "tehais":[["9m","1p","4p","5p","8p","9p","1s","2s","4s","5s","E","F","C"],
                                  ["9m","1p","2p","3s","3s","3s","7s","8s","9s","S","W","P","P"],
                                  ["1m","1p","5p","5p","0p","1s","2s","4s","4s","7s","7s","S","S"]]},
                    {"type":"tsumo","actor":0,"pai":"8s"},
                    {"type":"dahai","actor":0,"pai":"5p","tsumogiri":False},
                    {"type": "pon", "actor": 2, "target": 0, "pai": "5p", "consumed": ["5p", "5p"]}
                    ]
        expect = [{"type": "dahai", "actor": 2, "pai": "1m", "tsumogiri": False}, {"type": "dahai", "actor": 2, "pai": "1p", "tsumogiri": False},{"type": "dahai", "actor": 2, "pai": "1s", "tsumogiri": False}, {"type": "dahai", "actor": 2, "pai": "2s", "tsumogiri": False}, {"type": "dahai", "actor": 2, "pai": "4s", "tsumogiri": False}, {"type": "dahai", "actor": 2, "pai": "4s", "tsumogiri": False}, {"type": "dahai", "actor": 2, "pai": "7s", "tsumogiri": False}, {"type": "dahai", "actor": 2, "pai": "7s", "tsumogiri": False}, {"type": "dahai", "actor": 2, "pai": "2z", "tsumogiri": False}, {"type": "dahai", "actor": 2, "pai": "2z", "tsumogiri": False}]
                # {"type": "dahai", "actor": 2, "pai": "5pr", "tsumogiri": False} # 5prは喰い変え
        game_state = loadGameStateFromMjai(mjai_log)
        pag = PossibleActionGenerator()
        dahais = pag.possible_action_dahai(game_state)
        dahais_mjai = [act.to_mjai() for act in dahais]
        dahais_json = json.dumps(dahais_mjai)
        expect_json = json.dumps(expect)
        self.assertEqual(dahais_json, expect_json)
    
    def test_possible_pon(self) :
        mjai_log = [{"type":"start_game","names":["shanten","shanten","shanten"]},
                    {"type":"start_kyoku","bakaze":"E","kyoku":1,"honba":0,"kyotaku":0,"oya":0,"dora_marker":"8p",
                        "tehais":[["9m","1p","4p","5p","8p","9p","1s","2s","4s","5s","E","F","C"],
                                  ["9m","1p","2p","3s","3s","3s","7s","8s","9s","S","W","P","P"],
                                  ["1m","1p","5p","5p","0p","1s","2s","4s","4s","7s","7s","S","S"]]},
                    {"type":"tsumo","actor":0,"pai":"8s"},
                    {"type":"dahai","actor":0,"pai":"5p","tsumogiri":False}]

        game_state = loadGameStateFromMjai(mjai_log)
        pag = PossibleActionGenerator()
        pons = pag.possible_actions_pon(game_state)
        expect = [{"type": "pon", "actor": 2, "target": 0, "pai": "5p", "consumed": ["5p", "5p"]},
                  {"type": "pon", "actor": 2, "target": 0, "pai": "5p", "consumed": ["5p", "5pr"]}]

        pons_mjai = [act.to_mjai() for act in pons]
        pons_json = json.dumps(pons_mjai)
        expect_json = json.dumps(expect)
        self.assertEqual(pons_json, expect_json)

    def test_possible_ankan(self) :
        mjai_log = [{"type":"start_game","names":["shanten","shanten","shanten"]},
                    {"type":"start_kyoku","bakaze":"E","kyoku":1,"honba":0,"kyotaku":0,"oya":0,"dora_marker":"8p",
                    "tehais":[["9m","1p","4p","0p","5p","5p","1s","2s","4s","E","E","E","E"],
                              ["9m","1p","2p","3s","3s","3s","7s","8s","9s","S","W","P","P"],
                              ["1m","1p","4p","6p","7p","1s","2s","4s","4s","7s","7s","S","S"]]},
                    {"type":"tsumo","actor":0,"pai":"5p"}]
        expect = [{"type": "ankan", "actor": 0, "consumed": ["5pr", "5p", "5p", "5p"]},
                  {"type": "ankan", "actor": 0, "consumed": ["1z", "1z", "1z", "1z"]}]
        game_state = loadGameStateFromMjai(mjai_log)
        pag = PossibleActionGenerator()
        kans = pag.possible_actions_ankan(game_state)
        kans_mjai = [act.to_mjai() for act in kans]
        kans_json = json.dumps(kans_mjai)
        expect_json = json.dumps(expect)
        self.assertEqual(kans_json, expect_json)

    def test_possible_kakan(self) :
        mjai_log = [{"type":"start_game","names":["shanten","shanten","shanten"]},
                    {"type":"start_kyoku","bakaze":"E","kyoku":1,"honba":0,"kyotaku":0,"oya":0,"dora_marker":"8p",
                        "tehais":[["9m","1p","1p","5p","8p","9p","1s","2s","4s","5s","E","F","C"],
                                  ["9m","1p","2p","3s","3s","3s","7s","8s","9s","E","W","P","P"],
                                  ["1m","1p","5p","5p","0p","1s","2s","4s","4s","7s","7s","S","S"]]},
                    {"type":"tsumo","actor":0,"pai":"8s"},
                    {"type":"dahai","actor":0,"pai":"5p","tsumogiri":False},
                    {"type": "pon", "actor": 2, "target": 0, "pai": "5p", "consumed": ["5p", "5p"]},
                    {"type":"dahai","actor":2,"pai":"1m","tsumogiri":False},
                    {"type":"tsumo","actor":0,"pai":"S"},
                    {"type":"dahai","actor":0,"pai":"S","tsumogiri":True},
                    {"type": "pon", "actor": 2, "target": 0, "pai": "S", "consumed": ["S", "S"]},
                    {"type":"dahai","actor":2,"pai":"1p","tsumogiri":False},
                    {"type": "pon", "actor": 0, "target": 0, "pai": "1p", "consumed": ["1p", "1p"]},
                    {"type":"dahai","actor":0,"pai":"F","tsumogiri":False},
                    {"type":"tsumo","actor":1,"pai":"C"},
                    {"type":"dahai","actor":1,"pai":"C","tsumogiri":True},
                    {"type":"tsumo","actor":2,"pai":"S"}
                    ]
        expect = [{"type": "kakan", "actor": 2, "pai": "5pr", "consumed": ["5p", "5p", "5p"]},
                  {"type": "kakan", "actor": 2, "pai": "2z", "consumed": ["2z", "2z", "2z"]}]
        game_state = loadGameStateFromMjai(mjai_log)
        pag = PossibleActionGenerator()
        kans = pag.possible_actions_kakan(game_state)
        kans_mjai = [act.to_mjai() for act in kans]
        kans_json = json.dumps(kans_mjai)
        expect_json = json.dumps(expect)
        self.assertEqual(kans_json, expect_json)

    def test_possible_daiminkan(self) :
        mjai_log = [{"type":"start_game","names":["shanten","shanten","shanten"]},
                    {"type":"start_kyoku","bakaze":"E","kyoku":1,"honba":0,"kyotaku":0,"oya":0,"dora_marker":"8p","tehais":[["9m","1p","4p","5p","8p","9p","1s","2s","4s","5s","E","F","C"],["9m","1p","2p","3s","3s","3s","7s","8s","9s","S","W","P","P"],["1m","1p","5p","5p","0p","1s","2s","4s","4s","7s","7s","S","S"]]},
                    {"type":"tsumo","actor":0,"pai":"8s"},
                    {"type":"dahai","actor":0,"pai":"5p","tsumogiri":False}]

        game_state = loadGameStateFromMjai(mjai_log)
        pag = PossibleActionGenerator()
        kans = pag.possible_actions_daiminkan(game_state)
        expect = [{"type": "daiminkan", "actor": 2, "target": 0, "pai": "5p", "consumed": ["5p", "5p", "5pr"]}]

        kans_mjai = [act.to_mjai() for act in kans]
        kans_json = json.dumps(kans_mjai)
        expect_json = json.dumps(expect)
        self.assertEqual(kans_json, expect_json)

    def test_possible_actions_dahai_with_reach(self) :
        mjai_log = [{"type":"start_game","names":["shanten","shanten","shanten"]},
                    {"type":"start_kyoku","bakaze":"E","kyoku":1,"honba":0,"kyotaku":0,"oya":0,"dora_marker":"8p","tehais":[["1m","2m","3m","4p","0p","6p","5s","7s","8s","E","E","E","C"],["9m","1p","2p","3s","3s","3s","7s","8s","9s","S","W","P","P"],["1m","1p","4p","6p","7p","1s","2s","4s","4s","7s","7s","S","S"]]},
                    {"type":"tsumo","actor":0,"pai":"C"},
                    {"type":"reach","actor":0}]
        game_state = loadGameStateFromMjai(mjai_log)

        pag = PossibleActionGenerator()
        reach_dahai = pag.possible_actions_dahai_with_reach(game_state)
        expect = [{"type": "dahai", "actor": 0, "pai": "5s", "tsumogiri": False}, 
                  {"type": "dahai", "actor": 0, "pai": "8s", "tsumogiri": False}]        
        dahais_mjai = [act.to_mjai() for act in reach_dahai]
        dahais_json = json.dumps(dahais_mjai)
        expect_json = json.dumps(expect)
        self.assertEqual(dahais_json, expect_json)

    def test_possible_actions_hora_tsumo(self) :
        mjai_log = [{"type":"start_game","names":["shanten","shanten","shanten"]},
                    {"type":"start_kyoku","bakaze":"E","kyoku":1,"honba":0,"kyotaku":0,"oya":0,"dora_marker":"8p","tehais":[["1m","2m","3m","4p","0p","6p","5s","7s","8s","E","E","E","C"],["9m","1p","2p","3s","3s","3s","7s","8s","9s","S","W","P","P"],["1m","1p","4p","6p","7p","1s","2s","4s","4s","7s","7s","S","S"]]},
                    {"type":"tsumo","actor":0,"pai":"C"},
                    {"type":"dahai","actor":0,"pai":"5s" , "tsumogiri" : False},
                    {"type":"tsumo","actor":1,"pai":"1m"},
                    {"type":"dahai","actor":1,"pai":"1m" ,"tsumogiri" : True},
                    {"type":"tsumo","actor":2,"pai":"2m"},
                    {"type":"dahai","actor":2,"pai":"2m" ,"tsumogiri" : True},
                    {"type":"tsumo","actor":0,"pai":"9s"},
                    ]
        game_state = loadGameStateFromMjai(mjai_log)

        pag = PossibleActionGenerator()
        hora_tsumo = pag.possible_actions_hora(game_state)

        expect = [{"type": "hora", "actor": 0, "target": 0, "pai": "9s"}]
        horas_mjai = [act.to_mjai() for act in hora_tsumo]
        horas_json = json.dumps(horas_mjai)
        expect_json = json.dumps(expect)
        self.assertEqual(horas_json, expect_json)

    def test_possible_actions_hora_ron(self) :
        mjai_log = [{"type":"start_game","names":["shanten","shanten","shanten"]},
                    {"type":"start_kyoku","bakaze":"E","kyoku":1,"honba":0,"kyotaku":0,"oya":0,"dora_marker":"8p","tehais":[["1m","2m","3m","4p","0p","6p","2s","2s","4s","E","E","E","N"],["4m","5m","6m","3s","3s","3s","7s","8s","S","S","S","N","N"],["1m","1p","4p","6p","7p","1s","2s","4s","4s","7s","9s","W","W"]]},
                    {"type":"tsumo","actor":0,"pai":"5s"},
                    {"type":"dahai","actor":0,"pai":"N" , "tsumogiri" : False},
                    {"type":"tsumo","actor":1,"pai":"1m"},
                    {"type":"dahai","actor":1,"pai":"1m" ,"tsumogiri" : True},
                    {"type":"tsumo","actor":2,"pai":"6s"},
                    {"type":"dahai","actor":2,"pai":"6s" ,"tsumogiri" : True},
                    ]
        game_state = loadGameStateFromMjai(mjai_log)
        pag = PossibleActionGenerator()
        hora_ron = pag.possible_actions_hora(game_state)
        expect = [{"type": "hora", "actor": 0, "target": 2, "pai": "6s"}, {"type": "hora", "actor": 1, "target": 2, "pai": "6s"}]
        horas_mjai = [act.to_mjai() for act in hora_ron]
        horas_json = json.dumps(horas_mjai)
        expect_json = json.dumps(expect)
        self.assertEqual(horas_json, expect_json)

    def test_possible_action_hora_ron_2(self) :
        mjai_log = [{"type":"start_game","names":["shanten","shanten","shanten"]},
                    {"type":"start_kyoku","bakaze":"E","kyoku":1,"honba":0,"kyotaku":0,"oya":0,"dora_marker":"F","tehais":[["2p","3p","3p","4p","4p","5p","2s","2s","6s","6s","7s","8s","N"],["1m","2p","3p","4p","9p","9p","3s","3s","E","E","S","S","P"],["1m","9m","2p","2p","5p","6p","2s","3s","5sr","5s","7s","8s","9s"]]},
                    {"type":"tsumo","actor":0,"pai":"1p"},
                    {"type":"nukidora","actor":0,"pai":"N"},
                    {"type":"tsumo","actor":0,"pai":"8p"},
                    {"type":"dahai","actor":0,"pai":"1p" , "tsumogiri" : False},
                    {"type":"tsumo","actor":1,"pai":"N"},
                    {"type":"nukidora","actor":1,"pai":"N"},
                    {"type":"tsumo","actor":1,"pai":"1m"},
                    {"type":"dahai","actor":1,"pai":"1m" ,"tsumogiri" : True},
                    {"type":"tsumo","actor":2,"pai":"N"},
                    {"type":"nukidora","actor":2,"pai":"N"},
                    {"type":"tsumo","actor":2,"pai":"2s"},
                    {"type":"dahai","actor":2,"pai":"2s" ,"tsumogiri" : True},
                    {"type":"pon","actor":0,"target":2,"pai":"2s","consumed":["2s","2s"]},
                    {"type":"dahai","actor":0,"pai":"8p" , "tsumogiri" : False},
                    {"type":"tsumo","actor":1,"pai":"1p"},
                    {"type":"dahai","actor":1,"pai":"1p" ,"tsumogiri" : True},
                    {"type":"tsumo","actor":2,"pai":"6s"},
                    {"type":"dahai","actor":2,"pai":"6s" ,"tsumogiri" : True}
                    ]
        game_state = loadGameStateFromMjai(mjai_log)
        pag = PossibleActionGenerator()
        action = pag.possible_game_actions(game_state)
        expect = [{"type": "hora", "actor": 0, "target": 2, "pai": "6s"},{"type": "pon", "actor": 0, "target": 2, "pai": "6s", "consumed": ["6s", "6s"]}]
        horas_mjai = [act.to_mjai() for act in action]
        horas_json = json.dumps(horas_mjai)
        expect_json = json.dumps(expect)
        self.assertEqual(horas_json, expect_json)

    def test_possible_action_hora_furiten(self) :
        mjai_log = [{"type":"start_game","names":["shanten","shanten","shanten"]},
                    {"type":"start_kyoku","bakaze":"E","kyoku":1,"honba":0,"kyotaku":0,"oya":0,"dora_marker":"F","tehais":[["2p","3p","3p","4p","4p","5p","2s","2s","6s","6s","7s","8s","N"],["1m","2p","3p","4p","9p","9p","3s","3s","E","E","S","S","P"],["1m","9m","2p","2p","5p","6p","2s","3s","5sr","5s","7s","8s","9s"]]},
                    {"type":"tsumo","actor":0,"pai":"1p"},
                    {"type":"nukidora","actor":0,"pai":"N"},
                    {"type":"tsumo","actor":0,"pai":"9s"},
                    {"type":"dahai","actor":0,"pai":"1p" , "tsumogiri" : False},
                    {"type":"tsumo","actor":1,"pai":"N"},
                    {"type":"nukidora","actor":1,"pai":"N"},
                    {"type":"tsumo","actor":1,"pai":"1m"},
                    {"type":"dahai","actor":1,"pai":"1m" ,"tsumogiri" : True},
                    {"type":"tsumo","actor":2,"pai":"N"},
                    {"type":"nukidora","actor":2,"pai":"N"},
                    {"type":"tsumo","actor":2,"pai":"2s"},
                    {"type":"dahai","actor":2,"pai":"2s" ,"tsumogiri" : True}, # ロン
                    {"type":"pon","actor":0,"target":2,"pai":"2s","consumed":["2s","2s"]},# ここで69s聴牌
                    {"type":"dahai","actor":0,"pai":"9s" , "tsumogiri" : False}, #フリテン
                    {"type":"tsumo","actor":1,"pai":"1p"},
                    {"type":"dahai","actor":1,"pai":"1p" ,"tsumogiri" : True},
                    {"type":"tsumo","actor":2,"pai":"6s"},
                    {"type":"dahai","actor":2,"pai":"6s" ,"tsumogiri" : True}
        ]
        game_state = loadGameStateFromMjai(mjai_log)
        pag = PossibleActionGenerator()
        action = pag.possible_game_actions(game_state)
        expect = [{"type": "pon", "actor": 0, "target": 2, "pai": "6s", "consumed": ["6s", "6s"]}]
        horas_mjai = [act.to_mjai() for act in action]
        horas_json = json.dumps(horas_mjai)
        expect_json = json.dumps(expect)
        self.assertEqual(horas_json, expect_json)
        
    def test_possible_action_hora_ryanshan(self) :
        mjai_log = [{"type":"start_game","names":["shanten","shanten","shanten"]},
                    {"type":"start_kyoku","bakaze":"E","kyoku":1,"honba":0,"kyotaku":0,"oya":0,"dora_marker":"F","tehais":[["1p","1p","2p","4p","4p","5p","2s","2s","6s","6s","7s","8s","N"],["1m","2p","4p","4p","9p","9p","3s","3s","E","E","S","S","P"],["3p","3p","5p","6p","7p","4s","4s","4s","5s","6s","7s","9s","9s"]]},
                    {"type":"tsumo","actor":0,"pai":"1p"},
                    {"type":"dahai","actor":0,"pai":"1p" , "tsumogiri" : True},
                    {"type":"tsumo","actor":1,"pai":"1m"},
                    {"type":"dahai","actor":1,"pai":"1m" ,"tsumogiri" : True},
                    {"type":"tsumo","actor":2,"pai":"N"},
                    {"type":"nukidora","actor":2,"pai":"N"},
                    {"type":"tsumo","actor":2,"pai":"4s"},
                    {"type":"ankan","actor":2,"consumed":["4s","4s","4s","4s"]},
                    {"type":"tsumo","actor":2,"pai":"3p"}
        ]
        game_state = loadGameStateFromMjai(mjai_log)
        pag = PossibleActionGenerator()
        action = pag.possible_game_actions(game_state)
        # expect = [{"type": "pon", "actor": 0, "target": 2, "pai": "6s", "consumed": ["6s", "6s"]}]
        # horas_mjai = [act.to_mjai() for act in action]
        # horas_json = json.dumps(horas_mjai)
        # expect_json = json.dumps(expect)
        # self.assertEqual(horas_json, expect_json)
