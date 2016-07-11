import unittest
from nba_feature_generator.NBAFeatureExtractor import generateVectorForPlayersInOneTeam,generateVectorForOneTeamName

class TestNBAFeatureExtractor(unittest.TestCase):
    def testGenerateVectorForPlayersInOneTeam(self):
        result=generateVectorForPlayersInOneTeam(['kawhi_leonard', 'lamarcus_aldridge', 'tim_duncan', 'daniel_green', 'tony_parker', 'emanuel_ginobili', 'boris_diaw', 'kyle_anderson', 'patrick_mills', 'david_west', 'jonathon_simmons', 'matt_bonner', 'boban_marjanovic'])
        self.assertEqual(result[270],0)

    def testGenerateVectorForOneTeamName(self):
        result=generateVectorForOneTeamName('CLE')
        self.assertEqual(result[20],1)
        self.assertEqual(sum(result),1)