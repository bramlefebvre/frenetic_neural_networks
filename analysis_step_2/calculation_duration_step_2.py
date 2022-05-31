from daos.step_2_training_results_dao import save_calculation_duration_results
from daos.tournaments_and_patterns_dao import generate_single_tournament_and_patterns
from step_1.find_exuberant_system import find_exuberant_system
from step_2.data_structures import LearningAlgorithm
from step_2.initialize_dynamics import initialize_dynamics
from step_2.training import train_starting_with_random_vertex_n_times
from analysis_step_2.data_structures import CalculationDurationResult
import util
import timeit
import time

def generate_initial_activity_parameter_factors_list(number_of_states, number_of_patterns):
    fraction = 1 / 10 * number_of_states / number_of_patterns
    return [fraction * 2, fraction * 4]

def generate_training_set_size_list(number_of_states):
    return [number_of_states * 2, number_of_states * 4]

number_of_states_list = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
algorithm = LearningAlgorithm.LOOK_FORWARD_AND_ONLY_ONCE_PER_ARC
driving_value = 5
travel_time = 1
learning_rate = 0.5
desired_residence_time = 0.2
filename = 'data/step_2/calculation_duration_0'

def calculation_duration():
    for number_of_states in number_of_states_list:
        results = []
        number_of_patterns_list = util.generate_number_of_patterns_list(number_of_states)
        for number_of_patterns in number_of_patterns_list:
            exuberant_systems = util.generate_exuberant_systems(number_of_states, number_of_patterns)
            initial_activity_parameter_factors = generate_initial_activity_parameter_factors_list(number_of_states, number_of_patterns)
            for initial_activity_parameter_factor in initial_activity_parameter_factors:
                training_set_size_list = generate_training_set_size_list(number_of_states)
                for training_set_size in training_set_size_list:
                    print('[number_of_states, number_of_patterns, initial_activity_parameter_factor, training_set_size]:')
                    print([number_of_states, number_of_patterns, initial_activity_parameter_factor, training_set_size])
                    for exuberant_system in exuberant_systems:
                        initial_dynamics = initialize_dynamics(exuberant_system, driving_value, initial_activity_parameter_factor, travel_time)
                        timer = timeit.Timer(lambda: train_starting_with_random_vertex_n_times(initial_dynamics, algorithm, learning_rate, desired_residence_time, training_set_size), timer = time.process_time)
                        times_executed, total_duration = timer.autorange()
                        calculation_duration = (total_duration / times_executed) * 10 ** 3
                        result = CalculationDurationResult(exuberant_system.id, None, number_of_states, number_of_patterns, driving_value, initial_activity_parameter_factor, travel_time, algorithm, learning_rate, desired_residence_time, training_set_size, calculation_duration)
                        results.append(result)
        save_calculation_duration_results(results, filename)