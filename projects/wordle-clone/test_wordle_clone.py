"""Tests for Wordle Clone — Terminal Edition."""


def test_basic():
    """Basic smoke test."""
    import wordle_clone
    assert hasattr(wordle_clone, 'main')
    print("✅ Basic test passed")


if __name__ == "__main__":
    test_basic()
    print("\n🎉 All tests passed!")
