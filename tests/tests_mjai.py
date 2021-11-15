import unittest
import json

from mjlegal.mjai import MjaiLoader
from mjlegal.mjai_player_loader import MjaiPlayerLoader
from mjlegal.possible_action import PossibleActionGenerator
from mjlegal.mjai_possible_action import MjaiPossibleActionGenerator

SERVER_TO_CLIENT = 0
CLIENT_TO_SERVER = 1
DIRECT_DICT = {'<-' : SERVER_TO_CLIENT, '->' : CLIENT_TO_SERVER}

def load_mjai_records(filename) :
    records = []
    log_input_file = open(filename, 'r', encoding="utf-8")
    for line in log_input_file :
        mjai_ev = json.loads(line)
        records.append(mjai_ev)
    log_input_file.close()
    return records

def test_mjai_load(log_filename) :
    records = load_mjai_records(log_filename)
    mjl = MjaiLoader()
    possibleActionGenerator = PossibleActionGenerator()
    for i in range(0, len(records) - 1) :
        record = records[i]
        next_record = records[i + 1]
        mjl.action(record)
 
        # for debug
        # print(record)
        # for player_state in mjl.game.player_states :
        #     print(player_state.dump())
 
        possible_actions = possibleActionGenerator.possible_game_actions(mjl.game)
        if(next_record['type'] in ("dahai", "pon", "ankan", "daiminkan", "kakan", "nukidora")) :
            possible_record = [action for action in possible_actions 
                if action.to_mjai()['type'] == next_record['type'] and action.to_mjai()['actor'] == next_record['actor']]
            assert len(possible_record) > 0 
            

def load_mjai_player_records(filename) :
    records = []
    log_input_file = open(filename, 'r', encoding="utf-8")
    for line in log_input_file :
        tokens = line.split('\t')
        direction_str = tokens[0]
        if direction_str in DIRECT_DICT :
            mjai_str = tokens[1]
            mjai_ev = json.loads(mjai_str)
            record = {'direction' : DIRECT_DICT[direction_str], 'record' : mjai_ev}
            records.append(record)
    log_input_file.close()
    return records

def equal_mjai_action(action1, action2) :
    return all(action1[key] == action2[key] for key in action1)

def test_mjai_player_records(filename) :
    records = load_mjai_player_records(filename)
    mjaiPlayerLoader = MjaiPlayerLoader()
    mjaiPossibleActionGenerator = MjaiPossibleActionGenerator()
    mjaiPossibleActionGenerator.name = 'Manue1'
    possible_actions = None
    previous_receive_action = None
    for record in records :
        direction = record['direction']
        ev = record['record']
        if direction == SERVER_TO_CLIENT :
            previous_receive_action = ev
            mjaiPlayerLoader.action_receive(previous_receive_action)
            possible_actions = mjaiPossibleActionGenerator.possible_mjai_action(mjaiPlayerLoader.game, previous_receive_action)
        elif direction == CLIENT_TO_SERVER :
            mjaiPlayerLoader.action_send(ev)
            is_legal = any(equal_mjai_action(possible, ev) for possible in possible_actions)
            if not is_legal :
                print("previous receive:", previous_receive_action)
                print("illegal_action:", ev)
                print("possible_action:", possible_actions)
                print("player_states:",mjaiPlayerLoader.game.player_states[mjaiPlayerLoader.game.player_id].dump())
        else :
            self.fail('Invalid mjai player record..')

class TestMjaiLoader(unittest.TestCase) :
    def test_mjai_load_0(self) :
        test_mjai_load("./tests/test_data/test_mjson_0.mjson")

    def test_mjai_load_1(self) :
        test_mjai_load("./tests/test_data/test_mjson_1.mjson")

    def test_mjai_load_2(self) :
        test_mjai_load("./tests/test_data/test_mjson_2.mjson")

    def test_mjai_load_3(self) :
        test_mjai_load("./tests/test_data/test_mjson_3.mjson")

    def test_player_mjai_log_load_0(self) :
        test_mjai_player_records('./tests/test_data/test_mjai_player_log_01.txt')

    def test_player_mjai_log_load_1(self) :
        test_mjai_player_records('./tests/test_data/test_mjai_player_log_02.txt')

