"""Tests for Consistent Hashing Ring."""


def test_basic():
    """Basic smoke test."""
    import consistent_hashing
    assert hasattr(consistent_hashing, 'main')
    print("✅ Basic test passed")


if __name__ == "__main__":
    test_basic()
    print("\n🎉 All tests passed!")
