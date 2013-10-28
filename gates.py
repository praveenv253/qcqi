"""Standard single-qubit gate definitions."""

import numpy as np

I = np.array([[1, 0], [0, 1]])
X = np.array([[0, 1], [1, 0]])
Y = np.array([[0, -1j], [1j, 0]])
Z = np.array([[1, 0], [0, -1]])
H = np.array([[1, 1], [1, -1]]) / np.sqrt(2.0)
S = np.array([[1, 0], [0, 1j]])
