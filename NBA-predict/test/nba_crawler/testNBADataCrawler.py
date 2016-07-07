import unittest
from nba_crawler.NBADataCrawler import getNumberOfGamesAtOneDay,getTeamsPlayingAtOneDay,getURLForOneMatchData,getMatchScoreFromURL,getHealthyPlayersFromURL

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
        self.assertEqual(result,[{'home_team': 'ORL', 'away_team': 'CHI'}, {'home_team': 'PHI', 'away_team': 'CHA'}, {'home_team': 'BOS', 'away_team': 'POR'}, {'home_team': 'TOR', 'away_team': 'UTA'}, {'home_team': 'HOU', 'away_team': 'NOP'}, {'home_team': 'MEM', 'away_team': 'SAC'}, {'home_team': 'MIL', 'away_team': 'IND'}, {'home_team': 'MIN', 'away_team': 'WAS'}, {'home_team': 'SAS', 'away_team': 'DET'}, {'home_team': 'DEN', 'away_team': 'LAL'}, {'away_team': 'OKC', 'home_team': 'LAC'}])

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

    def testGetHealthyPlayersFromURL(self):
        result = getHealthyPlayersFromURL('http://www.nba.com/games/20151203/SASMEM/gameinfo.html')
        self.assertEqual(result, {'away_team': ['kawhi_leonard', 'lamarcus_aldridge', 'tim_duncan', 'daniel_green', 'tony_parker', 'emanuel_ginobili', 'boris_diaw', 'kyle_anderson', 'patrick_mills', 'david_west', 'jonathon_simmons', 'matt_bonner', 'boban_marjanovic'], 'home_team': ['jeff_green', 'zach_randolph', 'marc_gasol', 'tony_allen', 'mike_conley', 'matt_barnes', 'courtney_lee', 'jamychal_green', 'mario_chalmers', 'vince_carter', 'james_ennis', 'russ_smith', 'brandan_wright']})
        result = getHealthyPlayersFromURL('http://www.nba.com/games/20160211/WASMIL/gameinfo.html')
        self.assertEqual(result, {'away_team': ['otto_porter', 'jared_dudley', 'marcin_gortat', 'bradley_beal', 'john_wall', 'nene', 'garrett_temple', 'ramon_sessions', 'kelly_oubre', 'drew_gooden', 'dejuan_blair', 'jarell_eddie'], 'home_team': ['giannis_antetokounmpo', 'jabari_parker', 'miles_plumlee', 'khris_middleton', 'oj_mayo', 'greg_monroe', 'michael_carter-williams', 'jerryd_bayless', 'rashad_vaughn', 'chris_copeland', 'tyler_ennis', 'john_henson', 'johnny_obryant']})
