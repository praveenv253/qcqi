#!/usr/bin/env python

from circuit import *
from states import *
from gates import *

if __name__ == '__main__':
    print 'Test 1'
    c = Circuit(2)
    print c.state[-1]                   # |00>
    print c.add_gate(X, [1,])           # |10>
    print c.add_gate(X, [2,], [1,])     # |11>
    print c.add_gate(H, [1,])           # |-1>
    print c.add_gate(Z, [1,])           # |+1>
    print c.add_gate(H, [2,])           # |+->
    print c.add_gate(Z, [2,])           # |++>
    print c.add_gate(H, [1,])           # |0+>
    print c.add_gate(X, [1,], [2,])     # |00>+|11>
    print
    print 'Test 2'
    c = Circuit(3)
    print c.state[-1]                   # |000>
    print c.add_gate(X, [2,], [-1,])    # |010>
    print c.add_gate(H, [3,])           # |01+>
    print c.add_gate(H, [1,])           # |+1+>
    print c.add_gate(X, [2,], [1,3])    # |010>+|011>+|110>+|101>
