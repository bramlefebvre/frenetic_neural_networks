'''
Frenetic steering: implementations of the algorithms described in the paper 'Frenetic steering in a nonequilibrium graph'.
Copyright (C) 2022-2024 Bram Lefebvre

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General
Public License as published by the Free Software Foundation, either version 3 of the License, or (at your
option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even
the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

A copy of the GNU General Public License is in the file COPYING. It can also be found at
<https://www.gnu.org/licenses/>.
'''

from frenetic_steering.application_on_images.show_image import show_image
from frenetic_steering.step_1.local_disentangling.find_local_disentangled_system import find_local_disentangled_system
from frenetic_steering.step_2.calculate_path import calculate_path
from frenetic_steering.step_2.data_structures import LearningAlgorithm
from frenetic_steering.step_2.initialize_dynamics import initialize_dynamics
from frenetic_steering.step_2.training import train_starting_with_random_vertex_n_times
from frenetic_steering.daos import base_dao
from frenetic_steering.application_on_images import load_images

config = base_dao.read_data("config")
input_file = config["input_file"] # type: ignore

travel_time = 1
driving_value = 5
initial_activity_parameter_factor = 1000
learning_rate = 0.5
desired_residence_time = 0.2
training_set_size = 100
algorithm = LearningAlgorithm.LOOK_FORWARD_AND_ONLY_ONCE_PER_ARC


def local_steering_and_show():
    input = load_images.load_image(input_file)
    last_state = local_steering(input)
    show_image(last_state)


def local_steering(input):
    local_disentangled_system = find_local_disentangled_system(input)
    disentangled_system = local_disentangled_system.disentangled_system
    dynamics = initialize_dynamics(disentangled_system, driving_value, initial_activity_parameter_factor, travel_time)
    training_result = train_starting_with_random_vertex_n_times(dynamics, algorithm, learning_rate, desired_residence_time, training_set_size)
    dynamics = training_result.dynamics
    path = calculate_path(dynamics.rate_matrix, 0, travel_time).path # type: ignore
    last_state_index = path['state'][-1]
    last_state = local_disentangled_system.index_to_state_function(last_state_index)
    return last_state



