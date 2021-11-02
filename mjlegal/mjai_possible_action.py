from .possible_action import PossibleActionGenerator

class MjaiPossibleActionGenerator :
    
    def __init__(self) :
        self.possibleAction = PossibleActionGenerator()
        self.name = "mjlegal"

    def possible_mjai_action(self, game_state, previous_mjai_action) :
        possible_actions = []
        action_type = previous_mjai_action['type']
        if action_type == "hello" :
            join_action = {"type" : "join", "name" : self.name, "room" : "default"}
            possible_actions.append(join_action)
        elif action_type in ("start_game", "start_kyoku", "reach_accepted", "hora", "ryukyoku", "end_kyoku") :
            none_action = {"type" : "none"}
            possible_actions.append(none_action)
        elif "actor" in previous_mjai_action :
            actor = previous_mjai_action["actor"]
            if actor != game_state.player_id :
                none_action = {"type" : "none"}
                possible_actions.append(none_action)
            possible_game_actions = self.possibleAction.possible_game_actions(game_state)
            possible_actions += possible_game_actions
        else :
            pass

        return possible_actions
        