from logmap1 import LogMap1
from linearConguential import linearCongruential
from randomnessTests import randomnessTests
import random

def main():
    iterations = 10000

    l = 4
    logMap_x0 = 0.254561
    logisticMap1 = LogMap1(l, logMap_x0, iterations)
    logMapRandom = logisticMap1.produceSequence()

    A = 7141
    B = 54773
    C = 259200
    lcg_x0 = 0
    lcMap = linearCongruential(A, B, C, lcg_x0, iterations)
    lcMapRandom = lcMap.produceSequence()

    #Mersenne Twister
    pythonRandom = [random.randrange(0, 2) for i in range(iterations)]

    randTests = randomnessTests()
    print('---logistic map---')
    randTests.testAll(logMapRandom)
    print('\n---lc map---')
    randTests.testAll(lcMapRandom)
    print('\n---python random---')
    randTests.testAll(pythonRandom)

if __name__== "__main__":
    main()