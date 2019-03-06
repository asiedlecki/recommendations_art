from math import pow, sqrt
import numpy as np
from numba import jit, vectorize

# słownik krytyków filmowych i ich ocen niewielkiego zestawu filmów
critics = {'Lisa Rose': {'Kobieta w błękitnej wodzie': 2.5, 'Węże w samolocie': 3.5, 'Całe szczęście': 3.0,
                         'Superman: Powrót': 3.5, 'Ja, ty i on': 2.5, 'Nocny słuchacz': 3.0},
           'Gene Seymour': {'Kobieta w błękitnej wodzie': 3.0, 'Węże w samolocie': 3.5, 'Całe szczęście': 1.5,
                         'Superman: Powrót': 5.0, 'Ja, ty i on': 3.5, 'Nocny słuchacz': 3.0},
           'Michael Phillips': {'Kobieta w błękitnej wodzie': 2.5, 'Węże w samolocie': 3.0,
                         'Superman: Powrót': 3.5, 'Nocny słuchacz': 4.0},
           'Claudia Puig': {'Węże w samolocie': 3.5, 'Całe szczęście': 3.0,
                         'Superman: Powrót': 4.0, 'Ja, ty i on': 2.5, 'Nocny słuchacz': 4.5},
           'Mick LaSalle': {'Kobieta w błękitnej wodzie': 3.0, 'Węże w samolocie': 4.0, 'Całe szczęście': 2.0,
                         'Superman: Powrót': 3.0, 'Ja, ty i on': 2.0, 'Nocny słuchacz': 3.0},
           'Jack Matthews': {'Kobieta w błękitnej wodzie': 3.0, 'Węże w samolocie': 4.0,
                         'Superman: Powrót': 5.0, 'Ja, ty i on': 3.5, 'Nocny słuchacz': 3.0},
           'Toby': {'Węże w samolocie': 4.5, 'Superman: Powrót': 4.0, 'Ja, ty i on': 1.0}
            }

# @profile
def pearson(prefs, pos1, pos2):
    # We can compare only same positions in both objects, so lets gather intersection info
    # c1 = [x for x in prefs[pos1].keys()]
    # c2 = [x for x in prefs[pos2].keys()]
    # inter = set(c1).intersection(c2)
    # inter = [item for item in c1 if item in c2]
    # inter = list(set(c1) & set(c2))
    # inter = list(filter(lambda x: x in c1, c2))
    # inter = list(filter(set(c1).__contains__, sublist))
    inter = {}

    # for item in c1:
    #     if item in c2:
    #         inter.append(item)
    # print(type(pos1), pos1, type(pos2), pos2)
    for item in prefs[pos1]:
        if item in prefs[pos2]:
            inter.setdefault(item)

    n = float(len(inter))

    # subcalculations for Pearson correlation coefficient
    sum12 = sum(prefs[pos1][item] * prefs[pos2][item] for item in inter)
    sum1 = sum(prefs[pos1][item] for item in inter)
    sum2 = sum(prefs[pos2][item] for item in inter)

    pow1 = sum(pow(prefs[pos1][item], 2) for item in inter)
    pow2 = sum(pow(prefs[pos2][item], 2) for item in inter)

    num = n*sum12 - sum1*sum2
    den = sqrt((n*pow1 - pow(sum1, 2)) * (n*pow2 - pow(sum2, 2)))
    # print('sum12:{0} sum1:{1} sum2:{2} pow1:{3} pow2:{4} num:{5} den:{6}'.format(sum12, sum1, sum2, pow1, pow2, num, den))
    if den == 0: return 0.0
    r = round(num / den, 6)
    return r

def pearson_numpy(prefs, pos1, pos2):

    inter = [item for item in prefs[pos1] if item in prefs[pos2]]

    x = [prefs[pos1][item] for item in inter]
    y = [prefs[pos2][item] for item in inter]

    r = np.corrcoef(x=x, y=y)

    return round(r[0][1], 6)

def get_intersection(prefs, pos1, pos2):

    inter = [item for item in prefs[pos1] if item in prefs[pos2]]
    # sorted_dict = dict(sorted(unsorted_dict.items()))

    return inter

def pearson_cuda(inter, pos1, pos2):
    for pos in inter:
        pass
    # subcalculations for Pearson correlation coefficient
    sum12 = sum(prefs[pos1][item] * prefs[pos2][item] for item in inter)
    sum1 = sum(prefs[pos1][item] for item in inter)
    sum2 = sum(prefs[pos2][item] for item in inter)

    pow1 = sum(pow(prefs[pos1][item], 2) for item in inter)
    pow2 = sum(pow(prefs[pos2][item], 2) for item in inter)

    num = n*sum12 - sum1*sum2
    den = sqrt((n*pow1 - pow(sum1, 2)) * (n*pow2 - pow(sum2, 2)))
    # print('sum12:{0} sum1:{1} sum2:{2} pow1:{3} pow2:{4} num:{5} den:{6}'.format(sum12, sum1, sum2, pow1, pow2, num, den))
    if den == 0: return 0.0
    r = round(num / den, 6)
    return r