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


from analysis_step_1.train_step_1 import train as train_step_1
from analysis_step_1.calculation_duration_step_1 import calculation_duration as calculation_duration_step_1
from analysis_step_1.calculation_duration_step_1 import print_mean_duration
from analysis_step_1.analyse_sizes_basins import plot_dependency_on_s as step_1_plot_dependency_on_s
from analysis_step_1.analyse_sizes_basins import plot_dependency_on_k as step_1_plot_dependency_on_k
from analysis_step_1.analyse_sizes_basins import plot_median_smallest_basin_size_dependency_on_s
from analysis_step_1.analyse_sizes_basins import plot_percentual_average_difference
from analysis_step_1.plot_s_calc import plot_s_calc as step_1_plot_s_calc
from analysis_step_1.plot_k_calc import plot_k_calc as step_1_plot_k_calc
from analysis_step_1.plot_s_success import plot_s_success as step_1_plot_s_success
from analysis_step_1.plot_k_success import plot_k_success as step_1_plot_k_success
from analysis_step_2.train_cycles import train_cycles
from analysis_step_2.train_cycles import train_cycles_R
from analysis_step_2.train_step_2 import train as train_step_2
from analysis_step_2.train_step_2 import train_driving_value
from analysis_step_2.train_step_2 import train_R
from analysis_step_2.calculation_duration_step_2 import calculation_duration as calculation_duration_step_2
from analysis_step_2.plot_s_performance import plot_s_performance
from analysis_step_2.plot_k_performance import plot_k_performance
from analysis_step_2.plot_a_performance import plot_a_performance
from analysis_step_2.plot_n_performance import plot_n_performance
from analysis_step_2.plot_s_success import plot_s_success
from analysis_step_2.plot_k_success import plot_k_success
from analysis_step_2.plot_a_success import plot_a_success
from analysis_step_2.plot_n_success import plot_n_success
from analysis_step_2.plot_s_calc import plot_s_calc
from analysis_step_2.plot_k_calc import plot_k_calc
from analysis_step_2.plot_e_performance import plot_e_performance
from demo_1.demo_step_1 import demo_step_1
from demo_1.demo_step_2 import demo_step_2
from demo_1.demo_step_2_2 import demo_step_2_2
from analysis_step_1.smallest_basin_size_hist import smallest_basin_size_hist

print_mean_duration()