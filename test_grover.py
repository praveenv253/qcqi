#!/usr/bin/env python

from circuit import *
from states import *
from gates import *
from grover import *

def test_oracle():
    print 'Oracle test'
    c = Circuit(3)
    print c.state[-1]                   # |000>
    c.add_gate(H, [1,])
    c.add_gate(H, [2,])
    c.add_gate(H, [3,])
    print c.add_gate(Z, [3,])           # |++->
    print oracle(c, 2, ['00', '11'])    # |000> goes to |001> and vice versa;
                                        # |110> goes to |111> and vice versa

def test_cond_phase_shift():
    print 'Conditional phase shift test'
    print 'Test 1'
    c = Circuit(3)
    print c.state[-1].transpose()           # |000>
    print cond_phase_shift(c).transpose()   # -|000>
    c.add_gate(X, [1,])
    print cond_phase_shift(c).transpose()   # -|100>
    c.add_gate(X, [2,])
    print cond_phase_shift(c).transpose()   # -|110>
    c.add_gate(X, [1,])
    print cond_phase_shift(c).transpose()   # -|010>
    print 'Test 2'
    c = Circuit(5)
    print c.state[-1].transpose()           # |00000>
    print cond_phase_shift(c).transpose()   # -|00000>
    c.add_gate(X, [2,])
    c.add_gate(X, [4,])
    print cond_phase_shift(c).transpose()   # -|01010>
    for i in range(1, 6):
        c.add_gate(X, [i,])
    print cond_phase_shift(c).transpose()   # -|10101>


if __name__ == '__main__':
    test_oracle()
    test_cond_phase_shift()
