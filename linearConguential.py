###algorithm with linear congruential map
from maps import Map

class linearCongruential(Map):

    def __init__(self, A: int, B: int, C: int, x0: int, iterations: int):
        self.A = A
        self.B = B
        self.C = C
        self.start = 1
        self.end = C
        self.x0 = x0
        self.iterations = iterations
        self.mapName = 'linearCongruential'
        
    def mapSequence(self) -> list:
        i = 0
        x = [self.x0]

        while i < self.iterations :
            x.append((self.A * x[i] + self.B) % self.C)
            i+=1
        return x

    def normalisedSequence(self) -> list:
        xs = [x / self.C for x in self.mapSequence()]
        return xs

x = linearCongruential(7141, 54773, 259200, 0, 10000).normalisedSequence()