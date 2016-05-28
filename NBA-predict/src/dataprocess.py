import pandas
import os
from datetime import date as dateclass

def get_date_from_excel(date):
    s=str(date).split()[0]
    s=s.split('-')
    a=[int(s[1]),int(s[2]),int(s[0])]
    return a


def get_all_names(data):
    isnull=data.isnull()
    names=[]
    n,m=data.shape
    for i in range(n):
        for j in range(13):
            s='Player'+str(j+1)
            if isnull.iloc[i][s]!=True:
                f=True
                for k in range(len(names)):
                    if names[k]==data.iloc[i][s]:
                        f=False
                        break
                if f==True:
                    names.append(data.iloc[i][s])
    return names


def get_name_vector(data,players,all_name):
    vector=[0]*len(all_name)
    for i in range(len(all_name)):
        for j in range(len(players)):
            if players[j]==all_name[i]:
                vector[i]=1
                break
    return vector


def get_wins(data,team,n):
    win=0
    game=0
    for i in range(n,0,-1):
        if data.iloc[i]['Team']==team:
            game+=1
            if i%2==0:
                score1=int(data.iloc[i]['Score'])
                score2=int(data.iloc[i+1]['Score'])
            else:
                score1 = int(data.iloc[i]['Score'])
                score2 = int(data.iloc[i-1]['Score'])
            if score1>score2:
                win+=1
            if game==10:
                break
    if game==10:
        return win
    else:
        return -1

def last_game(data,team,date,n):
    interval=-1
    for i in range(n, 0, -1):
        if data.iloc[i]['Team']==team:
            thatdate=get_date_from_excel(data.iloc[i]['Date'])
            d0=dateclass(thatdate[2],thatdate[0],thatdate[1])
            d1=dateclass(date[2],date[0],date[1])
            delta=d1-d0
            interval=delta.days
            break
    return interval

def games_in_last_seven_days(data,team,date,n):
    games=0
    for i in range(n, 0, -1):
        thatdate = get_date_from_excel(data.iloc[i]['Date'])
        d0 = dateclass(thatdate[2], thatdate[0], thatdate[1])
        d1 = dateclass(date[2], date[0], date[1])
        delta = d1 - d0
        interval = delta.days
        if interval>7:
            break
        if data.iloc[i]['Team'] == team:
            games+=1
    return games

def games_in_visiting_field(data,team,n):
    games=0
    for i in range(n,0,-1):
        if data.iloc[i]['Team']==team:
            if i%2==0:
                break
            else:
                games+=1
    return games

def number_overtimes(data,team,n):
    for i in range(n, 0, -1):
        if data.iloc[i]['Team'] == team:
            return int(data.iloc[i]['Overtime'])
    return -1

def get_last_ten_score(data,team,n):
    score=[]
    for i in range(n, 0, -1):
        if data.iloc[i]['Team'] == team:
            score.append(data.iloc[i]['Score'])
            if len(score)==10:
                break
    return score

def get_vector(data,team,players,date,n,all_name):
    vector=get_name_vector(data,players,all_name)
    if get_wins(data,team,n)==-1:
        return None
    vector.append(get_wins(data,team,n))
    vector.append(last_game(data,team,date,n))
    vector.append(games_in_last_seven_days(data,team,date,n))
    vector.append(games_in_visiting_field(data,team,n))
    vector.append(number_overtimes(data,team,n))
    score=get_last_ten_score(data,team,n)
    for i in range(len(score)):
        vector.append(score[i])
    return vector

