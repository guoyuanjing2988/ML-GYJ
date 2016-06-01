import copy
def get_user_traininginput(users,id):
    l=0
    r=len(users)-1
    k=-1
    while l<=r:
        m=(l+r)//2
        if users[m][0]==id:
            k=m
            break
        elif users[m][0]<id:
            l=m+1
        else:
            r=m-1
    if k==-1:
        raise ValueError('id not in users list')
    else:
        return copy.deepcopy(users[k][1:])