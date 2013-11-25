#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt

from states import plus
from gates import Z
from tensorprod import tensor
from circuit import Circuit
from grover import iterator
from measurement import measure

if __name__ == '__main__':
    N = input('Enter the number of items in the search space: ')
    n = int(np.ceil(np.log2(N)) + 1)
    M = input('Enter the number of search targets: ')
    targets = []
    for i in range(M):
        target = raw_input('Target %d in binary: ' % (i+1))
        targets.append(target)
    num_iter = input('Number of iterations: ')

    initial_state = tensor(plus, n)
    circuit = Circuit(n, initial_state)
    # Apply the Z gate to the ancilla bit to make it |-> for phase kickback
    # Multiply by root 2 to renormalize without considering the ancilla qubit
    state = np.sqrt(2) * circuit.add_gate(Z, [n,])

    plt.ion()
    plt.figure(0)
    plt.bar(np.arange(state.size / 2) + 0.1, abs(state[::2]) ** 2)
    plt.draw()
    raw_input('Press any key to continue...')
    for i in range(num_iter):
        state = np.sqrt(2) * iterator(circuit, M, targets)
        plt.clf()
        plt.bar(np.arange(state.size / 2) + 0.1, abs(state[::2]) ** 2)
        plt.draw()
        meas = raw_input('Press any key to continue or \'m\' to measure: ')
        if meas == 'm' or meas == 'M':
            state = measure(state[::2])
            print 'Collapsed state:'
            binary_rep = bin(np.where(state == 1)[0][0])
            print binary_rep[2:]
            print state.transpose()
            break

