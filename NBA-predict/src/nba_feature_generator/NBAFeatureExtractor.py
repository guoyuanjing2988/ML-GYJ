import pickle
import os
all_player_pickle_dir=os.path.join(os.path.dirname(os.path.dirname(__file__)),'nba_crawler','player_names.pickle')

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