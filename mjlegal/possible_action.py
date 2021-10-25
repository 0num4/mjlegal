import copy

from mahjong.shanten import Shanten
from mahjong.agari import Agari
from mahjong.hand_calculating.hand import HandCalculator
from mahjong.hand_calculating.hand_config import HandConfig, OptionalRules
from mahjong.constants import EAST, SOUTH, WEST, NORTH

from .game_state import GameState
from .player_state import PlayerState
from .mjtypes import Tile, Meld, TilesUtil
from .mjtypes import ActionType
from .action import Action

class PossibleActionGenerator :
    WINDS = {"E": EAST, "S" : SOUTH, "W" : WEST, "N" : NORTH}
    def __init__(self) :
        self.shanten = Shanten()
        self.agari  = Agari()
        self.hand = HandCalculator()

    def player_action_candidate(self, game_state : GameState) :
        candidate = []
        previous_action = game_state.previous_action
        
        if previous_action is None  :
            tsumo = Action(ActionType.TSUMO, game_state.oya)
            candidate.append(tsumo)
        else :
            prev_type  = previous_action.type
            prev_actor = previous_action.actor
            if prev_type in (ActionType.TSUMO, ActionType.PON, ActionType.CHI) :
                dahai = Action(ActionType.DAHAI, prev_actor)
                candidate.append(dahai)
            elif prev_type in (ActionType.ANKAN, ActionType.KAKAN, ActionType.DAIMINKAN, ActionType.NUKI) :
                tsumo = Action(ActionType.TSUMO, prev_actor)
                candidate.append(tsumo)
            elif prev_type == ActionType.DAHAI :
                other_player_ids = filter(lambda id : id != prev_actor, range(0, game_state.num_players))
                for id in other_player_ids :
                    meld_actions = [Action(action, id) for action in (ActionType.PON, ActionType.CHI, ActionType.DAIMINKAN, ActionType.HORA)]
                    candidate += meld_actions
                
                next_player_id = (prev_actor + 1) % game_state.num_players
                tsumo = Action(ActionType.TSUMO, next_player_id)
                candidate.append(tsumo)

            if prev_type in (ActionType.ANKAN, ActionType.KAKAN, ActionType.NUKI) :
                other_player_ids = filter(lambda id : id != prev_actor, range(0, game_state.num_players))
                for id in other_player_ids :
                    hora = Action(ActionType.HORA, id)
                    candidate.append(hora)

        return candidate

    def possible_game_actions(self, game_state) :
        pass
        
    def possible_action_dahai(self, game_state) :
        actions = []
        previous_action = game_state.previous_action
        if previous_action is not None  :
            prev_type  = previous_action.type
            if prev_type in (ActionType.TSUMO, ActionType.PON, ActionType.CHI) :
                prev_actor = previous_action.actor
                prev_actor_state = game_state.player_states[prev_actor]
                dahais = prev_actor_state.tiles
                if prev_type == ActionType.PON :
                    prev_pon = prev_actor_state.melds[-1]
                    dahais = [tile for tile in dahais if not(Tile.equal(tile, prev_pon.tiles[0], True))]
                elif prev_type == ActionType.CHI :
                    pass # TODO チーの喰い変え動作
                actions = [Action(type = ActionType.DAHAI, actor = prev_actor, tile = tile) for tile in dahais]
                if prev_actor_state.tsumo_tile :
                    tsumogiri_action = Action(type = ActionType.DAHAI, actor = prev_actor, 
                                        tile = prev_actor_state.tsumo_tile, tsumogiri = True)
                    actions.append(tsumogiri_action)
        #TODO 重複アクション削除
        return actions

    def possible_actions_pon(self, game_state):
        actions = []
        previous_action = game_state.previous_action
        if previous_action is not None  :
            prev_type  = previous_action.type
            prev_actor = previous_action.actor
            if prev_type == ActionType.DAHAI :
                prev_dahai = previous_action.tile
                other_player_ids = filter(lambda id : id != prev_actor, range(0, game_state.num_players))
                for id in other_player_ids :
                    player_state = game_state.player_states[id]
                    tiles = player_state.tiles
                    consumed_list = []
                    consumed_tiles = [tile for tile in tiles if tile.equal(prev_dahai, tile, True)]
                    num_consumed = len(consumed_tiles)
                    if num_consumed == 3 :
                        # 手牌に赤ドラを含む場合、2通りのconsumedができる(赤含む、含まない)
                        exclude_aka = [tile for tile in consumed_tiles if not tile.is_aka]
                        if len(exclude_aka) == 3 :
                            consumed_list.append(consumed_tiles[0:2])
                        else :
                            consumed_list.append(exclude_aka)
                            consumed_tiles.remove(prev_dahai)
                            consumed_list.append(consumed_tiles)
                    elif num_consumed == 2 :
                        consumed_list.append(consumed_tiles)
                    
                    for consumed in consumed_list :
                        pon_action = Action(type = ActionType.PON, 
                                        actor = id,
                                        target = prev_actor,
                                        consumed = consumed,
                                        tile = prev_dahai
                                        )
                        actions.append(pon_action)
        return actions

    def possible_actions_ankan(self, game_state):
        actions = []
        previous_action = game_state.previous_action
        if previous_action is not None  :
            prev_type  = previous_action.type
            if prev_type == ActionType.TSUMO :
                prev_actor = previous_action.actor
                prev_actor_state = game_state.player_states[prev_actor]
                tiles = prev_actor_state.tehai
                tiles34 = TilesUtil.tiles_to_tiles34(tiles)
                ankan_tiles = [Tile.from_tile34_index(i) for i, count in enumerate(tiles34) if count == 4]
                for ankan_t in ankan_tiles :
                    consumed = [tile for tile in tiles if Tile.equal(tile, ankan_t, True)]
                    kan_action = Action(type = ActionType.ANKAN, 
                                        actor = prev_actor,
                                        consumed = consumed)
                    actions.append(kan_action)
        return actions

    def possible_actions_kakan(self, game_state):
        actions = []
        previous_action = game_state.previous_action
        if previous_action is not None  :
            prev_type  = previous_action.type
            if prev_type == ActionType.TSUMO :
                prev_actor = previous_action.actor
                prev_actor_state = game_state.player_states[prev_actor]
                tiles = prev_actor_state.tehai
                melds = prev_actor_state.melds
                for meld in melds :
                    if meld.type == Meld.PON :
                        kakan_tiles = [tile for tile in tiles if Tile.equal(meld.tiles[0], tile, True)]
                        if len(kakan_tiles) > 0 :
                            kan_action = Action(type = ActionType.KAKAN, actor = prev_actor, tile=kakan_tiles[0], consumed = meld.tiles)
                            actions.append(kan_action)
        return actions

    def possible_actions_daiminkan(self, game_state):
        actions = []
        previous_action = game_state.previous_action
        if previous_action is not None  :
            prev_type  = previous_action.type
            prev_actor = previous_action.actor
            if prev_type == ActionType.DAHAI :
                prev_dahai = previous_action.tile
                other_player_ids = filter(lambda id : id != prev_actor, range(0, game_state.num_players))
                for id in other_player_ids :
                    player_state = game_state.player_states[id]
                    tiles = player_state.tiles
                    consumed_tiles = [tile for tile in tiles if tile.equal(prev_dahai, tile, True)]
                    num_consumed = len(consumed_tiles)
                    if num_consumed == 3 :
                        kan_action = Action(type = ActionType.DAIMINKAN, 
                                        actor = id,
                                        target = prev_actor,
                                        consumed = consumed_tiles,
                                        tile = prev_dahai
                                        )
                        actions.append(kan_action)
        return actions

    def possible_actions_nukidora(self, game_state):
        actions = []
        previous_action = game_state.previous_action
        if previous_action is not None  :
            prev_type  = previous_action.type
            if prev_type in (ActionType.TSUMO) :
                prev_actor = previous_action.actor
                prev_actor_state = game_state.player_states[prev_actor]
                tiles = prev_actor_state.tehai
                nukidora_pai = Tile.from_str("N")
                nukidora = next((tile for tile in tiles if tile == nukidora_pai), None)
                if nukidora :
                    actions.append(Action(type = ActionType.NUKI, actor = prev_actor, tile = nukidora))
        return actions

    def possible_actions_dahai_after_reach(self, game_state):
        actions = []
        previous_action = game_state.previous_action
        if previous_action is not None  :
            prev_type  = previous_action.type
            if prev_type == ActionType.TSUMO :
                prev_actor = previous_action.actor
                prev_actor_state = game_state.player_states[prev_actor]
                if not(prev_actor_state.is_reach) and prev_actor_state.is_menzen and prev_actor_state.score >= 1000:
                    tiles = prev_actor_state.tehai
                    tiles34 = TilesUtil.tiles_to_tiles34(tiles)
                    tenpai_tiles_34 = self.get_tenpai_tile(tiles34)
                    if sum(tenpai_tiles_34) > 0 :
                        tenpai_dahais = TilesUtil.find_tiles_34_in_tiles(tiles, tenpai_tiles_34)
                        for dahai in tenpai_dahais :
                            reach_dahai_action = Action(type = ActionType.DAHAI, actor = prev_actor, 
                                        tile = dahai, tsumogiri = (prev_actor_state.tsumo_tile == dahai))
                            actions.append(reach_dahai_action)
        return actions

    def possible_actions_hora(self, game_state):
        actions = []
        previous_action = game_state.previous_action
        if previous_action is not None  :
            is_tsumo=True
            is_rinshan = False
            prev_type  = previous_action.type
            actors = []
            if prev_type == ActionType.TSUMO :
                player_id = previous_action.actor
                actors.append(player_id)
                target = player_id
                is_rinshan = previous_action.rinshan
            elif prev_type in (ActionType.DAHAI, ActionType.ANKAN, ActionType.KAKAN, ActionType.NUKI) :
                is_tsumo=False
                prev_actor = previous_action.actor
                target = prev_actor
                actors = filter(lambda id : id != prev_actor, range(0, game_state.num_players))
                
            for actor in actors :
                player_state = game_state.player_states[actor]
                is_riichi= player_state.is_reach
                player_wind = game_state.player_wind(actor)
                hand_config = self.make_hand_config(is_tsumo   = is_tsumo,
                                                    is_riichi  = is_riichi,
                                                    is_ippatsu = False,
                                                    is_rinshan = is_rinshan,
                                                    is_chankan = False,
                                                    is_haitei  = False,
                                                    is_houtei  = False,
                                                    is_daburu_riichi = False,
                                                    is_nagashi_mangan = False,
                                                    is_tenhou = False,
                                                    is_renhou = False,
                                                    is_chiihou = False,
                                                    player_wind = PossibleActionGenerator.WINDS[player_wind],
                                                    round_wind = PossibleActionGenerator.WINDS[game_state.bakaze])

                if self._can_hora(game_state, player_state, previous_action.tile, hand_config) :
                    hora_action = Action(type = ActionType.HORA, 
                                actor = actor, target = target, 
                                tile = previous_action.tile)
                    actions.append(hora_action)
        return actions

    def _can_hora(self, game_state, player_state, win_tile, hand_config) :
        tiles = player_state.tiles
        tehai = tiles + [win_tile]
        tiles34 = TilesUtil.tiles_to_tiles34(tehai)
        is_agari = False
        if self.agari.is_agari(tiles34) :
            tiles136 = TilesUtil.tiles_to_tiles136(tiles)
            tehai136 = TilesUtil.tiles_to_tiles136(tehai)
            melds136 = player_state.melds136 if len(player_state.melds) > 0 else None
            win_tile136_list = list(set(tehai136) - set(tiles136))
            dora_ind = TilesUtil.tiles_to_tiles136(game_state.dora_markers)
            hand_value = self.hand.estimate_hand_value(tiles = tehai136, win_tile = win_tile136_list[0],
                                            melds = melds136, dora_indicators = dora_ind, config = hand_config)
            # print(hand_value.cost)
            is_agari = hand_value.cost is not None
        return is_agari

    def get_machi(self, tiles_34) :
        tile_count = sum(tiles_34)
        assert tile_count < 14 and tile_count % 2 == 1

        machi_tiles_34 = [0] * 34
        for i in range(0,34) :
            temp_tiles = copy.copy(tiles_34)
            if temp_tiles[i] < 4 :
                temp_tiles[i] += 1
                if self.agari.is_agari(temp_tiles) :
                    machi_tiles_34[i] = 1
        return machi_tiles_34

    def get_tenpai_tile(self, tiles_34) :
        tenpai_tiles_34 = [0] * 34
        for i in range(0,34) :
            temp_tiles = copy.copy(tiles_34)
            if temp_tiles[i] > 0 :
                temp_tiles[i] -= 1
                machi_tiles_34 = self.get_machi(temp_tiles)
                if sum(machi_tiles_34) > 0 :
                    tenpai_tiles_34[i] = 1
        return tenpai_tiles_34

    def make_hand_config(self,
        is_tsumo=False,
        is_riichi=False,
        is_ippatsu=False,
        is_rinshan=False,
        is_chankan=False,
        is_haitei=False,
        is_houtei=False,
        is_daburu_riichi=False,
        is_nagashi_mangan=False,
        is_tenhou=False,
        is_renhou=False,
        is_chiihou=False,
        player_wind=None,
        round_wind=None,
    ):
        options = OptionalRules(
            has_open_tanyao=True,
            has_aka_dora=True,
            has_double_yakuman=True,
            renhou_as_yakuman=False,
            has_daisharin=False,
            has_daisharin_other_suits=False,
            # has_daichisei=False,
            # has_sashikomi_yakuman=False,
            # limit_to_sextuple_yakuman=True,
            # paarenchan_needs_yaku=False,
        )
        return HandConfig(
            is_tsumo=is_tsumo,
            is_riichi=is_riichi,
            is_ippatsu=is_ippatsu,
            is_rinshan=is_rinshan,
            is_chankan=is_chankan,
            is_haitei=is_haitei,
            is_houtei=is_houtei,
            is_daburu_riichi=is_daburu_riichi,
            is_nagashi_mangan=is_nagashi_mangan,
            is_tenhou=is_tenhou,
            is_renhou=is_renhou,
            is_chiihou=is_chiihou,
            player_wind=player_wind,
            round_wind=round_wind,
            # is_open_riichi=False,
            # paarenchan=0,
            options=options,
        )
