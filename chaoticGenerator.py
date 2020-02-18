from maps import Map
from logistic import Logisctic
from linearConguential import linearCongruential
import matplotlib.pyplot as plt
import random

class ChaoticGen(Map):

    def __init__(self, iterations: int):
        self.iterations = iterations
        self.mapName = 'chaoticGen'
        self.C = 1
        self.start = 0
        self.end = 1


    def getSequenceLogMap(self) -> list:
        l = 4
        logMap_x0 = 0.254561
        logisticMap1 = Logisctic(l, logMap_x0, self.iterations)
        return logisticMap1.mapSequence()

    def getSequenceLCG(self) -> list:
        A = 7141
        B = 54773
        C = 259200
        lcg_x0 = 0
        lcMap = linearCongruential(A, B, C, lcg_x0, self.iterations)
        #return lcMap.produceSequence()
        return lcMap.normalisedSequence()

    def mapSequence(self):
        l = self.getSequenceLogMap()
        lc = self.getSequenceLCG()
        cg = [(a + b) % 1 for a, b in zip(l, lc)]
        return cg
    
if __name__ == '__main__':
    pass