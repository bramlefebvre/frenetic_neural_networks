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

from frenetic_steering.application_on_images import load_images
from frenetic_steering.step_1.local_disentangling.util import number_of_spins_with_different_value


def find_closest_pattern():
    input = load_images.load_input()
    distances = []
    for i in range(load_images.get_number_of_patterns()):
        pattern = load_images.load_pattern(i)
        distances.append(number_of_spins_with_different_value(input, pattern))
    minimum_distance = min(distances)
    index_minimum = distances.index(minimum_distance)
    return (load_images.load_pattern(index_minimum), minimum_distance)
        
