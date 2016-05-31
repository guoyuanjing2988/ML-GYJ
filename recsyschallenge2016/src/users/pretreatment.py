def get_country_code(s):
    country_names = ['de','at','ch','non_dach']
    for i in range(len(country_names)):
        if s==country_names[i]:
            return i+1
    raise ValueError('country name not in the list, your country name is:'+s)

def cancel_comma(s,maxn):
    s1=s.split(',')
    temp=[]
    for k in range(maxn):
        if k < len(s1):
            temp.append(int(s1[k]))
        else:
            temp.append(0)
    return temp

def get_maxn(a,k):
    max_len=0
    for i in range(len(a)):
        if a[i][k]!=0:
            s = a[i][k].split(',')
            if len(s)>max_len:
                max_len=len(s)
    return max_len


def get_users_vector(data):
    print('Start Users')
    columns = data.columns.tolist()
    isnull=data.isnull()
    n, m = data.shape
    users_temp = []
    for i in range(n):
        temp = []
        for j in range(m):
            if isnull.iloc[i][columns[j]]!=True:
                temp.append(data.iloc[i][columns[j]])
            else:
                temp.append(0)
        users_temp.append(temp)
    print('Step 1')
    max_len_1 = get_maxn(users_temp,1)
    max_len_11= get_maxn(users_temp,11)
    users_modified = []
    for i in range(n):
        temp = []
        for j in range(m):
            if users_temp[i][j]==0:
                temp.append(0)
            elif j == 1:
                temptemp=cancel_comma(users_temp[i][j],max_len_1)
                temp=temp+temptemp
            elif j == 5:
                temp.append(get_country_code(users_temp[i][5]))
            elif j==11:
                temptemp = cancel_comma(users_temp[i][j], max_len_11)
                temp=temp+temptemp
            elif users_temp[i][j]=='NULL':
                temp.append(0)
            else:
                temp.append(int(users_temp[i][j]))
        users_modified.append(temp)
    print('Step 2')
    return users_modified

