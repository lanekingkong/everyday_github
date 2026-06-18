"""Tests for Text Adventure Game Engine."""


def test_basic():
    """Basic smoke test."""
    import text_adventure
    assert hasattr(text_adventure, 'main')
    print("✅ Basic test passed")


if __name__ == "__main__":
    test_basic()
    print("\n🎉 All tests passed!")
