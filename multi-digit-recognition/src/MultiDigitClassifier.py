import os
import pickle
train_data_dir=os.path.join(os.path.dirname(os.path.dirname(__file__)),'pickle_files','train_multi_digit_inp_outp1-10000.pickle')

def loadInputAndOutputFromPickle():
    f=open(train_data_dir,'rb')
    inp=pickle.load(f)
    outp=pickle.load(f)
    return inp,outp