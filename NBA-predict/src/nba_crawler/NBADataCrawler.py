from util.http_util import readContentFromURL

nba_gameline_url='http://www.nba.com/gameline/'
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
        prev_loc = website_content.find('<div id="nbaGL00215', home_team_loc) + 1
    return teams_playing

def getURLForOneMatchData(game_date,away_team,home_team):
    return 'http://www.nba.com/games/'+game_date+'/'+away_team+home_team+'/gameinfo.html'

def _getScoreFromPosition(website_content,location):
    score_end_location = website_content.find('<', location + 1)
    if website_content[location+20]!='"':
        return int(website_content[location+25:score_end_location])
    else:
        return int(website_content[location+22:score_end_location])

def getMatchScoreFromURL(match_url):
    website_content = readContentFromURL(match_url)
    away_team_loc=website_content.find('<h2 class="teamAway')
    score={}
    score['away_team']=_getScoreFromPosition(website_content,away_team_loc)
    home_team_loc=website_content.find('<h2 class="teamHome')
    score['home_team']=_getScoreFromPosition(website_content,home_team_loc)
    return score