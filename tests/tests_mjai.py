import unittest
import json

from mjlegal.mjai import MjaiLoader

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

class TestMjaiLoader(unittest.TestCase) :
    def test_mjai_load_0(self) :
        test_mjai_load("./tests/test_data/test_mjson_0.mjson")

    def test_mjai_load_1(self) :
        test_mjai_load("./tests/test_data/test_mjson_1.mjson")

