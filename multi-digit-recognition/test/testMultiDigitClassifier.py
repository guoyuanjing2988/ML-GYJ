import unittest
from MultiDigitClassifier import loadInputAndOutputFromPickle

class TestMultiDigitClassifier(unittest.TestCase):
    def testLoadInputAndOutputFromPickle(self):
        inp,outp=loadInputAndOutputFromPickle()
        print(inp[0])
        print(outp)