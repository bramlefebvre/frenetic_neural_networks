import pstats

stats = pstats.Stats('data/step_2_profiler_data_2')
stats.sort_stats(pstats.SortKey.CUMULATIVE).print_stats(20)