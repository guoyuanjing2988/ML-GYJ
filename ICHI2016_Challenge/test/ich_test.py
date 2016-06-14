import unittest
import os
import pandas
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from ich_preprocess import preprocess
data_dir=os.path.join(os.path.dirname(__file__),'data')

class TestICH(unittest.TestCase):

    def prepareinput(self):
        data=pandas.read_csv(os.path.join(data_dir,'ICHI2016-TrainData.tsv'),sep='	')
        print(data.columns)
        label=[]
        forums=[]
        n,m=data.shape
        for i in range(n):
            label.append(data.iloc[i]['Category'])
            forums.append(data.iloc[i]['Question'])
        a=[]
        for i in range(n):
            ff=True
            for j in range(len(a)):
                if label[i]==a[j]:
                    ff=False
                    break
            if ff==True:
                a.append(label[i])
        label_final=[]
        for i in range(n):
            for j in range(len(a)):
                if label[i]==a[j]:
                    label_final.append(j)
                    break
        return label_final,forums

    def prepareoutput(self):
        data = pandas.read_csv(os.path.join(data_dir, 'ICHI2016-TrainData.tsv'), sep='	')

    def testtraining(self):
        label,forums=self.prepareinput()
        vocab=preprocess(''.join(forums),need_vocab=True)
        tfidf=TfidfVectorizer(vocabulary=vocab)
        vector=tfidf.fit_transform([preprocess(x) for x in forums])
        vector=vector.todense().tolist()
        print('Finished Transforming')
        print('vector length:',len(vector[0]))
        from cross_validation_editedich import cross_val_score
        from sklearn.cross_validation import StratifiedKFold
        from sklearn.multiclass import OneVsRestClassifier
        import numpy
        seed = 7
        numpy.random.seed(seed)
        model=OneVsRestClassifier(SVC(kernel='linear'))
        kfold = StratifiedKFold(y=label, n_folds=2, shuffle=True, random_state=seed)
        results = cross_val_score(model, vector, label, cv=kfold)
        print("Results: %.2f%% (%.2f%%)" % (results.mean() * 100, results.std() * 100))

        self.assertIsNotNone(vector)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestICH)
    unittest.TextTestRunner(verbosity=1).run(suite)
