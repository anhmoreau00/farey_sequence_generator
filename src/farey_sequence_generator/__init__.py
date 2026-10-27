"""farey_sequence_generator: generate Farey sequences of order n.

A Farey sequence F_n is the sorted list of every reduced fraction
between 0 and 1 whose denominator does not exceed n.

Only the names listed in __all__ below are part of the public API.
"""

from .core import FareyFraction, generate_farey_sequence, farey_length

__all__ = [
    "FareyFraction",
    "generate_farey_sequence",
    "farey_length",
]
