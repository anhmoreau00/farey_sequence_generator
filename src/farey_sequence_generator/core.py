from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class FareyFraction:
    """An immutable, reduced fraction in the closed interval [0, 1].

    Every fraction produced by :func:`generate_farey_sequence` is already
    in lowest terms, so no further reduction is needed by callers.
    """

    numerator: int
    denominator: int

    def __post_init__(self) -> None:
        if self.denominator <= 0:
            raise ValueError(
                f"denominator must be positive, got {self.denominator}"
            )
        if not (0 <= self.numerator <= self.denominator):
            raise ValueError(
                "fraction must lie in [0, 1]; "
                f"got {self.numerator}/{self.denominator}"
            )

    def value(self) -> float:
        """Return the floating-point value of the fraction.

        This is a convenience only — the exact rational value is what the
        sequence guarantees.  Float conversion can lose precision for
        large numerators or denominators.
        """
        return self.numerator / self.denominator


def generate_farey_sequence(n: int) -> List[FareyFraction]:
    """Return the Farey sequence of order ``n`` as a list of fractions.

    The result always starts with ``0/1`` and ends with ``1/1`` is NOT
    included: by the standard definition used here, F_n lists every
    reduced fraction in the closed interval [0, 1], so the final term is
    ``1/1``.  Each adjacent pair of terms has the mediant property
    ``b*c - a*d == 1``.

    ``n`` must be a positive integer.  ``n == 1`` yields ``[0/1, 1/1]``.

    Raises:
        ValueError: if ``n`` is less than 1.
    """
    if n < 1:
        raise ValueError(f"order must be >= 1, got {n}")

    # Seed with the first two terms of every Farey sequence.
    # They are 0/1 and 1/n, because 1/n is the smallest positive fraction
    # with denominator <= n.
    a, b = 0, 1
    c, d = 1, n

    terms: List[FareyFraction] = [FareyFraction(a, b)]

    # Walk forward until we reach 1/1, which is the last term of F_n.
    while not (c == 1 and d == 1):
        terms.append(FareyFraction(c, d))
        k = (n + b) // d
        a, b, c, d = c, d, k * c - a, k * d - b

    terms.append(FareyFraction(1, 1))
    return terms


def farey_length(n: int) -> int:
    """Return the number of terms in the Farey sequence of order ``n``.

    This is ``1 + sum_{m=1..n} phi(m)`` where phi is Euler's totient.
    Computed directly here without needing the sequence itself, which is
    useful when you only need the count.

    Raises:
        ValueError: if ``n`` is less than 1.
    """
    if n < 1:
        raise ValueError(f"order must be >= 1, got {n}")

    # Euler's totient via trial division.  Fine for the moderate n this
    # library is intended for; a sieve would be faster for very large n
    # but would complicate the zero-dependency story.
    def totient(m: int) -> int:
        result = m
        x = m
        p = 2
        while p * p <= x:
            if x % p == 0:
                while x % p == 0:
                    x //= p
                result -= result // p
            p += 1
        if x > 1:
            result -= result // x
        return result

    return 1 + sum(totient(m) for m in range(1, n + 1))
