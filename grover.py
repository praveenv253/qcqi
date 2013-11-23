import numpy as np

from gates import X, Z, H
from tensorprod import tensor


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


def cond_phase_shift(circuit):
    """
    Performs the conditional phase shift operation 2|0><0| - I on the given
    circuit.

    Parameters
    ----------
    circuit : Circuit
        Quantum circuit to apply the conditional phase shift operation on

    Returns
    -------
    state : np.ndarray
        State of the system after the application of the conditional phase
        shift operation.
    """

    n = circuit.num_rails
    state = None

    # First, invert all qubits
    for i in range(1, n):
        qubits = [i,]
        gate = X.copy()
        circuit.add_gate(gate, qubits)

    # Then, apply a Z operation on any one qubit, with a control from all other
    # input qubits. This will ensure that the state gets negated only when it
    # is |111...1>
    gate = Z.copy()
    qubits = [n-1,]
    controls = range(1, n-1)
    circuit.add_gate(gate, qubits, controls)

    # Finally, invert everything back, so that only |000...0> would have
    # suffered negation
    for i in range(1, n):
        qubits = [i,]
        gate = X.copy()
        state = circuit.add_gate(gate, qubits)

    return state


def iterator(circuit, M, targets):
    """
    Builds and adds a Grover iterator for the given targets to the given
    cicuit.

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

    n = circuit.num_rails

    # First, apply the oracle
    oracle(circuit, M, targets)

    # Now, we need to perform the inversion-about-the-mean operation

    # So, first apply the n-qubit Hadamard gate on the first n-1 rails
    for i in range(1, n):
        circuit.add_gate(H, [i,])

    # Then apply the conditional phase shift operation
    cond_phase_shift(circuit)

    # Finally, reapply the n-qubit Hadamard gate
    state = None
    for i in range(1, n):
        state = circuit.add_gate(H, [i,])

    return state
