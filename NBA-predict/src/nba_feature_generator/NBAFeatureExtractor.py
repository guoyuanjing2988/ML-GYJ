import pickle
import os
from nba_crawler.NBADataCrawler import getAllTeamNames
all_player_pickle_dir=os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),'pickle_files','player_names.pickle')
all_match_pickle_dir=os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),'pickle_files','nba_matches.pickle')
all_teams=getAllTeamNames()

def generateVectorForPlayersInOneTeam(players):
    all_players=pickle.load(open(all_player_pickle_dir,'rb'))
    vector=[]
    for player in all_players:
        try:
            players.index(player)
            vector.append(1)
        except:
            vector.append(0)
    return vector

def generateVectorForOneTeamName(team_name):
    vector=[]
    for team in all_teams:
        if team==team_name:
            vector.append(1)
        else:
            vector.append(0)
    return vector

def generateVectorForOneMatch(matches=[],i=0,match=None):
    if match==None:
        match = matches[i]
    vector=generateVectorForOneTeamName(match['home_team'])+generateVectorForOneTeamName(match['away_team'])+generateVectorForPlayersInOneTeam(match['home_team_players'])+generateVectorForPlayersInOneTeam(match['away_team_players'])
    return vector

def refreshVectorForAllMatches():
    matches=pickle.load(open(all_match_pickle_dir,'rb'))
    inp_vector=[]
    outp_vector=[]
    for i in range(len(matches)):
        inp_vector.append(generateVectorForOneMatch(matches,i))
        outp_vector.append([matches[i]['home_team_score'],matches[i]['away_team_score']])
    f=open(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),'pickle_files','matches_vector.pickle'),'wb')
    pickle.dump(inp_vector,f)
    pickle.dump(outp_vector,f)
    f.close()

if __name__=='__main__':
    refreshVectorForAllMatches()