from daos.tournaments_and_patterns_dao import get_single_tournament_and_patterns
import timeit
import time
from step_1.find_exuberant_system import find_exuberant_system


tournament_and_patterns = get_single_tournament_and_patterns('1000_50_0', 'data/step_1/tournament_1000_50_0')

timer = timeit.Timer(lambda: find_exuberant_system(tournament_and_patterns, True))
times_executed, total_duration = timer.autorange()
calculation_duration_perf_counter = (total_duration / times_executed) * 10 ** 3
print('perf_counter time:')
print(calculation_duration_perf_counter)

timer = timeit.Timer(lambda: find_exuberant_system(tournament_and_patterns, True), timer = time.process_time)
times_executed, total_duration = timer.autorange()
calculation_duration_process_time = (total_duration / times_executed) * 10 ** 3
print('process time:')
print(calculation_duration_process_time)