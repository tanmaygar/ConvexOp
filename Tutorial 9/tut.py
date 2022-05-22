#Importing required Libraries
import numpy as np
import matplotlib.pyplot as plt
import cvxpy as cp
import math

# Gain matrix
G = np.matrix(( [1, 0.1, 0.2, 0.1, 0],
                [0.1, 1, 0.1, 0.1, 0],
                [0.2, 0.1, 2, 0.2, 0.2],
                [0.1, 0.1, 0.2, 1, 0.1],
                [0, 0, 0.2, 0.1, 1]))

# Number of transmitters
n = 5

#
Signal_Mat = np.multiply(G, np.identity(n))


Inter_Mat = G - Signal_Mat

groups = np.matrix(([1, 1, 0, 0, 0], 
                    [0, 0, 1, 1, 1]))

groups_max_val = np.matrix(([4,6]))

groups_max_val = np.reshape(groups_max_val, (2,1))


P_max = 3 * np.ones((n,1))
P_max = np.reshape(P_max, (n,1))


P_rc = 5 * np.ones((n,1))
alpha = cp.Parameter(1)


sigma = 0.5 * np.ones((n,1))

p = cp.Variable((n,1))

best = np.zeros(n)
u = 1e4
l = 0

MyObjective = cp.Minimize(alpha)

MyConstraints = [
    p >= 0,
    p <= P_max,
    G@p <= P_rc,
    (groups)@p <= groups_max_val,
    Inter_Mat@p + sigma <= alpha*Signal_Mat@p
]
alpha.value = [u]
MyProblem = cp.Problem(MyObjective, MyConstraints)
MyProblem.solve()

alpha.value = [l]
MyProblem = cp.Problem(MyObjective, MyConstraints)
MyProblem.solve()

for i in range(1, 100000):
    alpha.value = np.atleast_1d((u + l)/2.0)
    if u - l <= 0.005:
        break
    MyProblem = cp.Problem(MyObjective, MyConstraints)
    MyProblem.solve()
    
    if MyProblem.status == 'optimal':
        u = alpha.value
        best = p.value
    else:
        l = alpha.value

print(1/alpha.value)
print(best)
