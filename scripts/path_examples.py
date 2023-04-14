import frenetic_steering.daos.disentangled_systems_dao as disentangled_systems_dao

from frenetic_steering.step_2.calculate_path import calculate_path
from frenetic_steering.step_2.data_structures import LearningAlgorithm
from frenetic_steering.step_2.initialize_dynamics import initialize_dynamics
from frenetic_steering.step_2.training import train_starting_with_random_vertex_n_times
import matplotlib.pyplot as plt

disentangled_system = disentangled_systems_dao.get_single_disentangled_system('example_thesis', 'data/disentangled_systems')

initial_dynamics = initialize_dynamics(disentangled_system, 5, 20, 1)

initial_state = 3
travel_time = 1

dynamics = train_starting_with_random_vertex_n_times(initial_dynamics, LearningAlgorithm.LOOK_FORWARD_AND_ONLY_ONCE_PER_ARC, 0.5, 0.2, 32).dynamics



path = calculate_path(dynamics.rate_matrix, initial_state, travel_time)

jump_times = path.path['jump_time'].tolist()
jump_times.append(1)
states = path.path['state'].tolist()
states.append(0) 

plt.step(jump_times, states, where='post')
plt.xlabel('time(s)')
plt.ylabel('state')
plt.show()

