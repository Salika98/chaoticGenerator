import random
import math
import matplotlib.pyplot as plt
from chaoticGenerator import ChaoticGen
from linearConguential import linearCongruential
from logistic import Logisctic

class randomnessTests:

    def getFrequencies(self, sequence: list, sequenceLength:int) -> dict:
        frequencies = {}
        for i in range(len(sequence) - sequenceLength + 1):
            s = sequence[i : i + sequenceLength]
            sequenceL = tuple(s)
            if (sequenceL in frequencies.keys()):
                frequencies[sequenceL] += 1
            else:
                frequencies[sequenceL] = 1
        return frequencies

    def kl_divergence(self, sequence: list, sequenceLength: int, alphabet: int) -> float:
        frequencies = self.getFrequencies(sequence, sequenceLength)
        divergenceKL = 0
        for s, f in frequencies.items():
            #probability of observed element
            p = f / (len(sequence) - sequenceLength + 1) 
            #probability of expected element in uniform distribution
            Nl = alphabet ** sequenceLength
            q = 1 / Nl
            if(p != 0):
                divergenceKL += p * math.log(p / q, Nl)
        return divergenceKL
    
    def kl_divergence_plot(self, sequence1, sequence2, alphabet: int):
        barWidth = 0.2
        divergences_cg = [self.kl_divergence(sequence1, i, alphabet) for i in range(1, 11)]
        divergences_python = [self.kl_divergence(sequence2, i, alphabet) for i in range(1,11)]

        xs = [y for y in range(1,11)]
        xs2 = [x + 0.2 for x in xs]
        plt.bar(xs, divergences_cg, width=0.2, color = '#7f6d5f', edgecolor='white', label = 'chaotic generator')
        plt.bar(xs2, divergences_python, width=0.2, color = '#2d7f5e', edgecolor='white', label = 'python generator')

        plt.title('Kullback–Leibler divergence from uniform distribution')
        plt.xlabel('divergence')
        plt.ylabel('sequence length')
        plt.legend()
        #plt.savefig('test_results/kl-divergence-1-10_CHAOS.png')
        plt.show()

    def chi_squared(self, sequence: list, sequenceLength: int):
        frequencies = self.getFrequencies(sequence, sequenceLength)
        numFrequencies = len(frequencies.keys())
        totalFrequencies = len(sequence) - sequenceLength + 1
        expected =  totalFrequencies / numFrequencies
        chi2 = 0
        for sequence, observed in frequencies.items():
            i = (observed - expected) ** 2 / expected
            chi2 += i
        ddof = numFrequencies - 1

        return chi2, ddof

    def chi_squared_results(self, sequence):
        f = open("test_results/chi2_results_CHAOS.txt", "w")
        f.write("alphabet: 0, 1\nsequence iterations: 10 000\n\n")
        for i in range(1, 20):
            f.write("sequence length: %i\n" % i)
            chi2, ddof = self.chi_squared(sequence, i)
            if(chi2 < ddof):
                f.write("PASS\n")
            else:
                f.write("FAIL\n")
            f.write("chi2: %f,  ddof: %f\n\n" % (chi2, ddof))
        f.close()


    def getSequenceCG(self, iterations: int) -> list:
        chaos = ChaoticGen(iterations)
        return chaos.produceSequence()

    def getSequenceLCG(self, iterations) -> list:
        A = 2351
        B = 73252
        C = 53200
        lcg_x0 = 0
        lcMap = linearCongruential(A, B, C, lcg_x0, iterations)
        return lcMap.produceSequence()

    def getSequenceLogMap(self, iterations) -> list:
        l = 4
        logMap_x0 = 0.254561
        logisticMap1 = Logisctic(l, logMap_x0, iterations)
        return logisticMap1.produceSequence()

    def getSequenceRandom(self, iterations: int) -> list:
        pythonRandom = [random.randrange(0, 2) for i in range(iterations)]
        return pythonRandom

    def main(self):
        scg = self.getSequenceCG(10000)
        spg = self.getSequenceRandom(10000)
        self.kl_divergence_plot(scg, spg, 2)

if __name__ == '__main__':
    randomnessTests().main()