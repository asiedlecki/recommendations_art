import similarity
import pandas as pd
import datetime
from timeit import default_timer
import copy
import dataset
import sys


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

# building dict - position: [recommended positions]
# using buffer - bit faster, but much more RAM required
def buildRecomSetBuffered(prefs, distance=similarity.pearson, n=100):
    # n = number of similar movies per movie
    now = datetime.datetime.now()
    print(now)
    recom_set = {}
    rows_count = len(prefs)
    i = 0
    pearson_buffer = {}
    start = default_timer()

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
                    if len(pearson_buffer) <= 100000000000:
                        pearson_buffer[comp_key] = pearson
                    result.append((pearson, pos))
                    # print('pos: {0}, pearson: {1}'.format(pos, pearson))
        result.sort(reverse=True)

        if result:
            recom_set[pos1] = result[:n]

        if i%25 == 0:
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

# building dict - position: [recommended positions]
# not using buffer - a bit slower, but much less RAM is required
def buildRecomSet(prefs, distance=similarity.pearson, n=1000):
    # n = number of similar movies per movie
    now = datetime.datetime.now()
    print(now)
    recom_set = {}

    rows_count = len(prefs)
    i = 1
    start = default_timer()

    for pos in prefs:
        recom_set[pos] = topMatches(prefs=prefs, distance=distance, pos1=pos, n=n)

        if i % 25 == 0:
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


def getRecommendedItems(user_prefs, movies_sim):

    weighted_rating = {}
    similarity_sum = {}

    for (user_movie, user_rating) in user_prefs.items():
        if str(user_movie) in movies_sim:
            for (similarity, movie) in movies_sim[str(user_movie)]:

                # lets ignore movies that have been already rated by user
                if int(movie) in user_prefs or not similarity >= -1: continue

                # calculating sum of weighted rating of every non-watched movie
                weighted_rating.setdefault(movie, 0)
                weighted_rating[movie] += user_rating*similarity

                # summarizing all similarity measures
                similarity_sum.setdefault(movie, 0)
                similarity_sum[movie] += similarity
        else: continue

    # dividing sum of ratings by sum of similarities to get a mean of rating
    recs = [(0, movie) if similarity_sum[movie] == 0 else (round(rating/similarity_sum[movie], 6), movie) for movie, rating in weighted_rating.items()]

    # sorting recommendations
    recs.sort(reverse=True)
    return recs


def getRecommendedItems_v2(user_prefs, movies_sim):

    weighted_rating = {}
    similarity_sum = {}
    score_for_negative_corr = 0
    # sim_for_negative_corr = 0

    for (user_movie, user_rating) in user_prefs.items():
        # print(user_movie, user_rating)
        if str(user_movie) in movies_sim:
            # print(user_movie, 'in trained_data')
            for (similarity, movie) in movies_sim[str(user_movie)]:
                # lets ignore movies that have been already rated by user
                # lets ignore movies that have not been rated both by one user (distance has not been calculated for them)
                if int(movie) in user_prefs or not similarity >= -1: continue

                # calculating sum of weighted rating of every non-watched movie
                weighted_rating.setdefault(movie, 0)
                # so_far_rating = weighted_rating[movie]

                rating_norm = lambda user_rating, similarity: score_for_negative_corr if similarity < 0 else user_rating*similarity
                # rating_norm = lambda user_rating, similarity: user_rating * sim_for_negative_corr if user_rating * similarity < 0 else user_rating * similarity

                weighted_rating[movie] += rating_norm(user_rating, similarity)
                # if movie == '132456':
                # print('Weighted rating for', movie, ':', weighted_rating[movie], '=', so_far_rating, '+', user_rating, '*', similarity)

                # summarizing all similarity measures
                similarity_sum.setdefault(movie, 0)
                # so_far_sim_measures = similarity_sum[movie]
                # sim_norm = lambda similarity: score_for_negative_corr/float(user_rating) if similarity <= 0 else similarity
                # sim_norm = lambda similarity: sim_for_negative_corr if similarity <= 0 else similarity

                similarity_sum[movie] += abs(similarity)
                # if movie == '132456':
                # print('Similarity sum:', similarity_sum[movie], '=', so_far_sim_measures, '+', abs(similarity))
        else: continue

    # dividing sum of ratings by sum of similarities to get a mean of rating
    recs = [(0, movie) if similarity_sum[movie] == 0 else (round(rating/similarity_sum[movie], 6), movie) for movie, rating in weighted_rating.items()]

    # sorting recommendations
    recs.sort(reverse=True)
    return recs


def getRecommendedItems_v3(user_prefs, movies_sim):

    weighted_rating = {}
    similarity_sum = {}
    score_for_negative_corr = 0
    # sim_for_negative_corr = 0

    for user_movie, user_rating in user_prefs.items():
        # print(user_movie, type(user_movie), user_rating, type(user_rating))
        if user_movie in movies_sim:
            # print(user_movie, 'in trained_data')
            for movie, similarity in movies_sim[user_movie].items():
                # lets ignore movies that have been already rated by user
                # lets ignore movies that have not been rated both by one user (distance has not been calculated for them)
                if movie in user_prefs or not similarity >= -1:
                    # print(movie, 'in user_prefs or similarity < -1 (', similarity, ')')
                    continue

                # calculating sum of weighted rating of every non-watched movie
                weighted_rating.setdefault(movie, 0)
                # so_far_rating = weighted_rating[movie]

                rating_norm = lambda user_rating, similarity: score_for_negative_corr if similarity < 0 else user_rating*similarity
                # rating_norm = lambda user_rating, similarity: user_rating * sim_for_negative_corr if user_rating * similarity < 0 else user_rating * similarity

                weighted_rating[movie] += rating_norm(user_rating, similarity)
                # if movie == '132456':
                # print('Weighted rating for', movie, ':', weighted_rating[movie], '=', so_far_rating, '+', user_rating, '*', similarity)

                # summarizing all similarity measures
                similarity_sum.setdefault(movie, 0)
                # so_far_sim_measures = similarity_sum[movie]
                # sim_norm = lambda similarity: score_for_negative_corr/float(user_rating) if similarity <= 0 else similarity
                # sim_norm = lambda similarity: sim_for_negative_corr if similarity <= 0 else similarity

                similarity_sum[movie] += abs(similarity)
                # if movie == '132456':
                # print('Similarity sum:', similarity_sum[movie], '=', so_far_sim_measures, '+', abs(similarity))
        else: continue

    # dividing sum of ratings by sum of similarities to get a mean of rating
    recs = [(0, movie) if similarity_sum[movie] == 0 else (round(rating/similarity_sum[movie], 6), movie) for movie, rating in weighted_rating.items()]

    # sorting recommendations
    recs.sort(reverse=True)
    return recs

# 75th percentile gives good results, no other tested
def getPopularMovies(prefs, percentile=0.75, save_to_file=False, target_file='datasets/movies_popularity.json'):

    # counting number of ratings per movie
    movies_popularity = {}
    for movie in prefs:
        ratings = len(prefs[movie])
        movies_popularity[movie] = ratings

    if save_to_file:
        dataset.savePrefsToJson(target_file=target_file, prefs=movies_popularity)

    # creating data frame so as to check the given percentile
    df = pd.DataFrame.from_dict(data=movies_popularity, orient='index')
    threshold = int(df.quantile(q=percentile)[0])
    print('Minimum number of occurencies per object: {0}'.format(threshold))

    # creating set of movies for filtering
    popular_objects = set(key for key, value in movies_popularity.items() if value >= threshold)
    print('Number of objects to analyze: {0}'.format(len(popular_objects)))

    return popular_objects, threshold

# this function prepares dict of similar movies on the basis of only the most popular movies
def executeDictSimMovies(prefs_dict, target_file, most_popular=False, percentile=0.75, n=1000, distance=similarity.pearson, use_buffer=False):
    # n = number of similar movies per movie

    if most_popular == True:
        popular_items = getPopularMovies(prefs_dict, percentile)
        prefs_dict = {movie: prefs_dict[movie] for movie in popular_items}
        popular_items = None

    if use_buffer:
        prefs = buildRecomSetBuffered(prefs=prefs_dict, distance=distance, n=n)
    else:
        prefs = buildRecomSet(prefs=prefs_dict, distance=distance, n=n)

    print(sys.getsizeof(prefs)/float(1024**2), 'MB')

    dataset.savePrefsToJson(target_file=target_file, prefs=prefs)