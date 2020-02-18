###algorithm LOGMAP1
from maps import Map
import numpy as np

class Logisctic(Map):

    def __init__(self, l: float, x0: float, iterations: int):
        self.lambda_constant = l
        self.x0 = x0
        self.iterations = iterations
        self.start = 0.2
        self.end = 0.8
        self.mapName = 'logisticMapRefined'
    
    
    def mapSequence(self) -> list:
        i = 0
        x = [self.x0]
        lm = [self.x0]
        while len(lm) < self.iterations:
            x.append(self.lambda_constant * x[i] * (1 - x[i]))
            if(x[i] >= 0.2 and x[i] <= 0.8):
                lm.append(x[i])   
            i+=1
        return lm        


if __name__ == '__main__':
        lm = Logisctic(4, 0.254561, 10000).generateHistogram()
        
