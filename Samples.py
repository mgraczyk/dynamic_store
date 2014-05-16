#!/usr/bin/python3

import sys
import random

import operator

def gen_rand_sticky(N, swp, f0=None, seed=None):
    """ Generates a map f(n) from the first N integers to {0,1}

        If f0 is not given or is none, then f0 will be selected uniformly from {0,1}
        For 0 < n < N, P(f(n) == f(n-1)) == swp
    """

    assert(0 <= swp <= 1)

    if seed is not None:
        random.seed(seed)
    
    if f0 is None:
        f0 = random.choice((0,1))

    f0 = int(f0)
    if swp == 0:
        f = [f0]*N
    elif swp == 1:
        f1 = not f0
        f = [f0, f0]*(N/2) + ([f0] if N % 2 != 0 else [])
    else:
        f = [0]*N
        f[0] = f0

        for i in range(1, N):
            f[i] = f[i-1] ^ (random.random() < swp)
   
    return f

def gen_rand_sparse(N, Pon, Poff, f0=None, seed=None):
    """ Generates a map f(n) from the first N integers to {0,1}
        The map is consists of mostly f0 in {0,1} with some "islands" of ~f0.

        If f0 is not given or is none, then f0 will be selected uniformly from {0,1}

        f can be thought of as a 2 state markov chain with the weights
             S0
            |  ^
        Pon |  | Poff
            V  |
             S1
    """

    assert(0 <= Pon <= 1)
    assert(0 <= Poff <= 1)

    if seed is not None:
        random.seed(seed)
    
    if f0 is None:
        f0 = random.choice((0,1))

    f = [0]*N
    f[0] = int(f0)
    for i in range(1, N):
        r = random.random()
        if f[i-1] == 0:
            fi = f[i-1] ^ (r < Pon)
        else:
            fi = f[i-1] ^ (r < Poff)

        f[i] = fi
        last = fi

    return f

def count_transitions(f):
    trans = 0
    for i in range(1, len(f)):
        if f[i] != f[i-1]:
            trans += 1
    return trans

def terminal_plot(f):
    return "".join("^" if m else "_" for m in f)

def main():
    if len(sys.argv) < 2:
        print("USAGE: {} N".format(sys.argv[0]))
    else:
        N = int(sys.argv[1])
        sample = gen_rand_sparse(N, 0.02, 0.1, 0)
        print("Samples:")
        print(terminal_plot(sample))
        print("P(m == 1):")
        print(sum(sample)*1.0/N)

if __name__ == "__main__":
    main()
