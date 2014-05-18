#!/usr/bin/python3

import sys

import difflib
import itertools
from itertools import repeat
from pprint import pprint

import brancher
import Samples

from brancher import get_value_from_tree

def functional_fail(f, tree, treeVal, key):
    print("FAIL: Value mismatch")
    print("\tFound f({}) == {}, not {}".format(key, f[key], treeVal))

    #print("Samples:")
    #print(Samples.terminal_plot(f))

    #print("Tree:")
    #brancher.print_tree(tree)

    exit(1)

def test_decision_tree(f, tree):
    comparisons  = 0
    misses = 0
    for key,fv in enumerate(f):
        tv, comp, miss = get_value_from_tree(tree, key)

        if tv != fv:
            functional_fail(f, tree, tv, key)

        comparisons += comp
        misses += miss

    return comparisons, misses

def brancher_test(length, count):
    trans, depths, comps, totmisses = 0,0,0,0
    for i in range(count):
        sample = Samples.gen_rand_sparse(length, 0.005, 0.1, 0)
        tree = brancher.make_decision_tree(sample)

        comparisons, misses = test_decision_tree(sample, tree)

        trans += Samples.count_transitions(sample)
        depths += brancher.tree_depth(tree)
        comps += comparisons/length
        totmisses += misses/length

        flatcdf = Samples.hist_to_cdf(repeat(1, length))
        nocdf = brancher.tree_to_branches(tree)
        cdf = brancher.tree_to_branches(brancher.make_decision_tree(sample, flatcdf))
        if nocdf != cdf:
            print("Use of CDF changed output!")
            diff = list(difflib.Differ().compare(cdf, nocdf))
            pprint(diff)

    print("Avg Transitions = {}".format(trans/count))
    print("Avg Depth = {}".format(depths/count))
    print("Avg Comparisons = {}".format(comps/count))
    print("Avg Misses = {}".format(totmisses/count))
    print()

    
def main(length, count):
    brancher_test(length, count)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("USAGE: {} length [count]".format(sys.argv[0]))
    else:
        length = int(sys.argv[1])
        count =  int(sys.argv[2]) if len(sys.argv) > 2 else 1
        main(length, count)
