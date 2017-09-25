import similarity

def topMatches(prefs, pos1, distance=similarity.pearson, n=10):
    result = [(distance(prefs, pos1, pos), pos) for pos in prefs.keys() if pos != pos1]

    result.sort(reverse=True)
    return result[:n]

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