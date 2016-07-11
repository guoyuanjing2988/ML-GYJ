from util.http_util import readContentFromURL
import datetime
import pickle
import logging
import os
nba_gameline_url='http://www.nba.com/gameline/'
logging.basicConfig(level=logging.INFO , format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger=logging.getLogger('nba_crawler')

def getNumberOfGamesAtOneDay(game_date):
    url_at_game_date=nba_gameline_url+game_date+'/'
    website_content=readContentFromURL(url_at_game_date)
    prev_loc=0
    number_of_games=0
    while website_content.find('<div id="nbaGL00215',prev_loc)!=-1:
        number_of_games+=1
        prev_loc=website_content.find('<div id="nbaGL00215',prev_loc)+1
    return number_of_games

def getTeamsPlayingAtOneDay(game_date):
    url_at_game_date = nba_gameline_url + game_date + '/'
    website_content = readContentFromURL(url_at_game_date)
    prev_loc = 0
    teams_playing=[]
    while website_content.find('<div id="nbaGL00215', prev_loc) != -1:
        away_team_loc = website_content.find('<h5 class="nbaModTopTeamName awayteam">', prev_loc)
        teams_playing.append({})
        teams_playing[-1]['away_team']=website_content[away_team_loc+39:away_team_loc+42]
        home_team_loc = website_content.find('<h5 class="nbaModTopTeamName hometeam">', prev_loc)
        teams_playing[-1]['home_team']=website_content[home_team_loc+39:home_team_loc+42]
        prev_loc = home_team_loc+1
    i=0
    while (i<len(teams_playing)-1):
        if teams_playing[i]['home_team']==teams_playing[i+1]['home_team']:
            del(teams_playing[i])
        else:
            i+=1
    return teams_playing

def getURLForOneMatchData(game_date,away_team,home_team):
    return 'http://www.nba.com/games/'+game_date+'/'+away_team+home_team+'/gameinfo.html'

def _getScoreFromPosition(website_content,location):
    score_end_location = website_content.find('<', location + 1)
    if website_content[location+20]!='"':
        try:
            return int(website_content[location+25:score_end_location])
        except:
            return -1
    else:
        try:
            return int(website_content[location+22:score_end_location])
        except:
            return -1

def getMatchScoreFromURL(match_url):
    website_content = readContentFromURL(match_url)
    away_team_loc=website_content.find('<h2 class="teamAway')
    score={}
    score['away_team']=_getScoreFromPosition(website_content,away_team_loc)
    home_team_loc=website_content.find('<h2 class="teamHome')
    score['home_team']=_getScoreFromPosition(website_content,home_team_loc)
    return score

def _getColumnInformation(row_html):
    row=[]
    prev=0
    while row_html.find('<td',prev)!=-1:
        column_start=row_html.find('<td',prev)
        column_end=row_html.find('</td>',prev)
        row.append(row_html[column_start+4:column_end])
        prev=column_end+1
    return row

def _getTableInformation(players_table_html):
    table = []
    prev = 0
    while players_table_html.find('<tr', prev) != -1:
        table_row_start = players_table_html.find('<tr', prev)
        table_row_end = players_table_html.find('</tr>', table_row_start)
        table.append(_getColumnInformation(players_table_html[table_row_start:table_row_end]))
        prev = table_row_end + 1
    return table

def _getHealthPlayersFromHTML(players_table_html):
    table=_getTableInformation(players_table_html)
    health_players=[]
    for i in range(3,len(table)):
        player_name_start=table[i][0].find('<a href="/playerfile/')
        if player_name_start==-1:
            break
        player_name_end=table[i][0].find('/index.html')
        player_name=table[i][0][player_name_start+21:player_name_end]
        if len(table[i][0])>2:
            health_players.append(player_name)
        else:
            if table[i][1].find("DNP - Coach's Decision")!=-1:
                health_players.append(player_name)
    return health_players

def getHealthyPlayersFromURL(match_url):
    website_content = readContentFromURL(match_url)
    players={}
    away_team_loc_start=website_content.find('<table id="nbaGITeamStats"')
    away_team_loc_end=website_content.find('</table>',away_team_loc_start)
    players['away_team']=_getHealthPlayersFromHTML(website_content[away_team_loc_start:away_team_loc_end])
    home_team_loc_start=website_content.find('<table id="nbaGITeamStats"',away_team_loc_end)
    home_team_loc_end=website_content.find('</table>',home_team_loc_start)
    players['home_team']=_getHealthPlayersFromHTML(website_content[home_team_loc_start:home_team_loc_end])
    return players

def _filltwoposition(intx):
    if intx<10:
        return '0'+str(intx)
    else:
        return str(intx)

def getAllMatches(start_date,end_date):
    matches=[]
    for deltadate in range((end_date-start_date).days+1):
        date_string=str((start_date+datetime.timedelta(deltadate)).year)+_filltwoposition((start_date+datetime.timedelta(deltadate)).month)+_filltwoposition((start_date+datetime.timedelta(deltadate)).day)
        print(start_date+datetime.timedelta(deltadate))
        teams_playing=getTeamsPlayingAtOneDay(date_string)
        for i in range(len(teams_playing)):
            matches.append({})
            matches[-1]['home_team']=teams_playing[i]['home_team']
            matches[-1]['away_team']=teams_playing[i]['away_team']
            matches[-1]['year']=int(date_string[:4])
            matches[-1]['month']=int(date_string[4:6])
            matches[-1]['day']=int(date_string[6:8])
            score=getMatchScoreFromURL(getURLForOneMatchData(date_string,teams_playing[i]['away_team'],teams_playing[i]['home_team']))
            matches[-1]['home_team_score']=score['home_team']
            matches[-1]['away_team_score']=score['away_team']
            players=getHealthyPlayersFromURL(getURLForOneMatchData(date_string,teams_playing[i]['away_team'],teams_playing[i]['home_team']))
            matches[-1]['home_team_players']=players['home_team']
            matches[-1]['away_team_players']=players['away_team']
            if score['home_team']==-1 or score['away_team']==-1:
                del(matches[-1])
    return matches


def refreshNBADataPickle():
    matches=getAllMatches(datetime.date(year=2015,month=10,day=27),datetime.date(year=2016,month=6,day=19))
    pickle.dump(matches,open(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),'pickle_files','nba_matches.pickle'),'wb'))

def getAllTeamNames():
    matches = pickle.load(open(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),'pickle_files','nba_matches.pickle'), 'rb'))
    team_names=[]
    for match in matches:
        try:
            team_names.index(match['home_team'])
        except:
            team_names.append(match['home_team'])
    return team_names

def refreshAllPlayerNames():
    matches=pickle.load(open(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),'pickle_files','nba_matches.pickle'),'rb'))
    player_names=[]
    for match in matches:
        for player in match['home_team_players']:
            try:
                player_names.index(player)
            except:
                player_names.append(player)
        for player in match['away_team_players']:
            try:
                player_names.index(player)
            except:
                player_names.append(player)
    logger.info('player number:'+str(len(player_names)))
    pickle.dump(player_names,open(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),'pickle_files','player_names.pickle'),'wb'))

if __name__=='__main__':
    refreshNBADataPickle()
    refreshAllPlayerNames()


