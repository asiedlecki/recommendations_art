# to run cProfile: python -m cProfile -s cumtime exec_2.py
# to run line_profiler: C:\ProgramData\Anaconda3\Scripts>kernprof -l -v C:\Users\artur\PycharmProjects\Recommendations_art\exec_2.py

import recommendations as rec
# import similarity as sim
import dataset
# import cProfile

data = dataset.openJson(file='C:/Users/artur/PycharmProjects/Recommendations_art/datasets/prefs.json')
# pearson_pairs = rec.buildPearsonDict(data)
# dataset.savePrefsToJson(target_file='datasets/movies_pearson_pairs.json', prefs=pearson_pairs)
prefs = rec.buildRecomSet(prefs=data, n=100)
#
dataset.savePrefsToJson(target_file='datasets/movies_recommendations_total.json', prefs=prefs)
