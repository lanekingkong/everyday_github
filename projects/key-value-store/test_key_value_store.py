"""Tests for Persistent Key-Value Store."""


def test_basic():
    """Basic smoke test."""
    import key_value_store
    assert hasattr(key_value_store, 'main')
    print("✅ Basic test passed")


if __name__ == "__main__":
    test_basic()
    print("\n🎉 All tests passed!")
