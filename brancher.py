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

def _build_tree(f, t, cdf = None):
    instack = [(0, len(t), 0, len(f))]
    nodes = []

    while instack:
        lo, hi, left, right = instack.pop()

        if lo >= hi:
            nodes.append((True, LeafNode))
        else:
            # Split on the nearest transition to find the partition index
            # TODO: Midpoint computation must change with nonuniform cdf
            if cdf == None:
                mid = (right + left)/2
            else:
                lprob = cdf[left-1] if left else 0.0
                rprob = cdf[right] if right < len(cdf) else 1.0
                mid_p = (lprob + rprob)/2
                mid = minsearch(cdf, mid_p, left, right)

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
        
            if cdf == None:
                direction = Direction.Left if t[pi] > mid else Direction.Right
            else:
                direction = Direction.Right if cdf[t[pi]] <= mid_p else Direction.Left

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

    trans = get_transitions(f)
    if len(trans) == 0:
        return BranchNode(BranchData(0, 0, Direction.Right, f[0]), LeafNode, LeafNode)

    tree = _build_tree(f, trans, cdf)

    return tree

def tree_to_branches(tree, indent=0):
    assert(tree)

    indentStr = "  "*indent
    leftHint = "LIKELY"
    rightHint = "UNLIKELY"
    retfmt = indentStr + "  return {};\n"

    data = tree.data

    hint = leftHint if data.dr == Direction.Left else rightHint
    leftBr = tree_to_branches(tree.lch, indent+1) if tree.lch else retfmt.format(data.val ^ 1)
    rightBr = tree_to_branches(tree.rch, indent+1) if tree.rch else retfmt.format(data.val)

    return "{}if ({}(key < {})) {{\n{}{}}} else {{\n{}{}}}\n".format(
            indentStr, hint, data.key, leftBr, indentStr, rightBr, indentStr)


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
        #sample = Samples.gen_rand_sparse(N, 0.02, .15, 0)
        sample = [0]*10 + [0]*80 + [1, 0, 1]

        print("Samples:")
        print(Samples.terminal_plot(sample))
        print()

        cdf = Samples.hist_to_cdf(sample)

        print("CDF:")
        print(cdf)
        print()

        tree = make_decision_tree(sample, cdf)

        print("Code:")
        print(tree_to_branches(tree))
        print()
        
        print("Num Transitions:")
        print(Samples.count_transitions(sample))
        print()

        print("Depth:")
        print(tree_depth(tree))


if __name__ == "__main__":
    main()
