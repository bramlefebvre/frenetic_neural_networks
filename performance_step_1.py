import math
from step_1.find_exuberant_system import find_exuberant_system
import daos.tournaments_and_patterns_dao as tournaments_and_patterns_dao
import time

tournament_and_patterns = tournaments_and_patterns_dao.get_single_tournament_and_patterns('1000_50_0', 'data/step_1/tournament_1000_50')
start_time = time.time_ns()
find_exuberant_system(tournament_and_patterns)
end_time = time.time_ns()
elapsed_time_in_micro_seconds = (end_time - start_time) / (10 ** 3)
print('elapsed time in microseconds:')
print(elapsed_time_in_micro_seconds)

def generate_number_of_patterns_list(number_of_states):
    maximum_number_of_patterns = math.floor(number_of_states / 4)
    step = 1
    if maximum_number_of_patterns > 1000:
        step = math.floor(maximum_number_of_patterns / 100)
    return list(range(2, maximum_number_of_patterns, step))

number_of_states_list = [x * 1000 for x in range(1, 11)]

