def get_preprocess(data):
    n, m = data.shape
    columns = data.columns.tolist()
    nn = 0
    has3 = 0
    previous = -1
    isnull = data.isnull()
    total3 = 0
    f = False
    interactions_modified = []
    temp = []
    for i in range(n):
        ff = True
        for j in range(m):
            if isnull.iloc[i][columns[j]] == True:
                ff = False
                break
        if ff == True:
            id = int(data.iloc[i][columns[0]])
            rec = int(data.iloc[i][columns[2]])
            if id != previous:
                if f == True:
                    interactions_modified.append([previous, temp])
                previous = id
                temp = []
                nn += 1
                f = False
            else:
                temp.append([data.iloc[i][columns[1]], data.iloc[i][columns[2]],
                             data.iloc[i][columns[3]]])
            if (rec == 3):
                total3 += 1
                if f == False:
                    has3 += 1
                    f = True
    print('Total Candidates:', nn)
    print('Candidates with 3:', has3)
    print('Total 3 Recommendations:', total3)
    return interactions_modified
