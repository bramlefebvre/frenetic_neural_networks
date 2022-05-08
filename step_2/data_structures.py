class Dynamics:
    def __init__(self, rate_matrix, basins):
        self.rate_matrix = rate_matrix
        self.basins = basins

class Basins:
    def __init__(self, basins):
        self.basins = basins
    
    def get_basin_for_state(self, state):
        for basin in self.basins:
            if state in basin.states:
                return basin

class Basin:
    def __init__(self, index, pattern_states, states):
        self.index = index
        self.pattern_states = pattern_states
        self.states = states

