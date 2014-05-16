#!/usr/bin/python3

import sys

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

    print("Num Transitions = {}".format(Samples.count_transitions(f)))
    print("Depth = {}".format(brancher.tree_depth(tree)))
    print("Avg Comparisons = {}".format(comparisons/len(f)))
    print("Avg Misses = {}".format(misses/len(f)))
    print()

def brancher_test(N):
    sample = Samples.gen_rand_sparse(N, 0.02, 0.2, 0)
    tree = brancher.make_decision_tree(sample)

    test_decision_tree(sample, tree)
    
def main(N):
    brancher_test(N)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("USAGE: {} N".format(sys.argv[0]))
    else:
        N = int(sys.argv[1])
        main(N)
