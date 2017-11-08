# to run cProfile: python -m cProfile -s cumtime exec_2.py
# to run line_profiler: C:\ProgramData\Anaconda3\Scripts>kernprof -l -v C:\Users\artur\PycharmProjects\Recommendations_art\exec_2.py

import recommendations as rec
# import similarity as sim
import dataset
# import cProfile

# data = dataset.openJson(file='datasets/prefs.json')
#
# prefs = rec.buildRecomSet(prefs=data, n=1000000)
#
# dataset.savePrefsToJson(target_file='datasets/movies_recommendations_lotr.json', prefs=prefs)


my_ratings = dataset.loadImdbData(csv_ratings='datasets/imdb-ratings.csv', csv_links='datasets/ml-latest/links.csv', csv_movies='datasets/ml-latest/movies.csv')

print(my_ratings)
