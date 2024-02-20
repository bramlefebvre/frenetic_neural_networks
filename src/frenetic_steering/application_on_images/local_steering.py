from frenetic_steering.application_on_images.show_image import show_image
from frenetic_steering.step_1.local_disentangling.find_local_disentangled_system import find_local_disentangled_system
from frenetic_steering.step_2.calculate_path import calculate_path
from frenetic_steering.step_2.data_structures import LearningAlgorithm
from frenetic_steering.step_2.initialize_dynamics import initialize_dynamics
from frenetic_steering.step_2.training import train_starting_with_random_vertex_n_times



travel_time = 1
driving_value = 5
initial_activity_parameter_factor = 100
learning_rate = 0.5
desired_residence_time = 0.2
training_set_size = 100
algorithm = LearningAlgorithm.LOOK_FORWARD_AND_ONLY_ONCE_PER_ARC


def local_steering():
    local_disentangled_system = find_local_disentangled_system()
    disentangled_system = local_disentangled_system.disentangled_system
    dynamics = initialize_dynamics(disentangled_system, driving_value, initial_activity_parameter_factor, travel_time)
    training_result = train_starting_with_random_vertex_n_times(dynamics, algorithm, learning_rate, desired_residence_time, training_set_size)
    dynamics = training_result.dynamics
    path = calculate_path(dynamics.rate_matrix, 0, travel_time).path # type: ignore
    last_state_index = path['state'][-1]
    last_state = local_disentangled_system.index_to_state_map[last_state_index]
    show_image(last_state)



