import unittest
from nba_crawler.NBADataCrawler import getNumberOfGamesAtOneDay,getTeamsPlayingAtOneDay,getURLForOneMatchData,getMatchScoreFromURL

class TestNBADataCrawler(unittest.TestCase):
    def testGetNumberOfGamesAtOneDay(self):
        result=getNumberOfGamesAtOneDay('20151026')
        self.assertEqual(result,0)
        result=getNumberOfGamesAtOneDay('20151220')
        self.assertEqual(result,7)

    def testGetTeamsPlayingAtOneDay(self):
        result=getTeamsPlayingAtOneDay('20151025')
        self.assertEqual(result,[])
        result=getTeamsPlayingAtOneDay('20160302')
        self.assertEqual(result,[{'home_team': 'ORL', 'away_team': 'CHI'}, {'home_team': 'PHI', 'away_team': 'CHA'}, {'home_team': 'BOS', 'away_team': 'POR'}, {'home_team': 'TOR', 'away_team': 'UTA'}, {'home_team': 'HOU', 'away_team': 'NOP'}, {'home_team': 'MEM', 'away_team': 'SAC'}, {'home_team': 'MIL', 'away_team': 'IND'}, {'home_team': 'MIN', 'away_team': 'WAS'}, {'home_team': 'SAS', 'away_team': 'DET'}, {'home_team': 'DEN', 'away_team': 'LAL'}])

    def testGetURLForOneMatchData(self):
        result=getURLForOneMatchData('20160203','CLE','CHA')
        self.assertEqual(result,'http://www.nba.com/games/20160203/CLECHA/gameinfo.html')
        result=getURLForOneMatchData('20151203','SAS','MEM')
        self.assertEqual(result,'http://www.nba.com/games/20151203/SASMEM/gameinfo.html')

    def testGetMatchScoreFromURL(self):
        result=getMatchScoreFromURL('http://www.nba.com/games/20151203/SASMEM/gameinfo.html')
        self.assertEqual(result,{'away_team':103,'home_team':83})
        result=getMatchScoreFromURL('http://www.nba.com/games/20160211/WASMIL/gameinfo.html')
        self.assertEqual(result,{'away_team':92,'home_team':99})