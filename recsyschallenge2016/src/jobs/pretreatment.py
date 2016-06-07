from users.pretreatment import get_country_code
from users.pretreatment import returnbyte
from users.pretreatment import getwholelist
def get_jobs_vector(data):
    print('Start Jobs')
    columns = data.columns.tolist()
    isnull = data.isnull()
    n, m = data.shape
    jobs_temp = []
    for i in range(n):
        temp = []
        for j in range(m):
            if isnull.iloc[i][columns[j]] != True:
                if data.iloc[i][columns[j]] == 'NULL':
                    temp.append(0)
                elif j != 5:
                    temp.append(data.iloc[i][columns[j]])
                else:
                    temp.append(get_country_code(data.iloc[i][columns[j]]))
            else:
                temp.append(0)
        if temp[len(temp)-1]==1:
            jobs_temp.append(temp)
    jobs_modified = []
    whole = [[]] * m
    for i in range(m - 1):
        if (i!=6) and (i!=7):
            print(i)
            whole[i + 1] = getwholelist(jobs_temp[i + 1], i + 1)
    print('Step 1')
    print(whole[2])
    for i in range(len(jobs_temp)):
        temp = []
        for j in range(m):
            if j==0:
                temp.append(int(jobs_temp[i][j]))
            elif (j==7) or (j==8):
                pass
            else:
                temp = temp + returnbyte(whole[j], jobs_temp[i][j])
        jobs_modified.append(temp)
    print('Step 2')
    return jobs_modified