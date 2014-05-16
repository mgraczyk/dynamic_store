#!/usr/bin/python3

import sys
from bisect import bisect_right as minsearch

import Samples

class Direction:
    Left=0
    Right=1

def get_transitions(f):
    t = []
    for i in range(1, len(f)):
        if f[i] != f[i-1]:
            t.append(i)

    return t

def _build_tree(t, lo, hi, left, right):
    instack = [(lo, hi, left, right)]
    nodes = []

    while instack:
        lo, hi, left, right = instack.pop()

        if lo >= hi:
            nodes.append((True, None))
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
            direction = Direction.Left if t[pi] > mid else Direction.Right
            newLeft = None if pi+1 == hi else t[pi+1]

            instack.append((pi+1, hi, newLeft, right))
            instack.append((lo, pi, left, t[pi]))
            nodes.append((False, (pi, t[pi], direction)))

        while len(nodes) > 2 and nodes[-1][0] and nodes[-2][0]:
            _, lchild = nodes.pop()
            _, rchild = nodes.pop()
            _, parent = nodes.pop()
            nodes.append((True, (parent, (lchild, rchild))))

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
        return ((0, Direction.Right), (None, None))

    tree = _build_tree(trans, 0, len(trans), 0, len(f))

    return tree

def tree_to_branches(tree, indent = 0):
    pass

def tree_depth(tree):
    maxdepth = 0
    nodes = [(tree, 1)]

    while nodes:
        node, depth = nodes.pop()
        maxdepth = max(maxdepth, depth)
        if not node:
            continue

        nodes.append((node[1][0], 1 + depth))
        nodes.append((node[1][1], 1 + depth))

    return maxdepth

def print_tree(tree, startindent=0):
    nodes = [(tree, startindent)]
    prestr = "|   "
    while nodes:
        node, indent = nodes.pop()
        if node:
            print(prestr*indent + "|--" + str(node[0]))
            nodes.append((node[1][0], indent+1))
            nodes.append((node[1][1], indent+1))
        else:
            print(prestr*indent + "|--NULL")

def main():
    if len(sys.argv) < 2:
        print("USAGE: {} N".format(sys.argv[0]))
    else:
        N = int(sys.argv[1])
        sample = Samples.gen_rand_sparse(N, 1, 1, 0)

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
