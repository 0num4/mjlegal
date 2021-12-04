import unittest
import json

from mjlegal.mjai import MjaiLoader
from mjlegal.possible_action import PossibleActionGenerator
from mjlegal.mjai_possible_action import MjaiPossibleActionGenerator

TEST_DATA_DIR_PATH = "./tests/test_data/"

def load_mjai_records(filename) :
    records = []
    log_input_file = open(filename, 'r', encoding="utf-8")
    for line in log_input_file :
        mjai_ev = json.loads(line)
        records.append(mjai_ev)
    log_input_file.close()
    return records

def load_mjai_player_records(filename) :
    records = []
    log_input_file = open(filename, 'r', encoding="utf-8")
    for line in log_input_file :
        tokens = line.split('\t')
        records.append(tokens)
    log_input_file.close()
    return records

def load_expect_actions(filename) :
    with open(filename, mode ='r', encoding = 'utf-8') as file :
        expect_str = file.read()
    return json.loads(expect_str)

def save_expect_actions(filename, possible_actions) :
    output = json.dumps(possible_actions)
    with open(filename, mode = 'w', encoding = 'utf-8') as file :
        file.write(output)

def test_generate_expected(log_filename, expect_filename) :
    records = load_mjai_records(log_filename)
    mjl = MjaiLoader()
    possibleActionGenerator = PossibleActionGenerator()
    possible_actions = []
    for record in records :
        mjl.action(record)
        possible_action = possibleActionGenerator.possible_game_actions(mjl.game)
        mjson_list = [action.to_mjai_json() for action in possible_action]
        possible_actions.append(mjson_list)
    save_expect_actions(expect_filename, possible_actions)

def test_mjai(mjson_filename, expect_filename) :
    mjl = MjaiLoader()
    possibleActionGenerator = PossibleActionGenerator()
    records = load_mjai_records(mjson_filename)
    expect_actions = load_expect_actions(expect_filename)
    for record, expect in zip(records, expect_actions) :
        mjl.action(record)
        possible_action = possibleActionGenerator.possible_game_actions(mjl.game)
        mjson_list = [action.to_mjai_json() for action in possible_action]
        assert json.dumps(expect) == json.dumps(mjson_list)

def test_generate_mjai_player(player_id, mjson_filename, expect_filename) :
    mjl = MjaiLoader()
    mjaiPossibleActionGenerator = MjaiPossibleActionGenerator()
    records = load_mjai_records(mjson_filename)
    possible_actions = []
    for record in records :
        mjl.action(record)
        if record["type"] == "start_kyoku" :
            mjl.game.player_id = player_id
        possible_action = mjaiPossibleActionGenerator.possible_mjai_action(mjl.game)
        possible_actions.append(possible_action)
    save_expect_actions(expect_filename, possible_actions)

def test_mjai_player(player_id, mjson_filename, expect_filename) :
    mjl = MjaiLoader()
    mjaiPossibleActionGenerator = MjaiPossibleActionGenerator()
    records = load_mjai_records(mjson_filename)
    expect_actions = load_expect_actions(expect_filename)

    for record, expect in zip(records, expect_actions) :
        mjl.action(record)
        if record["type"] == "start_kyoku" :
            mjl.game.player_id = player_id
        possible_action = mjaiPossibleActionGenerator.possible_mjai_action(mjl.game)
        assert json.dumps(expect) == json.dumps(possible_action)

class TestRegression(unittest.TestCase) :
    def test_mjai_0(self) :
        test_mjai(TEST_DATA_DIR_PATH + "test_mjson_0.mjson", TEST_DATA_DIR_PATH + "test_expect_0.mjson")

    def test_mjai_1(self) :
        test_mjai(TEST_DATA_DIR_PATH + "test_mjson_1.mjson", TEST_DATA_DIR_PATH + "test_expect_1.mjson")

    def test_mjai_2(self) :
        test_mjai(TEST_DATA_DIR_PATH + "test_mjson_2.mjson", TEST_DATA_DIR_PATH + "test_expect_2.mjson")
        
    def test_mjai_3(self) :
        test_mjai(TEST_DATA_DIR_PATH + "test_mjson_3.mjson", TEST_DATA_DIR_PATH + "test_expect_3.mjson")
    
    def test_mjai_0_player_0(self) :
        test_mjai_player(0, TEST_DATA_DIR_PATH + "test_mjson_0.mjson", TEST_DATA_DIR_PATH + "test_expect_0_player_0.mjson")
    def test_mjai_0_player_1(self) :
        test_mjai_player(1, TEST_DATA_DIR_PATH + "test_mjson_0.mjson", TEST_DATA_DIR_PATH + "test_expect_0_player_1.mjson")
    def test_mjai_0_player_2(self) :
        test_mjai_player(2, TEST_DATA_DIR_PATH + "test_mjson_0.mjson", TEST_DATA_DIR_PATH + "test_expect_0_player_2.mjson")

    def test_mjai_1_player_0(self) :
        test_mjai_player(0, TEST_DATA_DIR_PATH + "test_mjson_1.mjson", TEST_DATA_DIR_PATH + "test_expect_1_player_0.mjson")
    def test_mjai_1_player_1(self) :
        test_mjai_player(1, TEST_DATA_DIR_PATH + "test_mjson_1.mjson", TEST_DATA_DIR_PATH + "test_expect_1_player_1.mjson")
    def test_mjai_1_player_2(self) :
        test_mjai_player(2, TEST_DATA_DIR_PATH + "test_mjson_1.mjson", TEST_DATA_DIR_PATH + "test_expect_1_player_2.mjson")

    def test_mjai_2_player_0(self) :
        test_mjai_player(0, TEST_DATA_DIR_PATH + "test_mjson_2.mjson", TEST_DATA_DIR_PATH + "test_expect_2_player_0.mjson")
    def test_mjai_2_player_1(self) :
        test_mjai_player(1, TEST_DATA_DIR_PATH + "test_mjson_2.mjson", TEST_DATA_DIR_PATH + "test_expect_2_player_1.mjson")
    def test_mjai_2_player_2(self) :
        test_mjai_player(2, TEST_DATA_DIR_PATH + "test_mjson_2.mjson", TEST_DATA_DIR_PATH + "test_expect_2_player_2.mjson")

    def test_mjai_3_player_0(self) :
        test_mjai_player(0, TEST_DATA_DIR_PATH + "test_mjson_3.mjson", TEST_DATA_DIR_PATH + "test_expect_3_player_0.mjson")
    def test_mjai_3_player_1(self) :
        test_mjai_player(1, TEST_DATA_DIR_PATH + "test_mjson_3.mjson", TEST_DATA_DIR_PATH + "test_expect_3_player_1.mjson")
    def test_mjai_3_player_2(self) :
        test_mjai_player(2, TEST_DATA_DIR_PATH + "test_mjson_3.mjson", TEST_DATA_DIR_PATH + "test_expect_3_player_2.mjson")


if __name__ == '__main__':
    test_generate_expected(TEST_DATA_DIR_PATH + "test_mjson_0.mjson", TEST_DATA_DIR_PATH + "expect/test_expect_0.mjson")
    test_generate_expected(TEST_DATA_DIR_PATH + "test_mjson_1.mjson", TEST_DATA_DIR_PATH + "expect/test_expect_1.mjson")
    test_generate_expected(TEST_DATA_DIR_PATH + "test_mjson_2.mjson", TEST_DATA_DIR_PATH + "expect/test_expect_2.mjson")
    test_generate_expected(TEST_DATA_DIR_PATH + "test_mjson_3.mjson", TEST_DATA_DIR_PATH + "expect/test_expect_3.mjson")

    test_generate_mjai_player(0, TEST_DATA_DIR_PATH + "test_mjson_0.mjson", TEST_DATA_DIR_PATH + "expect/test_expect_0_player_0.mjson")
    test_generate_mjai_player(1, TEST_DATA_DIR_PATH + "test_mjson_0.mjson", TEST_DATA_DIR_PATH + "expect/test_expect_0_player_1.mjson")
    test_generate_mjai_player(2, TEST_DATA_DIR_PATH + "test_mjson_0.mjson", TEST_DATA_DIR_PATH + "expect/test_expect_0_player_2.mjson")
    
    test_generate_mjai_player(0, TEST_DATA_DIR_PATH + "test_mjson_1.mjson", TEST_DATA_DIR_PATH + "expect/test_expect_1_player_0.mjson")
    test_generate_mjai_player(1, TEST_DATA_DIR_PATH + "test_mjson_1.mjson", TEST_DATA_DIR_PATH + "expect/test_expect_1_player_1.mjson")
    test_generate_mjai_player(2, TEST_DATA_DIR_PATH + "test_mjson_1.mjson", TEST_DATA_DIR_PATH + "expect/test_expect_1_player_2.mjson")
    
    test_generate_mjai_player(0, TEST_DATA_DIR_PATH + "test_mjson_2.mjson", TEST_DATA_DIR_PATH + "expect/test_expect_2_player_0.mjson")
    test_generate_mjai_player(1, TEST_DATA_DIR_PATH + "test_mjson_2.mjson", TEST_DATA_DIR_PATH + "expect/test_expect_2_player_1.mjson")
    test_generate_mjai_player(2, TEST_DATA_DIR_PATH + "test_mjson_2.mjson", TEST_DATA_DIR_PATH + "expect/test_expect_2_player_2.mjson")
    
    test_generate_mjai_player(0, TEST_DATA_DIR_PATH + "test_mjson_3.mjson", TEST_DATA_DIR_PATH + "expect/test_expect_3_player_0.mjson")
    test_generate_mjai_player(1, TEST_DATA_DIR_PATH + "test_mjson_3.mjson", TEST_DATA_DIR_PATH + "expect/test_expect_3_player_1.mjson")
    test_generate_mjai_player(2, TEST_DATA_DIR_PATH + "test_mjson_3.mjson", TEST_DATA_DIR_PATH + "expect/test_expect_3_player_2.mjson")
    
