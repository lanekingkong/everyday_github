"""Tests for CSV Data Profiler."""


def test_basic():
    """Basic smoke test."""
    import data_profiler
    assert hasattr(data_profiler, 'main')
    print("✅ Basic test passed")


if __name__ == "__main__":
    test_basic()
    print("\n🎉 All tests passed!")
