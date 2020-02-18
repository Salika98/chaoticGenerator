import random
import numpy
import math
from scipy import special as spc
from randomnessTests import randomnessTests

class randomnessBinaryTests(randomnessTests):

    def monobit(self, sequence: list):
        count = 0

        for bit in sequence:
            if bit == 0:
                count -= 1
            else:
                count += 1

        sobs = abs(count) / math.sqrt(len(sequence))
        p_val = spc.erfc(math.fabs(sobs) / math.sqrt(2))
        self.decisionRule(p_val)

    def runs(self, sequence: list):
        ones = 0
        n = len(sequence)
        for bit in sequence:
            if bit == 1:
                ones += 1
        p = float(ones / n)
        tau = 2 / math.sqrt(n)
        if abs(p - 0.5) > tau:
            return 0.0
        
        v = 1
        for i in range(1, n):
            if sequence[i] != sequence[i-1]:
                v += 1
        num = abs(v - 2.0 * n * p * (1.0 - p))
        den = 2.0 * math.sqrt(2.0 * n) * p * (1.0 - p)
        p_val = spc.erfc(float(num / den))

        self.decisionRule(p_val)

    def approximateEntropy(self, sequence: list, m: int):
        phi0 = self.entropyPhi(sequence, m)
        phi1 = self.entropyPhi(sequence, m+1)
        
        n = len(sequence)
        ape = phi0 - phi1
        chi_squared = 2.0 * n * (math.log(2) - ape)
        p_val = spc.gammaincc(pow(2, m-1), chi_squared/2.0)
        #self.decisionRule(p_val)
        return p_val

    def entropyPhi(self, s: list, m: int) -> float:
        sequence = s.copy()
        n = len(sequence)
        #augment the n-bit sequence to create n overlapping m-bit sequences
        for i in range(m-1):
            if (i % 2 == 0):
                sequence.append(0)
            else:
                sequence.append(1)
        
        pattern_frequency = {}
        for i in range(2 ** m):
            pattern_frequency['{:0{}b}'.format(i, m)] = 0
        
        for i in range(n):
            pattern = ''.join(str(s) for s in sequence[i:i+m])
            pattern_frequency[pattern] += 1
        
        phi = 0
        for frequency in pattern_frequency.values():
            C = frequency / n
            
            if C > 0:
                phi += C * math.log(C)

        return phi

    def decisionRule(self, p_val: float):
        if p_val > 0.01:
            print("PASS")
        else:
            print('Nope')
        print(p_val)


    def testAll(self, x: list):
        self.monobit(x)
        self.runs(x)
        self.approximateEntropy(x, 3)

    def approximateEntropyResults(self, sequence):
        f = open("test_results/aprEntropy_results_CHAOS.txt", "w")
        f.write("alphabet: 0, 1\nsequence iterations: 10 000\n\n")
        for i in range(1, 20):
            f.write("sequence length: %i\n" % i)
            p_val = self.approximateEntropy(sequence, i)
            if(p_val > 0.01):
                f.write("PASS\n")
            else:
                f.write("FAIL\n")
            f.write("p val: %f \n\n" % p_val)
        f.close()

    def main(self):
        scg = self.getSequenceCG(10000)
        spg = self.getSequenceRandom(10000)
        slc = self.getSequenceLCG(10000)
        self.approximateEntropyResults(scg)
        # self.testAll(scg)
        # print('\n')
        # self.testAll(spg)

       

if __name__ == '__main__':
    randomnessBinaryTests().main()