# to run cProfile: python -m cProfile -s cumtime exec_2.py
# to run line_profiler: C:\ProgramData\Anaconda3\Scripts>kernprof -l -v C:\Users\artur\PycharmProjects\Recommendations_art\exec_2.py

import recommendations as rec
import similarity as sim
import dataset
# import cProfile
import json


# movies = dataset.openJson('datasets/movies_recommendations_total.json')
# print(type(movies))
# my_ratings = dataset.loadImdbData(csv_ratings='datasets/imdb-ratings.csv', csv_links='datasets/ml-latest/links.csv', csv_movies='datasets/ml-latest/movies.csv')
# print(my_ratings['95294'])
# result = rec.getRecommendedItems(user_prefs=my_ratings, movies_sim=movies)
# print(result)

rec.executeDictSimMovies(prefs_file='datasets/prefs.json', target_file='datasets/similar_movies_2019.json', distance=sim.pearson)

# test_prefs = {'a': {'aa': 1, 'bb': 2, 'cc': 3}, 'b':{'aa': 1, 'bb': 5, 'cc': 7}}
# print(sim.pearson(sim.critics, 'Lisa Rose', 'Claudia Puig'))
# print(sim.pearson(test_prefs, 'a', 'b'))
# print(sim.pearson_numpy(test_prefs, 'a', 'b'))