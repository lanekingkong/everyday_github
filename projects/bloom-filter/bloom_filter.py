"""
Bloom Filter — Space-efficient probabilistic set membership test.
Supports configurable false-positive rate and multiple hash functions.
"""
import math
import hashlib
import struct


class BloomFilter:
    """
    Probabilistic data structure for set membership.

    False positives: possible (says "maybe in set")
    False negatives: impossible (never says "definitely not in set" when it is)
    """

    def __init__(self, expected_items: int = 1000, false_positive_rate: float = 0.01):
        """
        Args:
            expected_items: Estimated number of items to store
            false_positive_rate: Acceptable false positive probability (0.01 = 1%)
        """
        self.expected_items = expected_items
        self.fp_rate = false_positive_rate

        # Optimal bit array size: m = -n*ln(p) / (ln(2))^2
        self.bit_size = int(
            -(expected_items * math.log(false_positive_rate)) / (math.log(2) ** 2)
        )

        # Optimal number of hash functions: k = (m/n) * ln(2)
        self.hash_count = int((self.bit_size / expected_items) * math.log(2))

        self.bit_array = 0  # Use Python's arbitrary-precision int as bit array

        self._items_added = 0

    def _hashes(self, item: str):
        """Generate k hash values using double hashing technique."""
        h = hashlib.sha256(item.encode()).digest()
        h1, h2 = struct.unpack("!QQ", h[:16])
        for i in range(self.hash_count):
            yield (h1 + i * h2) % self.bit_size

    def add(self, item: str) -> None:
        """Add an item to the filter."""
        for idx in self._hashes(item):
            self.bit_array |= (1 << idx)
        self._items_added += 1

    def contains(self, item: str) -> bool:
        """Check if an item might be in the set."""
        for idx in self._hashes(item):
            if not (self.bit_array & (1 << idx)):
                return False
        return True

    @property
    def stats(self) -> dict:
        """Current filter statistics."""
        # Estimate fill ratio
        bits_set = self.bit_array.bit_count()
        fill = bits_set / self.bit_size

        # Current actual false positive rate
        actual_fp = fill ** self.hash_count

        return {
            "bit_size": self.bit_size,
            "hash_functions": self.hash_count,
            "items_added": self._items_added,
            "bits_set": bits_set,
            "fill_ratio": f"{fill:.1%}",
            "estimated_fp_rate": f"{actual_fp:.4%}",
            "memory_bytes": self.bit_size // 8,
        }


if __name__ == "__main__":
    bf = BloomFilter(expected_items=5000, false_positive_rate=0.01)

    print("═══ Bloom Filter Demo ═══\n")
    print(f"Config: {bf.expected_items} items @ {bf.fp_rate:.0%} FP rate")
    print(f"Bit array: {bf.bit_size:,} bits ({bf.bit_size//8:,} bytes)")
    print(f"Hash functions: {bf.hash_count}\n")

    # Add items
    words = ["apple", "banana", "cherry", "date", "elderberry",
             "fig", "grape", "honeydew", "kiwi", "lemon"]
    for w in words:
        bf.add(w)

    print(f"Added {len(words)} items\n")

    # Test membership
    tests = ["apple", "banana", "mango", "orange", "cherry", "papaya"]
    print("Testing membership:")
    for w in tests:
        in_set = w in words
        maybe_in = bf.contains(w)
        status = "✅" if in_set == maybe_in else ("⚠️  FP!" if maybe_in else "❌ FN!")
        print(f"  {w:12s} → In set: {str(in_set):5s} | BF says: {str(maybe_in):5s} {status}")

    print(f"\n{bf.stats}")
