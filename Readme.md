# Dynamic Storage Engine


This module converts constant data structures into compact representations that can be accessed quickly and efficiently.  The structures are organized based on the statistical properties of the underlying data.


## Brancher

Converts predicate functions F(n) : n in Z, n < N -> {0,1} into a branch network.

### Example

```
Samples:
________________________________^^^^____________________________________^^^^^__________________^^___________________________________________________^^^^^^^^^^^___________________________________________________________^^________________________________________________________________________________
Tree:
|--BranchData(trnum=6, key=148, dr=1, val=1)
|   |--BranchData(trnum=9, key=220, dr=1, val=0)
|   |   |--NULL
|   |   |--BranchData(trnum=8, key=218, dr=0, val=1)
|   |   |   |--NULL
|   |   |   |--BranchData(trnum=7, key=159, dr=1, val=0)
|   |   |   |   |--NULL
|   |   |   |   |--NULL
|   |--BranchData(trnum=2, key=72, dr=1, val=1)
|   |   |--BranchData(trnum=5, key=97, dr=1, val=0)
|   |   |   |--NULL
|   |   |   |--BranchData(trnum=4, key=95, dr=0, val=1)
|   |   |   |   |--NULL
|   |   |   |   |--BranchData(trnum=3, key=77, dr=1, val=0)
|   |   |   |   |   |--NULL
|   |   |   |   |   |--NULL
|   |   |--BranchData(trnum=1, key=36, dr=0, val=0)
|   |   |   |--NULL
|   |   |   |--BranchData(trnum=0, key=32, dr=0, val=1)
|   |   |   |   |--NULL
|   |   |   |   |--NULL

Code:
if (UNLIKELY(key < 148)) {
  if (UNLIKELY(key < 72)) {
    if (LIKELY(key < 36)) {
      if (LIKELY(key < 32)) {
        return 0;
      } else {
        return 1;
      }
    } else {
      return 0;
    }
  } else {
    if (UNLIKELY(key < 97)) {
      if (LIKELY(key < 95)) {
        if (UNLIKELY(key < 77)) {
          return 1;
        } else {
          return 0;
        }
      } else {
        return 1;
      }
    } else {
      return 0;
    }
  }
} else {
  if (UNLIKELY(key < 220)) {
    if (LIKELY(key < 218)) {
      if (UNLIKELY(key < 159)) {
        return 1;
      } else {
        return 0;
      }
    } else {
      return 1;
    }
  } else {
    return 0;
  }
}


Num Transitions:
10

Depth:
5

```

## More to come....
