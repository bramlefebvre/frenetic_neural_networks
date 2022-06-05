import pstats

stats = pstats.Stats('step_1_profiler_data')
stats.sort_stats(pstats.SortKey.CUMULATIVE).print_stats(20)