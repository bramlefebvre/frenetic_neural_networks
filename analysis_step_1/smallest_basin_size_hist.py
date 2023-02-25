'''
Frenetic steering: implementations of the algorithms described in the paper 'Frenetic steering in a nonequilibrium graph'.
Copyright (C) 2022-2023 Bram Lefebvre

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General
Public License as published by the Free Software Foundation, either version 3 of the License, or (at your
option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even
the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

A copy of the GNU General Public License is in the file COPYING. It can also be found at
<https://www.gnu.org/licenses/>.
'''


import daos.step_1_training_analysis_data_dao as step_1_training_analysis_data_dao
import matplotlib.pyplot as plt


def smallest_basin_size_hist():
    training_data_list = step_1_training_analysis_data_dao.get_training_data('data/step_1/s50_p5')

    smallest_basin_size_map = {}

    for result in training_data_list:
        if result.sizes_of_basins is None:
            raise ValueError('sizes of basins is None')
        smallest_basin_size = min(result.sizes_of_basins)
        if smallest_basin_size not in smallest_basin_size_map:
            smallest_basin_size_map[smallest_basin_size] = 0
        smallest_basin_size_map[smallest_basin_size] +=1
    
    print(smallest_basin_size_map)

    smallest_basin_size_items = smallest_basin_size_map.items()

    plt.bar([x[0] for x in smallest_basin_size_items], [x[1] for x in smallest_basin_size_items])
    # plt.xticks([5, 6, 7, 8])
    plt.xlabel('smallest basin size')
    plt.ylabel('frequency')
    plt.show()