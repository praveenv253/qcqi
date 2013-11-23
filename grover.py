import numpy as np
from gates import X

def oracle(circuit, M, targets):
    """
    Constructs the oracle for Grover's search algorithm for a given set of
    target states.

    Parameters
    ----------
    circuit : Circuit
        Quantum circuit to add the oracle to
    M : integer
        Number of target states
    targets : list of strings
        List of target states (in binary) for the Grover's search algorithm

    Returns
    -------
    state : np.ndarray
        State of the system after the application of the oracle.
    """

    state = None
    n = circuit.num_rails
    for target in targets:
        qubits = [n,]       # The last qubit of the oracle is flipped when the
                            # function is 1, and is not flipped when the
                            # function is 0 (y XOR f)
        gate = X.copy()
        t = np.array(list(target), dtype=int)
        one_controls = np.where(t == 1)[0] + 1   # +1 since rails are numbered
                                                 # from 1 to n, not 0 to n-1
        zero_controls = -1 * (np.where(t == 0)[0] + 1)
        controls = np.hstack((one_controls, zero_controls))
        state = circuit.add_gate(gate, qubits, controls)
    return state
