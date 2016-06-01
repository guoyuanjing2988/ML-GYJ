import copy
def get_job_traininginput(jobs,id):
    l = 0
    r = len(jobs)-1
    k = -1
    while l <= r:
        m = (l + r) // 2
        if jobs[m][0] == id:
            k = m
            break
        elif jobs[m][0] < id:
            l = m + 1
        else:
            r = m - 1
    if k == -1:
        return -1
    else:
        return copy.deepcopy(jobs[k][1:])