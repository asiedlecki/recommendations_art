# to run cProfile: python -m cProfile -s cumtime exec_2.py
# to run line_profiler: C:\ProgramData\Anaconda3\Scripts>kernprof -l -v C:\Users\artur\PycharmProjects\Recommendations_art\exec_2.py

import recommendations as rec
# import similarity as sim
import dataset
# import cProfile
import json

# data = dataset.openJson(file='datasets/prefs.json')
# popular_items = rec.getPopularMovies(data)
#
# prefs = rec.buildRecomSet(prefs=data, n=1000)
#
# dataset.savePrefsToJson(target_file='datasets/movies_recommendations_lotr.json', prefs=prefs)

# movies = dataset.openJson('datasets/movies_recommendations_total.json')
# print(type(movies))
# my_ratings = dataset.loadImdbData(csv_ratings='datasets/imdb-ratings.csv', csv_links='datasets/ml-latest/links.csv', csv_movies='datasets/ml-latest/movies.csv')
# print(my_ratings['95294'])
# result = rec.getRecommendedItems(user_prefs=my_ratings, movies_sim=movies)
# print(result)

rec.executeDictSimMovies(prefs_file='datasets/prefs.json', target_file='datasets/similar_movies.json')