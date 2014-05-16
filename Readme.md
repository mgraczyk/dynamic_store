# Dynamic Storage Engine


This module converts constant data structures into compact representations that can be accessed quickly and efficiently.  The structures are organized based on the statistical properties of the underlying data.


## Brancher

Converts predicate functions F(n) : n in Z, n < N -> {0,1} into a branch network.

### Example

```
TODO: Emit C code from decision tree

Samples:
__^^^^^^^^^^______________________^__________________________________________________^^^^^^___^^^^^_
Tree:
|--(3, 35, 1)
|   |--(4, 85, 0)
|   |   |--(5, 91, 0)
|   |   |   |--(6, 94, 0)
|   |   |   |   |--(7, 99, 0)
|   |   |   |   |   |--NULL
|   |   |   |   |   |--NULL
|   |   |   |   |--NULL
|   |   |   |--NULL
|   |   |--NULL
|   |--(1, 12, 1)
|   |   |--(2, 34, 0)
|   |   |   |--NULL
|   |   |   |--NULL
|   |   |--(0, 2, 1)
|   |   |   |--NULL
|   |   |   |--NULL
Num Transitions:
8

Depth:
5

```

## More to come....
