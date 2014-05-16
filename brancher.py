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
    tracker = []

    while instack:
        lo, hi, left, right = instack.pop()

        if lo >= hi:
            nodes.append(None)
            tracker.append(0)
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
            nodes.append((pi, t[pi], direction))
            tracker.append(1)

        while len(tracker) > 2 and \
           (tracker[-1] == 0 or tracker[-1] == 2) and \
           (tracker[-2] == 0 or tracker[-2] == 2):
            tracker.pop()
            tracker.pop()
            tracker.pop()
            tracker.append(2)

            lchild = nodes.pop()
            rchild = nodes.pop()
            parent = nodes.pop()
            nodes.append((parent, (lchild, rchild)))

    return nodes[0]

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
    if tree:
        ld = tree_depth(tree[1][0])
        rd = tree_depth(tree[1][1])
        return 1 + max(ld, rd)
    else:
        return 0

def print_tree(tree, indent=0):
    prestr = "|   "
    if tree:
        print(prestr*indent + "|--" + str(tree[0]))
        print_tree(tree[1][0], indent+1)
        print_tree(tree[1][1], indent+1)
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
        depth = tree_depth(tree)
        
        print("Tree:")
        print_tree(tree)
        
        print("Num Transitions:")
        print(Samples.count_transitions(sample))
        print()

        print("Depth:")
        print(depth)


if __name__ == "__main__":
    main()
