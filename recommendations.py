import similarity
import pandas as pd
import datetime
from timeit import default_timer
import copy


# returns topMatches for pos1 object on a basis of used distance function, work for critics and movies
def topMatches(prefs, pos1, distance=similarity.pearson, n=10):
    result = [(distance(prefs, pos1, pos), pos) for pos in prefs if pos != pos1]

    result.sort(reverse=True)
    return result[:n]

def topMatchesBuffered(prefs, pos1, distance=similarity.pearson, n=10):
    result = []
    pearson_buffer = {}
    for pos in prefs:
        if pos != pos1:
            if '_'.join(sorted([pos1, pos])) in pearson_buffer:
                pass
            else:
                pearson = distance(prefs, pos1, pos)
                pearson_buffer['_'.join(sorted([pos1, pos]))] = pearson
                result.append((pearson, pos))
    result.sort(reverse=True)
    return result[:n]

# create recommendations for particular critic (sorted list of tuples: (rating, movie)), works for critics only (uses critics similarity)
def synthMeter(prefs, pos1, distance=similarity.pearson, n=10): # n is a number of recommendations to return
    # create a dict of critics and their correlation coefficent to pos1
    r = {pos2: distance(prefs, pos1, pos2) for pos2 in prefs.keys() if pos1 != pos2}

    items_scores = {}
    items_div = {}
    for pos, distance in r.items():
        for item, rating in prefs[pos].items():
            if item not in prefs[pos1].keys(): # not to compare to the same position/person
                items_scores.setdefault(item, 0)
                items_div.setdefault(item, 0)
                items_scores[item] += sum([rating*distance])
                items_div[item] += sum([distance])
    recommendations = [(rating/items_div[item], item) for item, rating in items_scores.items()]
    recommendations.sort(reverse=True)
    return recommendations[:n]

def transformPrefs(prefs):
    rev_prefs = {}
    for pos in prefs.keys():
        for key, score in prefs[pos].items():
            rev_prefs.setdefault(key, {})
            rev_prefs[key][pos] = score

    return rev_prefs

def buildPearsonDict(prefs):
    start = datetime.datetime.now()
    print('buildPearsonDict started at {0}'.format(start))
    movies = {x for x in prefs}
    movies = [x for x in movies]
    movies.sort(reverse=True)
    len_movies = len(movies)
    print(len_movies, type(movies))
    diff = datetime.datetime.now()-start
    diff = diff.total_seconds()
    print('building set of movies finished at {0}, it took {1} minutes {2} seconds'.format(datetime.datetime.now(), divmod(diff, 60)[0], divmod(diff, 60)[1]))
    moviePairs = {}
    i = 1
    start_datetime = datetime.datetime.now()
    start = default_timer()
    for movie1 in movies:
        for movie2 in movies:
            # if '{0}_{1}'.format(movie1, movie2) in moviePairs or '{0}_{1}'.format(movie2, movie1) in moviePairs:
            #     pass
            # else:
            #     moviePairs['{0}_{1}'.format(movie1, movie2)] = similarity.pearson(prefs, movie1, movie2)
            if '_'.join(sorted([movie1, movie2])) in moviePairs:
                pass
            else:
                moviePairs['_'.join(sorted([movie1, movie2]))] = similarity.pearson(prefs, movie1, movie2)
        if i % 50 == 0:
            end = default_timer()
            duration = end - start
            perc_of_total = i / len_movies
            est_total_duration = duration / perc_of_total
            est_time_end = start_datetime + datetime.timedelta(seconds=est_total_duration)
            print(i, '/', len_movies, str(round(perc_of_total * 100, 2)) + '%', round(duration / 60, 2),
                  'minutes. Estimated end time:', est_time_end, '    Started at', start_datetime)
        if i % 300 == 0:
            break
        i += 1
    print('moviePairs finished at {0}'.format(datetime.datetime.now()))
    return moviePairs

# building dict - position: [recommended positions]
def buildRecomSet(prefs, distance=similarity.pearson, n=100):
    # n is number recommended movies per movie
    now = datetime.datetime.now()
    print(now)
    recom_set = {}
    rows_count = len(prefs)
    i = 0
    pearson_buffer = {}
    start = default_timer()
    for pos in prefs.keys():
        recom_set[f[pos]['movieId']] = topMatches(prefs=prefs, pos1=pos, n=n)
        if i%100 == 0:
            print(str(i)+':', f[pos], '('+f[pos]['movieId']+')')
        i += 1

    for pos1 in prefs:
        i += 1
        result = []
        for pos in prefs:
            if pos != pos1:
                comp_key = '_'.join(sorted([pos1, pos]))
                if comp_key in pearson_buffer:
                    result.append((pearson_buffer[comp_key], pos))
                    pearson_buffer.pop(comp_key)
                    # pearson_buffer[comp_key][0] += 1
                else:
                    pearson = distance(prefs, pos1, pos)
                    if len(pearson_buffer) <= 30000000:
                        pearson_buffer[comp_key] = pearson
                    result.append((pearson, pos))
                    # print('pos: {0}, pearson: {1}'.format(pos, pearson))
        result.sort(reverse=True)

        if result:
            recom_set[pos1] = result[:n]

        print(str(i)+':', pos1, 'of movieId')
        # print(type(pos), pos, recom_set[pos])

        end = default_timer()
        duration = end - start
        perc_of_total = (i)/rows_count
        est_total_duration = duration / perc_of_total
        est_time_end = now+datetime.timedelta(seconds=est_total_duration)
        print(i, '/', rows_count, str(round(perc_of_total*100, 2))+'%', round(duration/60, 2), 'minutes. Estimated end time:', est_time_end, '    Started at', now)
        if i%20 == 0:
            print('Length of pearson_buffer:', len(pearson_buffer))

    print('Recommendations built for {0} movies'.format(i, datetime.datetime.now()))
    now = datetime.datetime.now()
    print(now)
    return recom_set