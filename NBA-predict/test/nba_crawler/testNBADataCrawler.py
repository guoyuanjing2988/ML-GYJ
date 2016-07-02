import unittest
from nba_crawler.NBADataCrawler import getNumberOfGamesAtOneDay,getTeamsPlayingAtOneDay

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
