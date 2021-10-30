import unittest
import json

from mjlegal.mjai import MjaiLoader
from mjlegal.mjai_player_loader import MjaiPlayerLoader

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
    for record in records :
        mjl.action(record)
        # print(record)
        # for i, ps in enumerate(mjl.game.player_states) :
        #     print(i, ps.dump())

def load_mjai_player_records(filename) :
    records = []
    log_input_file = open(filename, 'r', encoding="utf-8")
    for line in log_input_file :
        tokens = line.split('\t')
        direction_str = tokens[0]
        mjai_str = tokens[1]
        mjai_ev = json.loads(mjai_str)
        record = {'direction' : DIRECT_DICT[direction_str], 'record' : mjai_ev}
        records.append(record)
    log_input_file.close()
    return records

class TestMjaiLoader(unittest.TestCase) :
    def test_mjai_load_0(self) :
        test_mjai_load("./tests/test_data/test_mjson_0.mjson")

    def test_mjai_load_1(self) :
        test_mjai_load("./tests/test_data/test_mjson_1.mjson")

    def test_player_mjai_log_load_0(self) :
        records = load_mjai_player_records('./tests/test_data/test_mjai_player_log_01.txt')
        mjaiPlayerLoader = MjaiPlayerLoader()
        for record in records :
            direction = record['direction']
            ev = record['record']
            if direction == SERVER_TO_CLIENT :
                mjaiPlayerLoader.action_receive(ev)
            elif direction == CLIENT_TO_SERVER :
                mjaiPlayerLoader.action_send(ev)
            else :
                self.fail('Invalid mjai player record..')

