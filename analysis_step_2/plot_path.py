from daos.exuberant_systems_dao import get_single_exuberant_system
from step_2.data_structures import LearningAlgorithm
from step_2.initialize_dynamics import initialize_dynamics
from step_2.training import train_starting_with_random_vertex_n_times
from step_2.calculate_performance import calculate_performance
from step_2.calculate_path import calculate_path
import matplotlib.pyplot as plt

exuberant_system = get_single_exuberant_system('example_thesis', 'data/exuberant_systems')

initial_dynamics = initialize_dynamics(exuberant_system, 5, 0.3, 1)
training_result = train_starting_with_random_vertex_n_times(initial_dynamics, LearningAlgorithm.LOOK_FORWARD_AND_ONLY_ONCE_PER_ARC, 0.5, 0.2, 32)
trained_dynamics = training_result.dynamics
performance = calculate_performance(training_result.dynamics, 0.2, 100)
print(performance)
path = calculate_path(initial_dynamics.rate_matrix, 3, 1)
print(path.path)
jump_times = path.path['jump_time'].tolist()
jump_times.append(1)
states = path.path['state'].tolist()
states.append(states[-1])

plt.step(jump_times, states, where='post')
plt.xlabel('time(s)')
plt.ylabel('state')
plt.show()