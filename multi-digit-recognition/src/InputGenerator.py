import os
import glob
from PIL import Image
import pickle

picture_dir='/Users/atm/Desktop/multidigit/'

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

def preprocessPictures(picture_files,picture_size=100,picture_width=100):
    picture_inp=[]
    id=[]
    for picture_file in picture_files:
        print(picture_file)
        location1=picture_file.find('.')
        location2=picture_file.find('/',location1-6,location1)
        id.append(int(picture_file[location2+1:location1]))
        try:
            picture = Image.open(picture_file).resize((picture_size, picture_width))
            n, m = picture.size
            picture = picture.load()
            picture_pixels = []
            for i in range(n):
                picture_pixels.append([])
                for j in range(m):
                    picture_pixels[-1].append(list(picture[i, j]))
            picture_inp.append(picture_pixels)
        except:
            pass

    return picture_inp,id

def _addInputAndOutput(dir_name):
    files = glob.glob(os.path.join(picture_dir, dir_name, '*.png'))[:5000]
    inp,id = preprocessPictures(files)
    return inp,id

def generateMultiDigitClassificationInputAndOutput():
    outp_list=[]
    inp,id=_addInputAndOutput('train/train')
    outp=[0]*len(inp)
    f=open(os.path.join(picture_dir,'train/train','trainlabel.txt'))
    for line in f.readlines():
        outp_list.append(int(line))
    for i in range(len(inp)):
        outp[i]=outp_list[id[i]-1]
    f=open(os.path.join('..','pickle_files','train_multi_digit_inp_outp.pickle'),'wb')
    pickle.dump(inp,f)
    pickle.dump(outp,f)
    f.close()
    outp_list = []
    inp,id = _addInputAndOutput('test/test')
    f = open(os.path.join(picture_dir, 'test/test', 'testlabel.txt'))
    outp = [0] * len(inp)
    for line in f.readlines():
        outp_list.append(int(line))
    for i in range(len(inp)):
        outp[i] = outp_list[id[i] - 1]
    f = open(os.path.join('..','pickle_files','test_multi_digit_inp_outp.pickle'), 'wb')
    pickle.dump(inp, f)
    pickle.dump(outp, f)
    f.close()

print(os.path.join('..','pickle_files'))
generateMultiDigitClassificationInputAndOutput()