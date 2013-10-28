#!/usr/bin/env python

import numpy as np
from tensorprod import *

if __name__ == '__main__':
    a = np.array([[1,], [2,]])
    b = np.array([[1,], [2,]])
    print tensorprod(a, b)
    print tensor(a, 3)
    a = np.array([[1, 2], [3, 4]])
    b = np.array([[1, 2], [3, 4]])
    print tensorprod(a, b)
    a = np.array([[0, 1], [1, 0]])
    print tensor(a, 3)

