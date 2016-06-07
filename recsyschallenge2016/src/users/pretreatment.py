import numpy
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

def returnbyte(whole,inform):
    if type(inform)==str:
        s=inform.split(',')
    else:
        s=[inform]
    a=[]
    for i in range(len(whole)):
        f=False
        for j in range(len(s)):
            if s[j]==whole[i]:
                f=True
                break
        if f==True:
            a.append(1)
        else:
            a.append(0)
    return a

def getwholelist(data,k):
    a = []
    for i in range(len(data)):
        s = data[i]
        if s!=0:
            if type(s)!=str:
                s=[s]
            else:
                s=s.split()
            for j in range(len(s)):
                ff = True
                for k in range(len(a)):
                    if a[k] == s[j]:
                        ff = False
                        break
                if ff == True:
                    a.append(s[j])
    return a

def get_users_vector(data):
    import copy
    print('Start Users')
    columns = data.columns.tolist()
    isnull=data.isnull()
    n, m = data.shape
    users_temp = []
    for i in range(n):
        temp = []
        for j in range(m):
            if isnull.iloc[i][columns[j]]!=True:
                if data.iloc[i][columns[j]] == 'NULL':
                    temp.append(0)
                elif j!=5:
                    temp.append(data.iloc[i][columns[j]])
                else:
                    temp.append(get_country_code(data.iloc[i][columns[j]]))
            else:
                temp.append(0)
        users_temp.append(temp)
    print('Step 1')
    users_modified = []
    whole=[[]]*m
    for i in range(m-1):
        print(i)
        whole[i+1]=copy.deepcopy(getwholelist([row[i+1] for row in users_temp],i+1))
    print(whole[2])
    for i in range(n):
        temp = []
        for j in range(m):
            if (j==0):
                temp.append(int(users_temp[i][j]))
            else:
                temp=temp+returnbyte(whole[j],users_temp[i][j])

        users_modified.append(temp)
    print('Step 2')
    return users_modified
