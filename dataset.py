import pandas as pd
import numpy as np
import csv
import json
from timeit import default_timer
import datetime
import logging
import random
from sklearn.model_selection import train_test_split

# loading data from IMDB export file
def loadImdbData(csv_ratings, csv_links='datasets/ml-latest/links.csv', csv_movies='datasets/ml-latest/movies.csv'):
    ratings = pd.read_csv(filepath_or_buffer=csv_ratings, sep=',', encoding='latin1')
    links = pd.read_csv(filepath_or_buffer=csv_links, sep=',')
    links = links.set_index('imdbId')

    currentUser = {}
    for x in ratings[['Const', 'Your Rating', 'Title']].values:
        index = int(x[0].lstrip('tt'))
        try:
            currentUser[int(links.loc[index]['movieId'])] = x[1]/2
        except: pass
    return currentUser


# loading whole MovieLensData into dict of preferences
# returns dict of movies
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

def transformPrefs(prefs):
    rev_prefs = {}
    for pos in prefs.keys():
        for key, score in prefs[pos].items():
            rev_prefs.setdefault(key, {})
            rev_prefs[key][pos] = score

    return rev_prefs

def getUsersDict(prefs_file, raw_file=False):
    """
    Gets dict of users and their rated movies from MovieLens raw data or from dict of movies.

    :param prefs_file: input josn file location
    :param raw_file: boolean; indicates whether function performs on raw MovieLens file that needs to be
    transformed to dict first or performs on dict of movies
    :return: dict of users
    """
    if raw_file == False:
        users_dict = transformPrefs(openJson(prefs_file))
    else:
        movies_dict = loadMovieLensData(file='datasets/ml-latest/ratings.csv')
        users_dict = transformPrefs(openJson(movies_dict))

    return users_dict

# saving prefs to csv file
# needs repairing
def savePrefsToCSV(target_file, fieldnames, prefs, restval=''):

    with open(target_file, mode='w') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames)
        writer.writeheader()
        for k in prefs:
            writer.writerow({field: prefs[k].get(field) or k for field in fieldnames})

# saving prefs to json file
def savePrefsToJson(target_file, prefs):
    with open(target_file, 'w') as fp:
        json.dump(obj=prefs, fp=fp, indent=4, sort_keys=False)

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

def dictToArray(dict_object):
    names = ['id', 'data']
    formats = [int, dict]
    dtype = dict(names=names, formats=formats)
    return np.array(list(dict_object.items()), dtype=dtype)


def getRidOfLongTail(movies_prefs, popular_movies, filter_users=False, power_users=None):
    all_movies = set(movies_prefs.keys())
    all_users = set(transformPrefs(movies_prefs).keys())

    for movie_id in all_movies:
        if movie_id not in popular_movies:
            movies_prefs.pop(movie_id)

    if filter_users == True:
        for movie_id in popular_movies:
            for user_id in all_users:
                if user_id not in power_users:
                    try:
                        movies_prefs[movie_id].pop(user_id)
                    except:
                        pass

    return movies_prefs

# splits movies of every user within test / train set into another train/test sets
# perc variable states percentage of test set, 100%-perc goes to train set
def usersInnerSplit(set_dict, users_prefs, perc, random_state):
    prefs_f_test_set = {key: values for key, values in users_prefs.items() if key in set_dict}
    users_test_train = prefs_f_test_set.copy()
    users_test_test = prefs_f_test_set.copy()

    print('start', '-----', datetime.datetime.now())
    dict_len = len(users_test_test)
    i = 0
    for user in prefs_f_test_set.keys():
        random.seed(random_state)
        items_to_remove = random.sample(list(prefs_f_test_set[user].keys()), k=int(len(prefs_f_test_set[user]) * perc))
        users_test_train[user] = {key: values for key, values in users_test_train[user].items()
                                  if key not in items_to_remove}
        users_test_test[user] = {key: values for key, values in users_test_test[user].items()
                                 if key in items_to_remove}

        i += 1
        if i % 5000 == 0:
            print(str(i) + '/' + str(dict_len), datetime.datetime.now())
    print('end', '-----', datetime.datetime.now())

    return users_test_train, users_test_test
