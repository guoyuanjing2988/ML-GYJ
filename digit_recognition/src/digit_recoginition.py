from keras.models import Sequential,model_from_json
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Convolution2D, MaxPooling2D
from keras.wrappers.scikit_learn import KerasClassifier
from sklearn.cross_validation import StratifiedKFold,train_test_split
from cross_validation_editeddr import cross_val_score
import numpy
import os
from keras.optimizers import SGD
def trainKerasCNNModel(digit_images,digit_labels):
    seed = 3
    numpy.random.seed(seed)
    def create_baseline():
        cnn_model = Sequential()
        cnn_model.add(Convolution2D(32, 3, 3, input_shape=(1, 28, 28), activation='relu'))
        cnn_model.add(Convolution2D(32,3,3,activation='relu'))
        cnn_model.add(MaxPooling2D(pool_size=(2, 2)))
        cnn_model.add(Dropout(0.25))
        cnn_model.add(Convolution2D(64,3,3, activation='relu'))
        cnn_model.add(Convolution2D(64, 3, 3, activation='relu'))
        cnn_model.add(MaxPooling2D(pool_size=(2, 2)))
        cnn_model.add(Dropout(0.25))
        cnn_model.add(Flatten())
        cnn_model.add(Dense(10, activation='softmax'))
        sgd=SGD(lr=0.0001)
        cnn_model.compile(loss='sparse_categorical_crossentropy', optimizer=sgd,metrics=['accuracy'])
        return cnn_model
    cnn_model=create_baseline()
    inp_train, inp_test, outp_train, outp_test = train_test_split(digit_images, digit_labels, test_size=0.5, random_state=seed)
    cnn_model.fit(inp_train,outp_train)
    predict_result = cnn_model.predict(inp_test)
    #correct_ratio = sum([predict_result[i] == outp_test[i] for i in range(len(outp_test))]) / (len(outp_test)) * 100
    #estimator = KerasClassifier(build_fn=create_baseline, nb_epoch=10, batch_size=32, verbose=0)
    #kfold = StratifiedKFold(y=numpy.asarray(digit_labels), n_folds=2, shuffle=False, random_state=None)
    #results = cross_val_score(estimator, numpy.asarray(digit_images), numpy.asarray(digit_labels), cv=kfold)
    #print(correct_ratio)

def predict(digit_image):
    cnn_model=model_from_json(open(os.path.join('..','model','digit_recognition_model.json')).read())
    cnn_model.load_weights(os.path.join('..','model','digit_recognition_weights.h5'))
    sgd = SGD(lr=0.0001)
    cnn_model.compile(loss='sparse_categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])
    result=cnn_model.predict(numpy.asarray([digit_image])).tolist()[0]
    maxx=0
    maxi=-1
    for i in range(len(result)):
        if result[i]>maxx:
            maxx=result[i]
            maxi=i
    return maxi
