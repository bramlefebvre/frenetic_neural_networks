import daos.tournaments_and_patterns as tournaments_and_patterns
import numpy
import step_2.execute_learning_step_bram as execute_learning_step_bram

# tournament_and_patterns = tournaments_and_patterns.get_single_tournament_and_patterns('fig.4.11', 'testfile_1.json')


a = [[1, 2], [3, 4]]
b = numpy.array(a)
print(b)
b[0, 1] += 1
print(b)