import similarity
import pandas as pd
import datetime
from timeit import default_timer


# returns topMatches for pos1 object on a basis of used distance function, work for critics and movies
def topMatches(prefs, pos1, distance=similarity.pearson, n=10):
    result = [(distance(prefs, pos1, pos), pos) for pos in prefs if pos != pos1]

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

# building dict - position: [recommended positions]
def buildRecomSet(prefs, n=100):
    # n is number recommended movies per movie
    now = datetime.datetime.now()
    print(now)
    recom_set = {}
    # f = pd.read_csv(filepath_or_buffer=movies_dict, sep=',')
    # f = f.set_index('movieId')
    rows_count = len(prefs)
    i = 1
    start = default_timer()
    # for pos in prefs.keys():
    #     recom_set[f[pos]['movieId']] = topMatches(prefs=prefs, pos1=pos, n=n)
    #     if i%100 == 0:
    #         print(str(i)+':', f[pos], '('+f[pos]['movieId']+')')
    #     i += 1
    for pos in prefs:
        recom_set[pos] = topMatches(prefs=prefs, pos1=pos, n=n)

        print(str(i)+':', pos, 'of movieId')
        # print(type(pos), pos, recom_set[pos])

        end = default_timer()
        duration = end - start
        perc_of_total = (i)/rows_count
        est_total_duration = duration / perc_of_total
        est_time_end = now+datetime.timedelta(seconds=est_total_duration)
        print(i, '/', rows_count, str(round(perc_of_total*100, 2))+'%', round(duration/60, 2), 'minutes. Estimated end time:', est_time_end, '    Started at', now)
        # if i == 16:
        #     break
        i += 1
    print('Recommendations built for {0} movies'.format(i, datetime.datetime.now()))
    now = datetime.datetime.now()
    print(now)
    return recom_set