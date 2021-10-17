
class GameState :
    
    def __init__(self) :
        self.reset()
        self.start_kyoku()

    def reset(self) :
        self.bakaze = 0
        self.kyoku = 0
        self.honba = 0
        self.chicha = 0 # 常に0
        self.num_initial_pipais = 0
        self.player_states = []

    def start_kyoku(self) :
        self.oya = 0
        self.num_pipais = 0
        self.dora_markers = []
        self.previous_action = None

    @property
    def num_players(self) :
        return len(self.player_states)

    @property
    def scores(self) :
        return [player_state.score for player_state in self.player_states]
    
    @scores.setter
    def scores(self, scores) :
        self.set_scores(scores)

    def set_scores(self, scores) :
        assert len(scores) == len(self.player_states)
        for i, score in enumerate(scores) :
            self.player_states[i] = score

    def set_delta_scores(self, delta_scores) :
        assert len(delta_scores) == len(self.player_states)
        for i, delta_score in enumerate(delta_scores) :
            self.player_states[i] += delta_score

    @property
    def previous_player(self) :
        if self.previous_action :
            previous_player_id = self.previous_action.actor
            return self.player_states[previous_player_id]

    
