"""Entropy estimation utilities for password strength analysis."""

import math
import string


def shannon_entropy(data: str) -> float:
    """Calculate Shannon entropy of a string."""
    if not data:
        return 0.0
    freq = {}
    for c in data:
        freq[c] = freq.get(c, 0) + 1
    length = len(data)
    entropy = 0.0
    for count in freq.values():
        p = count / length
        entropy -= p * math.log2(p)
    return entropy * length


def unique_chars(password: str) -> int:
    """Count unique character types used."""
    types = 0
    if any(c.islower() for c in password):
        types += 1
    if any(c.isupper() for c in password):
        types += 1
    if any(c.isdigit() for c in password):
        types += 1
    specials = set("!@#$%^&*()-_=+[]{}|;:,.<>?/~`")
    if any(c in specials for c in password):
        types += 1
    return types


def strength_label(entropy: float) -> str:
    if entropy < 28:
        return "Very Weak"
    elif entropy < 36:
        return "Weak"
    elif entropy < 60:
        return "Reasonable"
    elif entropy < 128:
        return "Strong"
    else:
        return "Very Strong"


if __name__ == "__main__":
    test_passwords = ["password", "Password123", "Tr0ub4dor&3", "correct-horse-battery-staple"]
    print("Password Entropy Analysis\n")
    for pw in test_passwords:
        s = shannon_entropy(pw)
        types = unique_chars(pw)
        print(f"  '{pw}'")
        print(f"    Shannon: {s:.1f} bits | Types: {types}/4 | {strength_label(s)}\n")
