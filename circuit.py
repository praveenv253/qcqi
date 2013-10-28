"""Provides the class Circuit, to build a quantum computing circuit."""

import numpy as np

from states import zero, one
from gates import I, X
from tensorprod import tensor, tensorprod

class Circuit(object):
    """
    Circuit(num_rails, initial_state=0)

    Defines a quantum computational circuit.
    Allows one to define the number of rails in the circuit, add gates to any
    number of rails, etc.
    Records the state of the circuit after the addition of each gate.

    Parameters
    ----------
    num_rails : integer
        Number of rails in the circuit.
    initial_state : np.ndarray
        Initial state vector of all rails. Must be either the qubit-wise state
        or the joint state. If the definition is qubit-wise, then the qubits
        must be either |0> or |1>.
        => Must have either num_rails of 2^num_rails number of entries.
    """

    def __init__(self, num_rails, initial_state=0):
        self.num_rails = num_rails
        self.state = []
        self.gates = []
        if initial_state:
            if initial_state.shape == [num_rails, 1]:
                # Qubit-wise definition.
                state = None
                for qubit in initial_state:
                    if qubit == 0:
                        if state is None:
                            state = zero
                        else:
                            state = tensorprod(state, zero)
                    elif qubit == 1:
                        if state is None:
                            state = one
                        else:
                            state = tensorprod(state, one)
                    else:
                        raise ValueError('Qubit can only be either 0 or 1')
            else:
                if initial_state.shape != [num_rails ** 2, 1]:
                    # Not a full description.
                    raise ValueError('Incomplete or improper definition of'
                                     ' initial_state')
        else:
            initial_state = tensor(zero, num_rails)
        self.state.append(initial_state)

    def add_gate(self, gate, qubits, controls=[]):
        """
        Add a gate to the circuit.

        Can currently handle only single-qubit gates with one or more controls.

        Parameters
        ----------
        gate : np.ndarray
            2D matrix defining the transformation. Must be unitary. Size of the
            matrix must be (NxN) where N is 2^len(qubits)
        qubits : list
            List of rail or qubit numbers upon which this gate acts. Numbers
            must be between 1 and num_rails.
        controls : list
            Control qubits upon which this gate depends. Absolute value of
            qubit numbers must be between 1 and num_rails. Use a negative sign
            to indicate 0-control.

        Returns
        -------
        state : np.ndarray
            (num_rails x 1) dimensional state vector after successful
            application of the gate.
        """

        # Implementation notes:
        #
        # 1. Currently computing whole operator matrix for the entire state
        #    space from the single-qubit gate, the qubit being operated upon
        #    and the control qubits.
        # 2. Qubit-wise computations are not feasible, because we would then
        #    have to operate multi-qubit gates on some qubits *only*, which
        #    would be difficult because it is hard to extract qubits from the
        #    system state.
        # 3. Implementing control by looking at the probability of the control
        #    qubit being 0 or 1 and then applying the operation with that
        #    probability is harder than simply writing out the whole operation
        #    matrix.

        n = len(qubits)
        N = 2 ** n
        if gate.shape != (N, N):
            raise ValueError('Gate is of improper shape')
        if n != 1 or gate.shape != (2, 2):
            raise NotImplementedError('Cannot handle gates that are not single'
                                      '-qubit')
        controls = np.array(controls)

        # First, determine the x-operator, to invert zero-control rails.
        x_operator = np.array([[1,],])
        for i in xrange(1, self.num_rails+1):
            if i in abs(controls):
                if controls[np.where(abs(controls) == i)] < 0:
                    # Zero-control
                    x_operator = tensorprod(x_operator, X)
                else:
                    x_operator = tensorprod(x_operator, I)
            else:
                x_operator = tensorprod(x_operator, I)

        # Now, determine the actual operation of the gate itself.
        operator = np.array([[1,],])
        for i in xrange(1, self.num_rails+1):
            if i in qubits:
                if i in abs(controls):
                    raise ValueError('A qubit cannot be used for the gate and'
                                     ' also be a control')
                else:
                    operator = tensorprod(operator, gate)
            else:
                # Ignore control qubits for now. Treat them like identity.
                operator = tensorprod(operator, I)

        # Now go back and identify (pun intended) parts of the operator where
        # there is control.
        controls = abs(controls)
        controls.sort()
        # Identity is a big I block that will be used to wipe out those places
        # where there should have been a control, but we put a gate instead.
        identity = tensor(I, self.num_rails-1)
        for i in controls[::-1]:
            # Block size is the number of contiguous 0's that appear at the
            # i'th qubit when you write the binary numbers in order.
            block_size = 2 ** (self.num_rails - i)
            # We start with one square of dimension (block_size x block_size)
            # at the (0, 0) index and make it identity. We then skip one
            # block, go to the third block starting from (0, 0) and repeat.
            # We do this both sideways and downwards. That effectively adds
            # the requisite control to the entire operator.
            for j in xrange(0, 2**self.num_rails, 2*block_size):
                for k in xrange(0, 2**self.num_rails, 2*block_size):
                    # p and q are starting positions of blocks of dimension
                    # (block_size x block_size) in indentity. These are
                    # required because identity is only half as big in side
                    # length when compared with operator.
                    p = j / 2
                    q = k / 2
                    operator[j:j+block_size, k:k+block_size] = (
                        identity[p:p+block_size, q:q+block_size]
                    )

        # Compute the overall gate matrix
        gate_matrix = np.dot(x_operator, np.dot(operator, x_operator))
        # Compute and return the state after application of the gate
        state = np.dot(gate_matrix, self.state[-1])
        self.state.append(state)
        return state

