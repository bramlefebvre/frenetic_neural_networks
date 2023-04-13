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


import frenetic_steering.daos.step_1_training_analysis_data_dao as step_1_training_analysis_data_dao
import matplotlib.pyplot as plt
from frenetic_steering.step_1.data_structures import TrainingAnalysisData
from statistics import median

def plot_median_smallest_basin_size_dependency_on_s():
    filename = 'data/step_1/sv_px_sdivp10_2'
    training_data_list = step_1_training_analysis_data_dao.get_training_data(filename)
    
    sorted_results: dict[int, list[TrainingAnalysisData]] = {}
    for result in training_data_list:
        number_of_states = result.number_of_states
        if number_of_states not in sorted_results:
            sorted_results[number_of_states] = []
        sorted_results[number_of_states].append(result)
    
    number_of_states_list = []
    median_smallest_basin_list = []

    for number_of_states, results in sorted_results.items():
        number_of_states_list.append(number_of_states)
        median_smallest_basin_list.append(_get_median_smallest_basin_size(results))

    plt.scatter(number_of_states_list, median_smallest_basin_list)
    plt.xlabel('number of states')
    plt.ylabel('median smallest basin size')
    plt.show()

def _get_median_smallest_basin_size(results):
    smallest_basin_size_list = []
    for result in results:
        smallest_basin_size = min(result.sizes_of_basins)
        smallest_basin_size_list.append(smallest_basin_size)
    return median(smallest_basin_size_list)
    
def plot_relative_average_difference():
    filename = 'data/step_1/sv_p5'
    training_data_list = step_1_training_analysis_data_dao.get_training_data(filename)
    
    sorted_results: dict[int, list[TrainingAnalysisData]] = {}
    for result in training_data_list:
        number_of_states = result.number_of_states
        if number_of_states not in sorted_results:
            sorted_results[number_of_states] = []
        sorted_results[number_of_states].append(result)
    
    number_of_states_list = []
    percentual_average_difference_list = []
    for number_of_states, results in sorted_results.items():
        number_of_states_list.append(number_of_states)
        percentual_average_difference_list.append(_get_relative_average_difference(number_of_states, results))

    plt.scatter(number_of_states_list, percentual_average_difference_list)
    plt.xlabel('number of states')
    plt.ylabel(r'$D_{dis} \cdot k/(N-k)\ (\%)$')
    plt.show()
    

def _get_relative_average_difference(number_of_states, results):
    number = 0
    summed_average_differences = 0
    number_of_patterns = results[0].number_of_patterns
    for result in results:
        assert result.number_of_patterns == number_of_patterns
        number += 1
        sizes_of_basins = result.sizes_of_basins
        if sizes_of_basins is None:
            raise ValueError('sizes of basins is None')
        summed_average_differences += _calculate_average_difference(sizes_of_basins)
        # for single state patterns
    return 100 * summed_average_differences / (number * (number_of_states / number_of_patterns - 1))
    

def plot_dependency_on_s():
    filename = 'data/step_1/sv_px_sdivp10_3'
    training_data_list = step_1_training_analysis_data_dao.get_training_data(filename)
    
    sorted_results: dict[int, list[TrainingAnalysisData]] = {}
    for result in training_data_list:
        number_of_states = result.number_of_states
        if number_of_states not in sorted_results:
            sorted_results[number_of_states] = []
        sorted_results[number_of_states].append(result)
    
    number_of_states_list: list[int] = []
    average_difference_list: list[float] = []

    for number_of_states, results in sorted_results.items():
        number_of_states_list.append(number_of_states)
        number = 0
        summed_average_differences = 0
        for result in results:
            number += 1
            sizes_of_basins = result.sizes_of_basins
            if sizes_of_basins is None:
                raise ValueError('sizes of basins is None')
            summed_average_differences += _calculate_average_difference(sizes_of_basins)
        average_difference_list.append(summed_average_differences / number)

    plt.scatter(number_of_states_list, average_difference_list)
    plt.xlabel('number of states')
    plt.ylabel('average difference in size basins')
    plt.show()

def plot_dependency_on_k():
    filename = 'data/step_1/s1000_pv'
    training_data_list = step_1_training_analysis_data_dao.get_training_data(filename)
    
    sorted_results: dict[int, list[TrainingAnalysisData]] = {}
    for result in training_data_list:
        number_of_patterns = result.number_of_patterns
        if number_of_patterns not in sorted_results:
            sorted_results[number_of_patterns] = []
        sorted_results[number_of_patterns].append(result)
    
    number_of_patterns_list: list[int] = []
    average_difference_list: list[float] = []

    for number_of_patterns, results in sorted_results.items():
        number_of_patterns_list.append(number_of_patterns)
        number = 0
        summed_average_differences = 0
        for result in results:
            number += 1
            sizes_of_basins = result.sizes_of_basins
            if sizes_of_basins is None:
                raise ValueError('sizes of basins is None')
            summed_average_differences += _calculate_average_difference(sizes_of_basins)
        average_difference_list.append(summed_average_differences / number)

    plt.scatter(number_of_patterns_list, average_difference_list)
    plt.xlabel('number of patterns')
    plt.ylabel('$D_{dis}$')
    plt.show()

def plot_dependency_on_d():
    filename = 'data/step_1/s50_p5_dv'
    training_data_list = step_1_training_analysis_data_dao.get_training_data(filename)
    sorted_results: dict[float, list[TrainingAnalysisData]] = {}
    for result in training_data_list:
        fraction_of_arcs_present = result.fraction_of_arcs_present
        if fraction_of_arcs_present not in sorted_results:
            sorted_results[fraction_of_arcs_present] = []
        sorted_results[fraction_of_arcs_present].append(result)
    
    fraction_of_arcs_present_list = []
    average_difference_list = []

    for fraction_of_arcs_present, results in sorted_results.items():
        fraction_of_arcs_present_list.append(fraction_of_arcs_present)
        number = 0
        summed_average_differences = 0
        for result in results:
            number += 1
            sizes_of_basins = result.sizes_of_basins
            if sizes_of_basins is None:
                raise ValueError('sizes of basins is None')
            summed_average_differences += _calculate_average_difference(sizes_of_basins)
        average_difference_list.append(summed_average_differences / number)
    
    print('fraction of arcs present list:')
    print(fraction_of_arcs_present_list)
    print('average difference in size basins:')
    print(average_difference_list)


    # plt.scatter(fraction_of_arcs_present_list, average_difference_list)
    # plt.xlabel('fraction of arcs present')
    # plt.ylabel('average difference in size basins')
    # plt.show()




def _calculate_average_difference(sizes_of_basins: list[int]):
    if len(sizes_of_basins) == 1:
        return 0
    sum = 0
    for index, size_of_basin_0 in enumerate(sizes_of_basins):
        for size_of_basin_1 in sizes_of_basins[index + 1:]:
            sum += abs(size_of_basin_1 - size_of_basin_0)
    number_of_basins = len(sizes_of_basins)
    number_of_terms = number_of_basins * (number_of_basins - 1) / 2
    return sum / number_of_terms

def _calculate_variance(sizes_of_basins: list[int]):
    sum = 0
    for size_of_basin_0 in sizes_of_basins:
        for size_of_basin_1 in sizes_of_basins:
            sum += (size_of_basin_0 - size_of_basin_1) ** 2
    return (1 / (len(sizes_of_basins) ** 2)) * sum

