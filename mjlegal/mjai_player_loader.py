from .game_state import GameState
from .player_state import PlayerState
from .mjtypes import TilesUtil, Tile
from .mjtypes import ActionType
from .action import Action

class MjaiPlayerLoader :
    def __init__(self) :
        self.game = None
        self.reach_dahai = False # 次の打牌が立直宣言牌
    
    def action_receive(self, action) :
        pass
    def action_send(self, action) :
        pass

    def action(self, action) :
        action_type = action["type"]
        if action_type == "start_game" :
            self.game = GameState()
        elif action_type == "start_kyoku" :
            self.game.start_kyoku()
            self.game.bakaze = action["bakaze"]
            self.game.kyoku = action["kyoku"]
            self.game.oya = action["oya"]
            self.game.dora_markers.append(Tile.from_str(action["dora_marker"]))

            self.game.player_states = []
            for id, tehai in enumerate(action["tehais"]) :
                player_state = PlayerState()
                player_state.player_id = id
                player_state.tiles = TilesUtil.tiles_str_array_to_tiles(tehai)
                self.game.player_states.append(player_state)
            
        elif "actor" in action :
            action_actor = action["actor"]
            player_state = self.game.player_states[action_actor]
            
            if action_type == "tsumo" :
                pai = action["pai"]
                tile = Tile.from_str(pai)
                self.game.previous_action = player_state.tsumo(pai)
                # self.game.previous_action = Action(type = ActionType.TSUMO, actor = action_actor, tile=tile)
            elif action_type == "dahai" :
                pai = action["pai"]
                tile = Tile.from_str(pai)
                self.game.previous_action = player_state.dahai(pai, self.reach_dahai)
                # self.game.previous_action = Action(type = ActionType.DAHAI, actor = action_actor, tile=tile)
                self.reach_dahai = False
            elif action_type == "pon" :
                pai = action["pai"]
                target = action["target"]
                consumed = action["consumed"]
                tile = Tile.from_str(pai)
                consumed_tiles = TilesUtil.str_to_tiles(consumed)
                self.game.previous_player.pop_ho()
                self.game.previous_action = player_state.pon(pai, consumed, target)
                # self.game.previous_action = Action(type = ActionType.PON, actor = action_actor, tile=tile, target = target, consumed = consumed_tiles)
            elif action_type == "chi" :
                pai = action["pai"]
                target = action["target"]
                consumed = action["consumed"]
                tile = Tile.from_str(pai)
                consumed_tiles = TilesUtil.str_to_tiles(consumed)
                self.game.previous_player.pop_ho()
                self.game.previous_action = player_state.chi(pai, consumed, target)
                # self.game.previous_action = Action(type = ActionType.CHI, actor = action_actor, tile=tile, target = target, consumed = consumed_tiles)
            elif action_type == "kakan" :
                pai = action["pai"]
                tile = Tile.from_str(pai)
                player_state.kakan(pai)
                self.game.previous_action = Action(type = ActionType.KAKAN, actor = action_actor, tile=tile)
            elif action_type == "ankan" :
                consumed = action["consumed"]
                consumed_tiles = TilesUtil.str_to_tiles(consumed)
                self.game.previous_action = player_state.ankan(consumed)
                # self.game.previous_action = Action(type = ActionType.ANKAN, actor = action_actor)
            elif action_type == "daiminkan" :
                pai = action["pai"]
                target = action["target"]
                consumed = action["consumed"]
                tile = Tile.from_str(pai)
                consumed_tiles = TilesUtil.str_to_tiles(consumed)
                self.game.previous_player.pop_ho()
                self.game.previous_action = player_state.daiminkan(pai, consumed, target)
                # self.game.previous_action = Action(type = ActionType.DAIMINKAN, actor = action_actor, tile=tile, target = target, consumed = consumed_tiles)
            elif action_type == "nukidora" :
                pai = action["pai"]
                tile = Tile.from_str(pai)
                self.game.previous_action = player_state.nukidora(pai)
                # self.game.previous_action = self.game.previous_action = Action(type = ActionType.NUKI, actor = action_actor, tile=tile)

            elif action_type == "reach" :
                self.reach_dahai = True
