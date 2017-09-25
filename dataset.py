import pandas as pd

def loadImdbData(file):
    f = pd.read_csv(filepath_or_buffer=file, sep=',')
    currentUser = {}
    for x in f[['Title', 'You rated']].values:
        currentUser[x[0]] = x[1]/2

    print(currentUser)
    # print(type(f))
    # print(f)
    # print(f.head(5))