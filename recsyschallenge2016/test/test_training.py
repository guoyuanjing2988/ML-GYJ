import unittest
import os
import pickle
from users.traininginput import get_user_traininginput
from jobs.traininginput import get_job_traininginput

#pickle_dir=
class TestTrain(unittest.TestCase):

    def test_get_training_input(self):
        import numpy
        f=open('users_information.pickle','rb')
        users=pickle.load(f)
        f.close()
        f=open('jobs_information.pickle','rb')
        jobs=pickle.load(f)
        f.close()
        f=open('interactions_information.pickle','rb')
        interactions=pickle.load(f)
        users_useful=[]
        inp=[]
        outp=[]
        for i in range(len(interactions)):
            user_vector=get_user_traininginput(users,interactions[i][0])
            for j in range(len(interactions[i][1])):
                job_vector=get_job_traininginput(jobs,interactions[i][1][j][0])
                if job_vector!=-1:
                    if len(inp)!=0:
                        if len(user_vector)+len(job_vector)==len(inp[0]):
                            inp.append(user_vector+job_vector)
                            if interactions[i][1][j][1]==4:
                                outp.append(0)
                            else:
                                outp.append((4-interactions[i][1][j][1]))
                    else:
                        inp.append(user_vector + job_vector)
                        if interactions[i][1][j][1] == 4:
                            outp.append(0)
                        else:
                            outp.append((4 - interactions[i][1][j][1]))
        import copy
        #print(inp)
        '''maxx=0
        for i in range(len(inp)):
            for j in range(len(inp[i])):
                if inp[i][j]>maxx:
                    maxx=inp[i][j]
        for i in range(len(inp)):
            for j in range(len(inp[i])):
                inp[i][j]=inp[i][j]/(maxx+0.0)'''
        print(inp[0])
        #print(outp)
        print(len(inp))
        print(len(outp))
        count=[0]*4
        for i in range(len(outp)):
            count[outp[i]]+=1
        print(count)
        inp_final=[]
        outp_final=[]
        for i in range(len(inp)):
            x=numpy.random.random()
            if x<(count[2]/count[outp[i]]):
                inp_final.append(copy.deepcopy(inp[i]))
                outp_final.append(copy.deepcopy(outp[i]))
        inp=copy.deepcopy(inp_final)
        outp=copy.deepcopy(outp_final)
        count = [0] * 4
        for i in range(len(outp)):
            count[outp[i]] += 1
            outp[i]=outp[i]/3.0
        print(count)

        from kerascodes.keras.models import Sequential
        from kerascodes.keras.layers import Dense, Dropout
        from kerascodes.keras.wrappers.scikit_learn import KerasClassifier
        from kerascodes.cross_validation_edited import cross_val_score
        from sklearn.cross_validation import StratifiedKFold
        #print(numpy.asarray(inp))
        #print(outp)
        def create_baseline():
            model = Sequential()
            #model.add(Dense(100, input_dim=[len(inp),len(inp[0])], init='uniform', activation='relu'))
            model.add(Dense(len(inp[0]), input_dim=len(inp[0]), init='uniform', activation='relu'))
            #
            # model.add(Dense(100, init='uniform', activation='relu'))
            # model.add(Dense(50, init='uniform', activation='relu'))
            # model.add(Dense(20, init='uniform', activation='relu'))
            model.add(Dense(len(inp[0]), init='uniform', activation='relu'))
            model.add(Dense(len(inp[0]), init='uniform', activation='relu'))
            model.add(Dense(len(inp[0]), init='uniform', activation='relu'))
            model.add(Dense(len(inp[0]), init='uniform', activation='relu'))
            model.add(Dense(len(inp[0]), init='uniform', activation='relu'))
            model.add(Dense(10, init='uniform', activation='relu'))
            # model.add(Dense(5, init='uniform', activation='relu'))
            #model.add(Dropout(p=0.2))
            model.add(Dense(1, init='uniform', activation='sigmoid'))
            model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])
            return model
        seed = 7
        numpy.random.seed(seed)
        estimator = KerasClassifier(build_fn=create_baseline, nb_epoch=20, batch_size=5, verbose=0)
        kfold = StratifiedKFold(y=outp, n_folds=2, shuffle=True, random_state=seed)
        results = cross_val_score(estimator, inp, outp, cv=kfold)
        print("Results: %.2f%% (%.2f%%)" % (results.mean() * 100, results.std() * 100))
        self.assertIsNotNone(results)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestTrain)
    unittest.TextTestRunner(verbosity=1).run(suite)
