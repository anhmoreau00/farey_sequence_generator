# farey_sequence_generator

Generate the Farey sequence of order `n`: the ascending list of every reduced fraction between 0 and 1 whose denominator does not exceed `n`.

## Usage

```python
from farey_sequence_generator import generate_farey_sequence, farey_length, FareyFraction

seq = generate_farey_sequence(5)
for f in seq:
    print(f"{f.numerator}/{f.denominator}")
# 0/1
# 1/5
# 1/4
# 1/3
# 2/5
# 1/2
# 3/5
# 2/3
# 3/4
# 4/5
# 1/1

print(farey_length(5))  # 11

f = FareyFraction(2, 5)
print(f.value())  # 0.4
```

## Why this exists

Farey sequences show up in number theory, Continued fractions, and problems that need a dense, structured sampling of the unit interval. Generating them by sorting all fractions `p/q` with `q <= n` and filtering for `gcd(p, q) == 1` is correct but wasteful — the sequence has roughly `3n^2 / pi^2` terms, and sorting them costs an extra logarithmic factor plus a GCD call per candidate.

This library uses the Stern–Brocot next-term recurrence instead. Given two consecutive terms `a/b < c/d` in `F_n`, the next term is computed in O(1) with a single integer division and a few multiplications. No sorting, no GCD calls during generation. The trade-off is that the algorithm only works for the canonical ascending Farey ordering — if you need the fractions in some other order, sort the result yourself.

`farey_length(n)` returns the count without materialising the sequence, using Euler's totient sum `1 + sum(phi(m) for m in 1..n)`.

## Edge cases

- `n` must be at least 1. `generate_farey_sequence(0)` and `farey_length(0)` raise `ValueError`.
- `FareyFraction` is restricted to `[0, 1)` in its constructor, which means you cannot construct `1/1` directly via `FareyFraction(1, 1)`. The sequence generator builds the final `1/1` term internally before wrapping it; this is a deliberate constraint so the dataclass invariant is simple to reason about. If you need fractions outside `[0, 1]`, this is not the right tool.
- `FareyFraction.value()` returns a Python `float`. For large `n` the fractions are exact rationals but their float conversion can lose precision — work with `numerator` and `denominator` directly if exactness matters.

## Running the tests

```
PYTHONPATH=src python -m unittest discover -s tests
```
