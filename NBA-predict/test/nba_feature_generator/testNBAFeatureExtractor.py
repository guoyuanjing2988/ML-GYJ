import unittest
from nba_feature_generator.NBAFeatureExtractor import generateVectorForPlayersInOneTeam,generateVectorForOneTeamName,generateVectorForOneMatch

class TestNBAFeatureExtractor(unittest.TestCase):
    def testGenerateVectorForPlayersInOneTeam(self):
        result=generateVectorForPlayersInOneTeam(['kawhi_leonard', 'lamarcus_aldridge', 'tim_duncan', 'daniel_green', 'tony_parker', 'emanuel_ginobili', 'boris_diaw', 'kyle_anderson', 'patrick_mills', 'david_west', 'jonathon_simmons', 'matt_bonner', 'boban_marjanovic'])
        self.assertEqual(result[270],0)

    def testGenerateVectorForOneTeamName(self):
        result=generateVectorForOneTeamName('CLE')
        self.assertEqual(result[20],1)
        self.assertEqual(sum(result),1)

    def testGenerateVectorForOneMatch(self):
        match={'away_team':'SAS','home_team':'MEM','away_team_players': ['kawhi_leonard', 'lamarcus_aldridge', 'tim_duncan', 'daniel_green', 'tony_parker', 'emanuel_ginobili', 'boris_diaw', 'kyle_anderson', 'patrick_mills', 'david_west', 'jonathon_simmons', 'matt_bonner', 'boban_marjanovic'], 'home_team_players': ['jeff_green', 'zach_randolph', 'marc_gasol', 'tony_allen', 'mike_conley', 'matt_barnes', 'courtney_lee', 'jamychal_green', 'mario_chalmers', 'vince_carter', 'james_ennis', 'russ_smith', 'brandan_wright']}
        result=generateVectorForOneMatch(match=match)
        self.assertEqual(len(result),1016)
