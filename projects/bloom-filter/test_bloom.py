"""Tests for BloomFilter implementation."""
from bloom_filter import BloomFilter


def test_basic():
    bf = BloomFilter(expected_items=100, false_positive_rate=0.01)
    bf.add("hello")
    bf.add("world")
    assert bf.contains("hello")
    assert bf.contains("world")
    assert not bf.contains("missing")
    print("✅ Basic test passed")


def test_false_positive_rate():
    bf = BloomFilter(expected_items=1000, false_positive_rate=0.05)
    known = set()
    for i in range(1000):
        item = f"item_{i}"
        bf.add(item)
        known.add(item)

    fps = 0
    trials = 10000
    for i in range(1000, 1000 + trials):
        if bf.contains(f"item_{i}"):
            fps += 1

    actual_fp = fps / trials
    print(f"  Expected FP: ≤5%, Actual: {actual_fp:.2%}")
    assert actual_fp < 0.10, f"FP rate too high: {actual_fp:.2%}"
    print(f"✅ FP rate test passed ({actual_fp:.2%})")


if __name__ == "__main__":
    test_basic()
    test_false_positive_rate()
    print("\n🎉 All tests passed!")
