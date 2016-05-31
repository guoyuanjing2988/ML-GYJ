import pandas
import os
import pickle
import unittest
from users.pretreatment import get_users_vector
from jobs.pretreatment import get_jobs_vector
data_dir=os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))),'data')
#data_dir=os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))),'media','data','i316981','recsys')
#data_dir=os.path.join(os.pardir,os.pardir,os.pardir,os.pardir,os.pardir,'media','data','i316981','recsys')
print(data_dir)
class TestInput(unittest.TestCase):

    def test_user_input(self):
        users_data=pandas.read_csv(os.path.join(data_dir,'users.csv'),sep='	')
        print(type(users_data))
        print(users_data.columns.tolist())
        print(users_data.shape)
        users_modified = get_users_vector(users_data)
        with open('users_information.pickle', 'wb') as f:
            pickle.dump(users_modified, f)
        self.assertIsNotNone(users_modified)

    def test_jobs_input(self):
        jobs_data = pandas.read_csv(os.path.join(data_dir, 'items.csv'), sep='	')
        jobs_modified = get_jobs_vector(jobs_data)
        with open('jobs_information.pickle', 'wb') as f:
            pickle.dump(jobs_modified, f)
        self.assertIsNotNone(jobs_modified)

    def test_interactions_input(self):
        interactions_data = pandas.read_csv(os.path.join(data_dir, 'interactions.csv'), sep='	')
        print(interactions_data.shape)
        n,m=interactions_data.shape
        columns=interactions_data.columns.tolist()
        nn=0
        has3=0
        previous=-1
        isnull=interactions_data.isnull()
        total3=0
        f=False
        for i in range(n):
            ff=True
            for j in range(m):
                if isnull.iloc[i][columns[j]]==True:
                    ff=False
                    break
            if ff==True:
                id=int(interactions_data.iloc[i][columns[0]])
                rec=int(interactions_data.iloc[i][columns[2]])
                if id!=previous:
                    previous=id
                    nn+=1
                    f=False
                if (rec==3):
                    total3+=1
                    if f==False:
                        has3+=1
                        f=True
        print('Total Candidates:',nn)
        print('Candidates with 3:',has3)
        print('Total 3 Recommendations:',total3)








