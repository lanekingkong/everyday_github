"""Tests for Terminal Pomodoro Timer."""


def test_basic():
    """Basic smoke test."""
    import pomodoro_timer
    assert hasattr(pomodoro_timer, 'main')
    print("✅ Basic test passed")


if __name__ == "__main__":
    test_basic()
    print("\n🎉 All tests passed!")
