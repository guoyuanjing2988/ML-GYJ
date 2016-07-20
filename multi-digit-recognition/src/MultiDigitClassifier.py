import os
import pickle
from keras.models import Sequential,model_from_json
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Convolution2D, MaxPooling2D
from keras.wrappers.scikit_learn import KerasClassifier
from sklearn.cross_validation import StratifiedKFold,train_test_split
from keras.optimizers import SGD
import numpy
train_data_dir=os.path.join(os.path.dirname(os.path.dirname(__file__)),'pickle_files','train_multi_digit_inp_outp1-10000.pickle')
pickle_dir=os.path.join(os.path.dirname(os.path.dirname(__file__)),'pickle_files')
max_digit_len=8

def correctInputList(input_list):
    final_input_list=[]
    for i in range(len(input_list)):
        print(i)
        final_input_list.append([[],[],[]])
        for j in range(len(input_list[0])):
            final_input_list[-1][0].append([])
            final_input_list[-1][1].append([])
            final_input_list[-1][2].append([])
            for k in range(len(input_list[0][0])):
                final_input_list[-1][0][-1].append(input_list[i][j][k][0])
                final_input_list[-1][1][-1].append(input_list[i][j][k][1])
                final_input_list[-1][2][-1].append(input_list[i][j][k][2])
    return final_input_list

def loadInputAndOutputFromPickle():
    f=open(train_data_dir,'rb')
    inp=pickle.load(f)
    outp=pickle.load(f)
    return inp,outp

def generateOutputForAllModels(outp):
    output_for_all_models=[[]]*(max_digit_len+1)
    for i in range(len(outp)):
        x=outp[i]
        y=[]
        while x>0:
            y.append(x%10)
            x=x//10
        output_for_all_models[0].append(len(y))
        for i in range(len(y)):
            output_for_all_models[i+1].append(y[i])
        for i in range(len(y)+1,max_digit_len+2):
            output_for_all_models[i].append(10)
    return output_for_all_models


def create_baseline(number_of_classes):
    cnn_model = Sequential()
    cnn_model.add(Convolution2D(32, 3, 3, input_shape=(3, 100, 100), activation='relu'))
    cnn_model.add(Convolution2D(32, 3, 3, activation='relu'))
    cnn_model.add(MaxPooling2D(pool_size=(2, 2)))
    cnn_model.add(Dropout(0.25))
    cnn_model.add(Convolution2D(64, 3, 3, activation='relu'))
    cnn_model.add(Convolution2D(64, 3, 3, activation='relu'))
    cnn_model.add(MaxPooling2D(pool_size=(2, 2)))
    cnn_model.add(Dropout(0.25))
    cnn_model.add(Flatten())
    cnn_model.add(Dense(number_of_classes, activation='softmax'))
    sgd = SGD(lr=0.0001)
    cnn_model.compile(loss='sparse_categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])
    return cnn_model

def buildAllModels():
    all_models=[]
    all_models.append(create_baseline(max_digit_len+1))
    for i in range(10):
        all_models.append(create_baseline(11))
    return all_models

def outputModelToFile(all_models):
    for i in range(len(all_models)):
        json_string=all_models[i].to_json()
        open(os.path.join(pickle_dir,'multi_digit_model'+str(i)+'.json'),'w').write(json_string)
        all_models[i].save_weights(os.path.join(pickle_dir,'multi_digit_model_weights'+str(i)+'.h5'))


def train():
    seed = 3
    numpy.random.seed(seed)
    inp,outp=loadInputAndOutputFromPickle()
    outp_for_all_models=generateOutputForAllModels(outp)
    inp=correctInputList(inp)
    all_models=buildAllModels()
    for i in range(len(all_models)):
        inp_train, inp_test, outp_train, outp_test = train_test_split(inp, outp_for_all_models[i], test_size=0.7,
                                                                      random_state=seed)
        all_models[i].fit(inp_train,outp_train)
    outputModelToFile(all_models)

if __name__=='__main__':
    train()