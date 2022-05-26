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

