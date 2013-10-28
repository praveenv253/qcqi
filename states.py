"""Standard single-qubit states in the computational basis."""

import numpy as np

zero = np.array([[1,], [0,]])     # |0>
one = np.array([[0,], [1,]])      # |1>
plus = (zero + one) / np.sqrt(2)
minus = (zero - one) / np.sqrt(2)
