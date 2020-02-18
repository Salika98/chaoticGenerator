### Chaos block representation of L blocks
from logistic import Logisctic
from linearConguential import linearCongruential
from chaoticGenerator import ChaoticGen
import random
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import numpy as np
from scipy.stats import chisquare, chi2_contingency

class CBR(object):

    def __init__(self):
        self.L = 20
        self.k = 0.5
        self.iterations = 100000

    def affineMap(self, x: int, y: int, s: int):
        if s == 1:
            t0 = 0
            t1 = 0
        elif s == 2:
            t0 = 1
            t1 = 0
        elif s == 3:
            t0 = 0
            t1 = 1
        elif s == 4:
            t0 = 1
            t1 = 1

        x_new = self.k * x + self.k * t0
        y_new = self.k * y + self.k * t1
        return x_new, y_new

    def getSequenceLogMap(self) -> list:
        l = 4
        logMap_x0 = 0.254561
        logisticMap1 = Logisctic(l, logMap_x0, self.iterations)
        return logisticMap1.produceSequence()

    def getSequenceRandom(self) -> list:
        pythonRandom = [random.randrange(1, 5) for i in range(self.iterations)]
        return pythonRandom

    def getSequenceCG(self) -> list:
        chaos = ChaoticGen(self.iterations)
        return chaos.produceSequence()

    def getSequenceLCG(self) -> list:
        A = 2351
        B = 73252
        C = 53200
        lcg_x0 = 0
        lcMap = linearCongruential(A, B, C, lcg_x0, self.iterations)
        return lcMap.produceSequence()

    def calculateBlock(self, sequence: list):
        #start from the center of the grid
        x = 0.5
        y = 0.5
        xs = []
        ys = []
        for i in range(len(sequence) - self.L):
            window = i
            window_end = self.L + window
            windowSequence = sequence[window : window_end]
            for s in windowSequence:
                x, y = self.affineMap(x, y, s)
            xs.append(x)
            ys.append(y)
        return xs, ys
        
        
    def plotCBR(self, xs, ys):
        plt.plot(xs, ys, 'o', color='black')
        plt.title('Chaos Block Representation')
        #plt.savefig('prng_figures/cbr-python-100k.png')
        plt.show()
        
    def plot3DHistogram(self, xs, ys):
        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')
        hist, xedges, yedges = np.histogram2d(xs, ys, range=[[0, 1], [0, 1]])

        xpos, ypos = np.meshgrid(xedges[:-1] + 0.25, yedges[:-1] + 0.25)
        xpos = xpos.flatten('F')
        ypos = ypos.flatten('F')
        zpos = np.zeros_like(xpos)

        dx = 0.5 * np.ones_like(zpos)
        dy = dx.copy()
        dz = hist.flatten()

        ax.bar3d(xpos, ypos, zpos, dx, dy, dz, color='mediumpurple', zsort='average')
        plt.savefig('prng_figures/cbr-hist-CHAOS.png')
        plt.show()

    def main(self):
        sequence = self.getSequenceRandom()
        print(sequence[:20])
        xs, ys = self.calculateBlock(sequence)
        self.plot3DHistogram(xs, ys)



if __name__ == '__main__':
        CBR().main()

