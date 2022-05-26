from step_1.find_exuberant_system import find_exuberant_system
import daos.tournaments_and_patterns_dao as tournaments_and_patterns_dao
import time
import timeit

tournament_and_patterns = tournaments_and_patterns_dao.get_tournaments_and_patterns('data/step_1/tournament_1000_50')[0]


timer = timeit.Timer(lambda: find_exuberant_system(tournament_and_patterns))
times_executed, total_duration = timer.autorange()
# find_exuberant_system(tournament_and_patterns)
print('times executed:')
print(times_executed)
# elapsed_time_in_micro_seconds = (end_time - start_time) / (10 ** 3)
print('elapsed time:')
print(total_duration)

start_time = time.time_ns()
find_exuberant_system(tournament_and_patterns)
end_time = time.time_ns()
print('time ms:')
print((end_time - start_time) / 10 ** 6)


