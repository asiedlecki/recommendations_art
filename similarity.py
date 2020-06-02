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
    print("Calc similarity for {0} and {1}".format(pos1, pos2))
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
            print("{0} watched both movies".format(item))
            inter.setdefault(item)

    n = float(len(inter))
    print("Count of users that watched both movies: {0}".format(n))

    # subcalculations for Pearson correlation coefficient
    sum12 = sum(prefs[pos1][item] * prefs[pos2][item] for item in inter)
    print("Subcalculations for {}, {}, {}".format(sum12, inter))
    sum1 = sum(prefs[pos1][item] for item in inter)
    print("Subcalculations for {}, {}, {}".format(sum1, inter))
    sum2 = sum(prefs[pos2][item] for item in inter)
    print("Subcalculations for {}, {}, {}".format(sum2, inter))

    pow1 = sum(pow(prefs[pos1][item], 2) for item in inter)
    print("Power {} for {}".format(pow1, inter))
    pow2 = sum(pow(prefs[pos2][item], 2) for item in inter)
    print("Power {} for {}".format(pow2, inter))

    num = n*sum12 - sum1*sum2
    print("{num} = {n} * {sum12} - {sum1} * {sum2}".format(num=num, n=n, sum1=sum1, sum2=sum2))
    den = sqrt((n*pow1 - pow(sum1, 2)) * (n*pow2 - pow(sum2, 2)))
    print("{den} = sqrt(({n}*{pow1} - pow({sum1}, 2)) * ({n}*{pow2} - pow({sum2}, 2)))".format(den=den, n=n, pow1=pow1,
                                                                                               sum1=sum1, pow2=pow2, sum2=sum2))
    # print('sum12:{0} sum1:{1} sum2:{2} pow1:{3} pow2:{4} num:{5} den:{6}'.format(sum12, sum1, sum2, pow1, pow2, num, den))
    if den == 0: return 0.0
    r = num / den
    return round(r, 6)

def pearson_numpy(prefs, pos1, pos2):

    inter = [item for item in prefs[pos1] if item in prefs[pos2]]

    x = [prefs[pos1][item] for item in inter]
    y = [prefs[pos2][item] for item in inter]

    r = (np.corrcoef(x=x, y=y)+1) / 2 # add 1 and divide by 2 to get values between <0, 1>

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
    r = num / den
    return round(r, 6)


# zwracanie miary podobieństwa opartej na odległości euklidesowej dla pozycji person1 i person2
def euclidean(prefs, person1, person2):
    # pobieranie listy wspólnych pozycji
    si={}
    for item in prefs[person1]:
        if item in prefs[person2]:
            si[item]=1
    # w przypadku braku wspólnych ocen zostanie zwrócona wartość 0
    if len(si) == 0: return 0
    # sumowanie kwadratów wszystkich różnic
    sum_of_squares = sum([pow(prefs[person1][item]-prefs[person2][item], 2)
                          for item in prefs[person1] if item in prefs[person2]])
    return 1/(1+sqrt(sum_of_squares)) # odwracamy by większa cyfra oznaczała większe podobieństwo (1 - identyczne)
    # w mianowniku dodano 1, by uniknąć dzielenia przez zero


def euclidean_numpy(prefs, pos1, pos2):
    inter = [item for item in prefs[pos1] if item in prefs[pos2]]

    if len(inter) == 0: return 0

    x = np.array([prefs[pos1][item] for item in inter])
    y = np.array([prefs[pos2][item] for item in inter])

    dist = np.linalg.norm(x - y)

    return round(1/(1+dist), 6)


def msd(prefs, person1, person2):
    # pobieranie listy wspólnych pozycji
    si={}
    for item in prefs[person1]:
        if item in prefs[person2]:
            si[item]=1
    # w przypadku braku wspólnych ocen zostanie zwrócona wartość 0
    n = len(si)
    if n == 0: return 0
    # sumowanie kwadratów wszystkich różnic
    sum_of_squares = sum([pow(prefs[person1][item]-prefs[person2][item], 2)
                          for item in prefs[person1] if item in prefs[person2]])
    return round(1/(1+1/n*sum_of_squares), 6) # odwracamy by większa cyfra oznaczała większe podobieństwo (1 - identyczne)
    # w mianowniku dodano 1, by uniknąć dzielenia przez zero