import recommendations as rec
# import similarity as sim
import dataset
import cProfile
# import math
# import multiprocessing

# if __name__ == '__main__':
#     pool_size = multiprocessing.cpu_count()
#     pool = multiprocessing.Pool(processes=pool_size-1)

prefs = dataset.loadMovieLensData(file='datasets/ml-latest/ratings.csv')
dataset.savePrefsToJson(target_file='datasets/prefs_v2.json', prefs=prefs)

# data = dataset.openJson(file='datasets/prefs.json')
# print(type(data))
# rec.buildRecomSet(prefs=data, n=100)

# dataset.savePrefsToJson(target_file='datasets/movies_recommendations.json', prefs=prefs)


# rec.testIndex(prefs_file='datasets/prefs.json', movies_file='datasets/ml-latest/movies.csv')