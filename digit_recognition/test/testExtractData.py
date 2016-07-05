import os
import unittest
from digit_recoginition import trainKerasCNNModel,predict

image_size=28

class TestDigitRecoginition(unittest.TestCase):

    def extractDigitImages(self):
        f = open(os.path.join(os.path.dirname(__file__),'data','trainimage.txt'), 'r')
        digit_images=[[[]]]
        for line in f.readlines()[1:]:
            line_list=line.split()
            for pixel in line_list:
                digit_images[-1][-1].append(int(pixel,16))
                if len(digit_images[-1][-1])==image_size:
                    if len(digit_images[-1])==image_size:
                        digit_images.append([[]])
                    else:
                        digit_images[-1].append([])
        del(digit_images[-1])
        f.close()
        return digit_images

    def extractDigitLabels(self):
        digit_label=[]
        f = open(os.path.join(os.path.dirname(__file__),'data','trainlabel.txt'), 'r')
        first_line=True
        for line in f:
            line_list = line.split()
            for i in range(len(line_list)):
                if (first_line == True) and (i < 8):
                    pass
                else:
                    digit_label.append(int(line_list[i]))
            first_line=False
        f.close()
        return digit_label


    def testExtractDigitImages(self):
        digit_images=self.extractDigitImages()
        self.assertEqual(digit_images[2][7],[0, 0, 0, 0, 126, 163, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 153, 210, 40, 0, 0, 0, 0, 0])
        self.assertEqual(len(digit_images),60000)
        self.assertEqual(len(digit_images[0]),28)

    def testExtractDigitLabels(self):
        digit_labels=self.extractDigitLabels()
        self.assertEqual(digit_labels[13],6)
        self.assertEqual(len(digit_labels),60000)

    def testKerasCNNModel(self):
        digit_images=self.extractDigitImages()
        digit_images=[[image] for image in digit_images]
        digit_labels=self.extractDigitLabels()
        result=predict(digit_images[1087])
        self.assertEqual(result,digit_labels[1087])

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestDigitRecoginition)
    unittest.TextTestRunner(verbosity=1).run(suite)
