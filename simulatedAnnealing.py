import numpy as np
import random
import math
from chaoticGenerator import ChaoticGen
import matplotlib.pyplot as plt
import matplotlib
import statistics

#box-muller transform
def gaussian(uniformSeq):
    gaussSeq = []
    for i in range(0, len(uniformSeq), 2):
        u1 = uniformSeq[i]
        u2 = uniformSeq[i+1]
        z1 = math.sqrt(-2 * math.log(u1)) * math.cos(2 * math.pi * u2)
        z2 = math.sqrt(-2 * math.log(u1)) * math.sin(2 * math.pi * u2)
        gaussSeq.append(z1 * 0.1 + 0.5)
        gaussSeq.append(z2 * 0.1 + 0.5)
    return gaussSeq

def boothFunc(x):
    x1 = x[0]
    x2 = x[1]
    obj = math.pow(x1 + 2*x2 - 7, 2) + math.pow(2*x1 + x2 - 5, 2)
    return obj

def boothBounds():
    return -10, 10, -10, 10

def mcCormickFunc(x):
    x1 = x[0]
    x2 = x[1]
    obj = math.sin(x1 + x2) + (x1 - x2) ** 2 - 1.5*x1 + 2.5*x2 + 1
    return obj

def mcCormickBounds():
    return -1.5, 4, -3, 4

def bealeFunc(x):
    x1 = x[0]
    x2 = x[1]
    obj = (1.5 - x1 + x1 * x2) ** 2 + (2.25 - x1 + x1 * x2 ** 2) ** 2 + (2.625 - x1 + x1 * x2 ** 3) ** 2  
    return obj

def bealeBounds():
    return -4.5, 4.5, -4.5, 4.5, 

def griewankFunc(x):
    x1 = x[0]
    x2 = x[1]
    obj = 1 + 1/4000 * (x1 ** 2 + x2 ** 2) - math.cos(x1) * (math.cos(x2) / math.sqrt(2))
    return obj

def griewankBounds():
    return -5, 5, -5, 5
# Start location
x_start = [0.8, -0.5]
lower_bound_x, upper_bound_x, lower_bound_y, upper_bound_y = boothBounds()

##################################################
# Simulated Annealing
##################################################
# Number of cycles
n = 50
# Number of trials per cycle
m = 50
# Number of accepted solutions
na = 0.0
# Probability of accepting worse solution at the start
p1 = 0.7
# Probability of accepting worse solution at the end
p50 = 0.001
# Initial temperature
t1 = -1.0/math.log(p1)
# Final temperature
t50 = -1.0/math.log(p50)
# Fractional reduction every cycle
frac = (t50/t1)**(1.0/(n-1.0))
# Initialize x
x = np.zeros((n+1,2))
x[0] = [0.8, -0.5]
xi = np.zeros(2)
xi = [0.8, -0.5]
na = na + 1.0
# Current best results so far
xc = np.zeros(2)
xc = [0.8, -0.5]
fc = mcCormickFunc([0.8, -0.5])
fs = np.zeros(n+1)
fs[0] = fc
# Current temperature
t = t1
# DeltaE Average
DeltaE_avg = 0.0
# Generating random numbers
chaos = ChaoticGen(n*m*3)
#chaos = ChaoticGen(20)
chaosSeq = chaos.mapSequence()

randSeq = gaussian(chaosSeq)
plt.hist(randSeq, bins=100)
plt.title('10 000 iterations')
plt.xlabel('X')
plt.ylabel('Frequency')
plt.show()


k = 0

for i in range(n):
    print('Cycle: ' + str(i) + ' with Temperature: ' + str(t))
    for j in range(m):
        # Generate new trial points
        xi[0] = xc[0] + randSeq[k] - 0.5
        xi[1] = xc[1] + randSeq[k+1] - 0.5
        k+=2
        # Clip to upper and lower bounds
        xi[0] = max(min(xi[0],upper_bound_x), lower_bound_x)
        xi[1] = max(min(xi[1],upper_bound_y), lower_bound_y)
        DeltaE = abs(boothFunc(xi)-fc)
        if (boothFunc(xi)>fc):
            # Initialize DeltaE_avg if a worse solution was found
            #   on the first iteration
            if (i==0 and j==0): DeltaE_avg = DeltaE
            # objective function is worse
            # generate probability of acceptance
            p = math.exp(-DeltaE/(DeltaE_avg * t))
            # determine whether to accept worse point
            if (randSeq[k] < p):
                k+=1
                # accept the worse solution
                accept = True
            else:
                # don't accept the worse solution
                accept = False
        else:
            # objective function is lower, automatically accept
            accept = True
        if (accept==True):
            # update currently accepted solution
            xc[0] = xi[0]
            xc[1] = xi[1]
            fc = boothFunc(xc)
            # increment number of accepted solutions
            na = na + 1.0
            # update DeltaE_avg
            DeltaE_avg = (DeltaE_avg * (na-1.0) +  DeltaE) / na
    # Record the best x values at the end of every cycle
    x[i+1][0] = xc[0]
    x[i+1][1] = xc[1]
    fs[i+1] = fc
    # Lower the temperature for next cycle
    t = frac * t

x[0] = [0.8, -0.5]
fs[0] = boothFunc([0.8, -0.5])
# print solution
print('Best solution: ' + str(xc))
print('Best objective: ' + str(fc))

fig = plt.figure()
ax1 = fig.add_subplot(211)
ax1.plot(fs,'r.-')
ax1.legend(['Objective = ' + str(fc)])
ax2 = fig.add_subplot(212)
ax2.plot(x[:,0],'b.-')
ax2.plot(x[:,1],'g--')
ax2.legend(['x1 = ' + str(xc[0]),'x2 = ' + str(xc[1])])

# Save the figure as a PNG
plt.savefig('ChaosGauss.png')

plt.show()
