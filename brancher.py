#!/usr/bin/python3

import sys
from bisect import bisect_left as minsearch

from collections import namedtuple

import Samples

BranchData = namedtuple("BranchData", ["trnum", "key", "dr", "val"])
BranchNode = namedtuple("BranchNode", ["data", "lch", "rch"])

LeafNode = None

class Direction:
    Left=0
    Right=1

def get_transitions(f):
    t = []
    for i in range(1, len(f)):
        if f[i] != f[i-1]:
            t.append(i)

    return t

def _build_tree(f, t):
    instack = [(0, len(t), 0, len(f))]
    nodes = []

    while instack:
        lo, hi, left, right = instack.pop()

        if lo >= hi:
            nodes.append((True, LeafNode))
        else:
            # Split on the nearest transition to find the partition index
            # TODO: Midpoint computation must change with nonuniform cdf
            mid = (right - left)/2
            ri = minsearch(t, mid, lo, hi)

            if ri == lo:
                pi = lo
            elif ri == hi:
                pi = hi - 1
            else:
                li = ri - 1
                ld = abs(t[li] - mid)
                rd = abs(t[ri] - mid)
                
                if ld < rd:
                    pi = li
                else:
                    pi = ri
          
            # TODO: Also fix directions with cdf
            direction = Direction.Right if t[pi] >= mid else Direction.Left
            newLeft = None if pi+1 == hi else t[pi+1]

            instack.append((lo, pi, left, t[pi]))
            instack.append((pi+1, hi, newLeft, right))
            nodes.append((False, BranchData(pi, t[pi], direction, f[t[pi]])))

        while len(nodes) > 2 and nodes[-1][0] and nodes[-2][0]:
            _, lchild = nodes.pop()
            _, rchild = nodes.pop()
            _, parent = nodes.pop()
            nodes.append((True, BranchNode(parent, lchild, rchild)))

    return nodes[0][1]

def make_decision_tree(f, cdf=None):
    """ f is the function to be encoded.
        cdf is the a posteriori probabilities of the inputs,
            or None to indicate a uniform input space.
    """

    if cdf is not None:
        raise NotImplementedError("nonunifom input cdfs are unimplemented.")

    trans = get_transitions(f)
    if len(trans) == 0:
        return BranchNode(BranchData(0, 0, Direction.Right, f[0]), LeafNode, LeafNode)

    tree = _build_tree(f, trans)

    return tree

def tree_to_branches(tree, indent = 0):
    pass

def get_value_from_tree(tree, key):
    """ Walks the decision tree.
        Returns (value, comparisons, misses)

        value is the computed function value
        comparisons is the number of comparisions used to find value
        misses is the number of incorrectly guesses decisions
    """

    node = tree
    comparisons = 0
    misses = 0
    val = 0
    while node:
        data = node.data
        comparisons += 1
        if key < data.key:
            val = data.val ^ 1
            misses += data.dr == Direction.Right
            node = node.lch
        else:
            val = data.val
            misses += data.dr == Direction.Left
            node = node.rch

    return val, comparisons, misses

def tree_depth(tree):
    maxdepth = 0
    nodes = [(tree, 1)]

    while nodes:
        node, depth = nodes.pop()
        if not node:
            continue

        maxdepth = max(maxdepth, depth)
        nodes.append((node.lch, 1 + depth))
        nodes.append((node.rch, 1 + depth))

    return maxdepth

def print_tree(tree, startindent=0):
    nodes = [(tree, startindent)]
    prestr = "|   "
    while nodes:
        node, indent = nodes.pop()
        if node:
            print(prestr*indent + "|--" + str(node.data))
            nodes.append((node.lch, indent+1))
            nodes.append((node.rch, indent+1))
        else:
            print(prestr*indent + "|--NULL")

def main():
    if len(sys.argv) < 2:
        print("USAGE: {} N".format(sys.argv[0]))
    else:
        N = int(sys.argv[1])
        sample = Samples.gen_rand_sparse(N, 0.02, 0.2, 0)

        print("Samples:")
        print(Samples.terminal_plot(sample))

        tree = make_decision_tree(sample)
        
        print("Tree:")
        print_tree(tree)
        
        print("Num Transitions:")
        print(Samples.count_transitions(sample))
        print()

        print("Depth:")
        print(tree_depth(tree))


if __name__ == "__main__":
    main()
