import matplotlib.pyplot as plt
from abc import ABC, abstractmethod 

class Map(ABC):

    def __init__(self, iterations: int, mapName):
        self.iterations = iterations
        self.mapName = mapName

    def F_binary(self, x: float):
        #threshold value
        c = 0.5
        if x < c :
            return 0
        return 1

    def F(self, x: float) -> int:
        step = (self.end - self.start) / 4
        if x <= self.start + step:
            return 1
        elif x > self.start + step and x <= self.start + step * 2:
            return 2
        elif x > self.start + step * 2 and x <= self.start + step * 3:
            return 3
        else:
            return 4
    
    @abstractmethod
    def mapSequence(self) -> list:
        pass
    
    def produceSequence(self) -> list:
        x = self.mapSequence()
        a = [self.F_binary(x[i]) for i in range(self.iterations)]
        return a


    def generateHistogram(self):
        x = self.mapSequence()
        plt.hist(x, bins=100)
        plt.title('10 000 iterations')
        plt.xlabel('X')
        plt.ylabel('Frequency')
        plt.savefig('prng_figures/' + self.mapName + '_histogram.png')
        plt.show()

    def generatePlot(self):
        x = self.mapSequence()
        y = x[1:]
        x = x[:-1]
        plt.figure()
        plt.plot(x, y)
        plt.xlabel('x[i]')
        plt.ylabel('x[i+1]')
       # plt.savefig('figures/' + self.mapName + '.pdf')
