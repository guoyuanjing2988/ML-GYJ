from users.pretreatment import get_country_code
from users.pretreatment import cancel_comma
from users.pretreatment import get_maxn
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
                temp.append(data.iloc[i][columns[j]])
            else:
                temp.append(0)
        if temp[len(temp)-1]==1:
            jobs_temp.append(temp)
    max_len_1 = get_maxn(jobs_temp, 1)
    max_len_10=get_maxn(jobs_temp, 10)
    jobs_modified = []
    print('Step 1')
    for i in range(len(jobs_temp)):
        temp = []
        for j in range(m):
            if jobs_temp[i][j] == 0:
                temp.append(0)
            elif j == 1:
                temptemp = cancel_comma(jobs_temp[i][j], max_len_1)
                temp = temp + temptemp
            elif j == 5:
                temp.append(get_country_code(jobs_temp[i][5]))
            elif (j==7) or (j==8):
                pass
            elif (j==10):
                temptemp = cancel_comma(jobs_temp[i][j], max_len_10)
                temp = temp + temptemp
            elif jobs_temp[i][j] == 'NULL':
                temp.append(0)
            else:
                temp.append(int(jobs_temp[i][j]))
        jobs_modified.append(temp)
    print('Step 2')
    return jobs_modified