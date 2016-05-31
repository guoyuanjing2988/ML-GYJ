import pandas
import os
import pickle
from users.pretreatment import get_users_vector
from jobs.pretreatment import get_jobs_vector
#data_dir=os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))),'PycharmProjects','Yuanjing','recsys','data')
#data_dir=os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))),'media','data','i316981','recsys')
data_dir=os.path.join(os.pardir,os.pardir,os.pardir,os.pardir,os.pardir,'media','data','i316981','recsys')
print(data_dir)
users_data=pandas.read_csv(os.path.join(data_dir,'users.csv'),sep='	')
print(type(users_data))
print(users_data.columns.tolist())
print(users_data.shape)
interactions_data=pandas.read_csv(os.path.join(data_dir,'interactions.csv'),sep='	')
print(interactions_data.shape)
users_modified=get_users_vector(users_data)
with open('users_information.pickle','wb') as f:
    pickle.dump(users_modified,f)
jobs_data=pandas.read_csv(os.path.join(data_dir,'items.csv'),sep='	')
jobs_modified=get_jobs_vector(jobs_data)
with open('jobs_information.pickle','wb') as f:
    pickle.dump(users_modified,f)
