import unittest
from nba_feature_generator.NBAFeatureExtractor import generateVectorForOneMatch
from nba_model_trainer.NBAScoreDifferenceClassifier import predict

class TestNBAScoreDifferenceClassifier(unittest.TestCase):

    def testPredict(self):
        match = {'away_team': 'SAS', 'home_team': 'MEM',
                 'away_team_players': ['kawhi_leonard', 'lamarcus_aldridge', 'tim_duncan', 'daniel_green',
                                       'tony_parker', 'emanuel_ginobili', 'boris_diaw', 'kyle_anderson',
                                       'patrick_mills', 'david_west', 'jonathon_simmons', 'matt_bonner',
                                       'boban_marjanovic'],
                 'home_team_players': ['jeff_green', 'zach_randolph', 'marc_gasol', 'tony_allen', 'mike_conley',
                                       'matt_barnes', 'courtney_lee', 'jamychal_green', 'mario_chalmers',
                                       'vince_carter', 'james_ennis', 'russ_smith', 'brandan_wright']}
        match_vector=generateVectorForOneMatch(match=match)
        result=predict(match_vector)
        print(result)
        self.assertIsNotNone(result)