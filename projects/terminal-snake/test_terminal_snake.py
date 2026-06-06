"""Tests for Terminal Snake Game."""


def test_basic():
    """Basic smoke test."""
    import terminal_snake
    assert hasattr(terminal_snake, 'main')
    print("✅ Basic test passed")


if __name__ == "__main__":
    test_basic()
    print("\n🎉 All tests passed!")
