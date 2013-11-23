#!/usr/bin/env python

from circuit import *
from states import *
from gates import *
from grover import oracle

if __name__ == '__main__':
    print 'Test 1'
    c = Circuit(3)
    print c.state[-1]                   # |000>
    c.add_gate(H, [1,])
    c.add_gate(H, [2,])
    c.add_gate(H, [3,])
    print c.add_gate(Z, [3,])           # |++->
    print oracle(c, 2, ['00', '11'])    # |000> goes to |001> and vice versa;
                                        # |110> goes to |111> and vice versa
