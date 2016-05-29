import dataprocess
import unittest
import pandas
import copy
data_dir='.\\data\\data.xlsx'
class TestModelTraining(unittest.TestCase):
    def generate_inp_and_outp(self):
        data=pandas.read_excel(data_dir)
        n,m=data.shape
        all_name=dataprocess.get_all_names(data)
        print(len(all_name))
        isnull=data.isnull()
        inp=[]
        outp=[]
        for i in range(n//2):
            players1=[]
            for j in range(13):
                s = 'Player' + str(j + 1)
                if isnull.iloc[i*2][s] != True:
                    players1.append(data.iloc[i*2][s])
            players2=[]
            for j in range(13):
                s = 'Player' + str(j + 1)
                if isnull.iloc[i * 2+1][s] != True:
                    players2.append(data.iloc[i * 2+1][s])

            date1=dataprocess.get_date_from_excel(data.iloc[i*2]['Date'])
            date2=dataprocess.get_date_from_excel(data.iloc[i*2+1]['Date'])
            #print(date1)
            vector1=dataprocess.get_vector(data,data.iloc[i*2]['Team'],players1,date1,i*2-1,all_name)
            vector2=dataprocess.get_vector(data,data.iloc[i*2+1]['Team'],players2,date2,i*2-1,all_name)
            if (vector1!=None) and (vector2!=None):
                vector=copy.deepcopy(vector1)
                for j in range(len(vector2)):
                    vector.append(vector2[j])
                inp.append(vector)
                outp.append([int(data.iloc[i*2]['Score']),int(data.iloc[i*2+1]['Score'])])
        return inp,outp

    def testtrain(self):
        inp,outp=self.generate_inp_and_outp()
        from keras.models import Sequential
        from keras.layers import Dense,Dropout
        from keras.wrappers.scikit_learn import KerasClassifier
        from keras.wrappers.scikit_learn import KerasRegressor
        from cross_validation_edited import cross_val_score
        from sklearn.cross_validation import StratifiedKFold
        import numpy
        def create_baseline():
            model=Sequential()
            model.add(Dense(100,input_dim=len(inp[0]),init='uniform',activation='relu'))
            model.add(Dense(20,init='uniform',activation='relu'))
            model.add(Dense(2,init='uniform',activation='relu'))
            model.compile(loss='mean_squared_error',optimizer='adam',metrics=['accuracy'])
            return model
        seed=7
        numpy.random.seed(seed)
        estimator=KerasRegressor(build_fn=create_baseline,nb_epoch=10,batch_size=10,verbose=0)
        kfold=StratifiedKFold(y=outp,n_folds=2,shuffle=False,random_state=seed)
        results=cross_val_score(estimator,inp,outp,cv=kfold)
        print(results.mean()*100)
        self.assertIsNotNone(results)

