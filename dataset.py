import pandas as pd
import json
from timeit import default_timer
import datetime
import logging

# loading data from IMDB export file
def loadImdbData(csv_ratings, csv_links='datasets/ml-latest/links.csv', csv_movies='datasets/ml-latest/movies.csv'):
    ratings = pd.read_csv(filepath_or_buffer=csv_ratings, sep=',', encoding='latin1')
    links = pd.read_csv(filepath_or_buffer=csv_links, sep=',')
    links = links.set_index('imdbId')

    currentUser = {}
    for x in ratings[['const', 'You rated', 'Title']].values:
        index = int(x[0].lstrip('tt'))
        try:
            currentUser[int(links.loc[index]['movieId'])] = x[1]/2
        except: pass
    return currentUser


# loading whole MovieLensData into dict of preferences
def loadMovieLensData(file):
    start = default_timer()
    logging.basicConfig(filename='loadMovieLensData.log', level=logging.DEBUG)
    f = pd.read_csv(filepath_or_buffer=file, sep=',')
    rows_count = f.shape[0]
    prefs = {}

    # data will be loaded as dictionary of movies (to omit transformPrefs functions in next queries)
    i = 0
    now = datetime.datetime.now()
    print(now)
    while True and i < rows_count:
        try:
            movieId = str(int(f.iloc[i][1]))
            userId = str(int(f.iloc[i][0]))
            rating = f.iloc[i][2]
            prefs.setdefault(movieId, {})
            prefs[movieId][userId] = rating

            # i += 1
        except ValueError:
            print('valueError', i)
            logging.warning(i, 'item could not be parsed as ValueError at', datetime.datetime.now())
        except:
            print('error', i)
            logging.warning(i, 'item could not be parsed at', datetime.datetime.now())

        if (i+1)%50000 == 0:
            end = default_timer()
            duration = end - start
            perc_of_total = (i+1)/rows_count
            est_total_duration = duration / perc_of_total
            est_time_end = now+datetime.timedelta(seconds=est_total_duration)
            print(i+1, '/', rows_count, str(round(perc_of_total*100, 2))+'%', round(duration/60, 2), 'minutes. Estimated end time:', est_time_end, '    Started at', now)
            #and i < 101

        i += 1

    return prefs

# saving prefs to json file
def savePrefsToJson(target_file, prefs):
    with open(target_file, 'w') as fp:
        json.dump(obj=prefs, fp=fp, indent=4, sort_keys=True)

def openJson(file):
    with open(file, 'r') as fp:
        data = json.load(fp)
    return data

# def csvToJson(file, json_orient='columns'):
#     f = pd.read_csv(filepath_or_buffer=file, sep=',')
#     f = f['user\Id', 'movieId', 'rating']
#     f.to_csv(path_or_buf='datasets/ml-latest/ratings_v2.csv', sep=',')
    # f.to_json(orient=json_orient, path_or_buf='datasets/ml-latest/ratings.json')
    # f.to_hdf(path_or_buf='datasets/ml-latest/ratings.h5', key='movieId', mode='w')
