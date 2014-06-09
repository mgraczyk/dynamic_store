#!/usr/bin/python3

import sys

import difflib
import itertools
from itertools import repeat
from pprint import pprint
import random

import brancher
import Samples

from brancher import get_value_from_tree
from brancher import BranchData
from brancher import BranchNode

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

def gen_brancher_tests(length, count):
    Ps = ((0.001, 0.1), (0.01, 0.2))
    for ppair in Ps:
        for i in range(count):
            yield Samples.gen_rand_sparse(length, ppair[0], ppair[1])

def rand_brancher_test(length, count):
    trans, depths, comps, totmisses = 0,0,0,0

    for sample in gen_brancher_tests(length, count):
        tree = brancher.make_decision_tree(sample)

        comparisons, misses = test_decision_tree(sample, tree)

        trans += Samples.count_transitions(sample)
        depths += brancher.tree_depth(tree)
        comps += comparisons/length
        totmisses += misses/length

    print("Avg Transitions = {}".format(trans/count))
    print("Avg Depth = {}".format(depths/count))
    print("Avg Comparisons = {}".format(comps/count))
    print("Avg Miss Rate = {}".format(totmisses/comps))
    print()

def brancher_test():
    tests = [
            (((0,1,0,1), (0,0.5,1.0,1.0)),
             BranchNode(BranchData(1,2,0,0),
                BranchNode(BranchData(0,1,1,1),
                    None,
                    None),
                BranchNode(BranchData(2,3,0,1),
                    None,
                    None))
            ),
            (((0,0,0,1,1,0,0,0,1,1), None),
             BranchNode(BranchData(1,5,0,0),
                BranchNode(BranchData(0,3,1,1),
                    None,
                    None),
                BranchNode(BranchData(2,8,0,1),
                    None,
                    None))
            )
        ]

    for i, test in enumerate(tests):
        actual = brancher.make_decision_tree(test[0][0], test[0][1])
        test_decision_tree(test[0][0], actual)
        expected = test[1]
        if actual != expected:
            print("*"*80)
            print("FAIL: Bad brancher result in test case {}.".format(i))
            print()
            print("Expected")
            print(brancher.tree_to_branches(expected, 1))
            print("Actual")
            print(brancher.tree_to_branches(actual, 1))
            print("*"*80)
    print()
    
def main(length, count):
    brancher_test()
    rand_brancher_test(length, count)

if __name__ == "__main__":
    if "h" in sys.argv:
        print("USAGE: {} length [count] [seed]".format(sys.argv[0]))
    else:
        length = int(sys.argv[1]) if len(sys.argv) > 1 else 100
        count =  int(sys.argv[2]) if len(sys.argv) > 2 else 1

        if len(sys.argv) > 3:
            random.seed(sys.argv[3])

        main(length, count)
