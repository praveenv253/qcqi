"""
Module to provide the tensorprod function.
"""

import numpy as np


def tensorprod(A, B):
    """
    Computes the tensor product of the 2D matrices A and B. Not efficient for
    large arrays.

    Parameters
    ----------
    A, B : np.ndarray, 2-dimensional
        Input matrices. Order is important.

    Returns
    -------
    C : np.ndarray, 2-dimensional
        C = A tensor B
    """

    if len(A.shape) == 1:
        A = A.reshape(A.shape + (1,))
    C = None
    for i in range(A.shape[0]):
        D = A[i, 0] * B.copy()
        for j in range(1, A.shape[1]):
            D = np.hstack((D, A[i, j] * B.copy()))
        if C is None:
            C = D.copy()
        else:
            C = np.vstack((C, D.copy()))

    return C


def tensor(A, n):
    """
    Computes the tensor product of the 2D matrix A with itself, n times.

    Parameters
    ----------
    A : np.ndarray, 2-dimensional
    n : integer

    Returns
    -------
    An : np.ndarray, 2-dimensional
        A tensored n times
    """

    if n < 0:
        raise ValueError
    if n == 0:
        return np.array([[1,],])
    if n == 1:
        return A
    return tensorprod(tensor(A, n-1), A)
