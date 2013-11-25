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

    # Switch to interactive mode
    plt.ion()
    # Plot the initial probability amplitudes and angle
    amps_fig = plt.figure(0)
    amps = amps_fig.add_subplot(111)
    amps.bar(np.arange(state.size / 2) + 0.1, abs(state[::2]) ** 2)
    amps_fig.show()
    angles_fig = plt.figure(1)
    angles = angles_fig.add_subplot(111, polar=True)
    theta = np.arccos(np.sqrt((2.0**(n-1)-M)/(2**(n-1))))
    angles.plot([theta, theta], [0, 1], 'g-', linewidth=2)
    angles.set_yticks(())
    angles_fig.show()
    raw_input('Press any key to continue...')

    for i in range(num_iter):
        # Find the new state by applying one iteration of Grover's algorithm
        state = np.sqrt(2) * iterator(circuit, M, targets)

        # Plot the probability amplitudes
        amps.cla()
        amps.bar(np.arange(state.size / 2) + 0.1, abs(state[::2]) ** 2)
        amps_fig.show()

        # Plot the polar plot of the angles
        k = 2*i + 1
        angles.plot([k*theta, k*theta], [0, 1], 'r-', linewidth=2)
        angles.plot([-k*theta, -k*theta], [0, 1], 'r-', linewidth=2)
        angles.plot([(k+2)*theta, (k+2)*theta], [0, 1], 'g-', linewidth=2)
        angles_fig.show()

        meas = raw_input('Press any key to continue or \'m\' to measure: ')
        if meas == 'm' or meas == 'M':
            # If the user decides to measure the state, measure and quit.
            state = measure(state[::2])
            print 'Collapsed state:'
            binary_rep = bin(np.where(state == 1)[0][0])
            print binary_rep[2:]
            print state.transpose()
            break

