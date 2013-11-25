import numpy as np

def measure(state, basis='computational'):
    """
    Measures a given state in the given basis, resulting in collapse of the
    quantum state.

    Parameters
    ----------
    state : np.ndarray
        The state to be measured
    basis : string
        One of computational or bell. Determines the basis in which to
        measure the given state

    Returns
    -------
    collapsed_state : np.ndarray
        The state of the system after measurement.
    """

    if basis == 'computational':
        probabilities = state ** 2
        cumulative_prob = np.cumsum(probabilities)
        r = np.random.random()
        # Choose the first occurrence of the cumulative probability shooting
        # higher than our random number
        index = np.where(cumulative_prob > r)[0][0]
        collapsed_state = np.zeros(state.shape)
        collapsed_state[index] = 1
        return collapsed_state
    elif basis == 'bell':
        raise NotImplementedError
    else:
        raise ValueError('Not a recognised basis')

