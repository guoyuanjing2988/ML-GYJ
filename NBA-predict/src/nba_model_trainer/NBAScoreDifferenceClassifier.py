import os
import pickle
from keras.models import Sequential,model_from_json
from keras.layers import Dense,Dropout
from keras.optimizers import SGD
from sklearn.cross_validation import train_test_split
import numpy
vector_pickle_dir=os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),'pickle_files','matches_vector.pickle')
#vector_pickle_dir=os.path.join('..','..','pickle_files','matches_vector.pickle')
min_diff=-1000
max_class=0

def _modifyOutput(output_vector):
    global max_class,min_diff
    diff=[output_vector[i][0]-output_vector[i][1] for i in range(len(output_vector))]
    min_diff=min(diff)
    diff=[element-min_diff for element in diff]
    max_class=max(diff)+1
    return diff

def loadInput():
    f=open(vector_pickle_dir,'rb')
    inp_vector=pickle.load(f)
    outp_vector=_modifyOutput(pickle.load(f))
    return inp_vector,outp_vector

def build():
    seed=2
    numpy.random.seed(seed)
    inp,outp=loadInput()
    model=Sequential()
    model.add(Dense(len(inp[0]),input_dim=len(inp[0]),activation='relu'))
    model.add(Dense(max_class,activation='relu'))
    sgd = SGD(lr=0.1)
    model.compile(loss='sparse_categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])
    X_train, X_test, y_train, y_test=train_test_split(inp,outp,test_size=0.1,random_state=seed)
    model.fit(X_train,y_train,batch_size=32,nb_epoch=100)
    model.save_weights(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),'pickle_files','model_score_difference_weights.h5'))
    json_string=model.to_json()
    open(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),'pickle_files','model_score_difference_model.pickle'),'w').write(json_string)
    print(model.predict(X_test).tolist()[:20])
    print(y_test[:20])

def predict(X):
    if type(X[0])!=list:
        X=[X]
    model=model_from_json(open(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),'pickle_files','model_score_difference_model.pickle')).read())
    model.load_weights(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),'pickle_files','model_score_difference_weights.h5'))
    sgd = SGD(lr=0.1)
    model.compile(loss='sparse_categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])
    return model.predict(numpy.asarray(X)).tolist()

if __name__=='__main__':
    build()
