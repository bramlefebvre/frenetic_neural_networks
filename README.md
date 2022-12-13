# Frenetic steering

This project contains the code of the implementations of the algorithms described in the paper 'Frenetic steering in a nonequilibrium graph'.

step_1 signifies the disentanglement algorithm, step_2 signifies the frenetic steering algorithm.

The starting point for the implementation of the algorithm for disentangling the basins of attraction is in the file step_1/find_exuberant_system.py

The starting point for the implementation of the algorithm based on the proof of Moon's theorem is in the file step_1/find_cycle.py

The starting point for the implementation of Manoussakis's algorithm is in the file step_1/find_hamilton_cycle.py

The starting point for the implementation of the algorithm for eliminating cycles that don't contain a pattern vertex is in the file step_1/eliminate_cycles_outside_pattern.py

The starting point for the implementation of the algorithm for frenetic steering is in the file step_2/execute_learning_step/algorithm_3/algorithm_3.py

In the folders analysis_step_1 and analysis_step_2 code can be found that was used to investigate the performance of the algorithms. 

The writer of the program, Bram Lefebvre, can be reached at bramlefebvre@gmail.com.