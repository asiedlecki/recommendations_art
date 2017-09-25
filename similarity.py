from math import pow, sqrt

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

def pearson(prefs, pos1, pos2):
    # We can compare only same positions in both objects, so lets gather intersection info
    inter = []

    for item in prefs[pos1]:
        if item in prefs[pos2]:
            inter.append(item)
    n = len(inter)

    # subcalculations for Pearson correlation coefficient
    sum12 = sum(prefs[pos1][item] * prefs[pos2][item] for item in inter)
    sum1 = sum(prefs[pos1][item] for item in inter)
    sum2 = sum(prefs[pos2][item] for item in inter)

    pow1 = sum(pow(prefs[pos1][item], 2) for item in inter)
    pow2 = sum(pow(prefs[pos2][item], 2) for item in inter)

    num = n*sum12 - sum1*sum2
    den = sqrt((n*pow1 - pow(sum1, 2)) * (n*pow2 - pow(sum2, 2)))

    if den == 0: return 0
    r = num / den
    return r