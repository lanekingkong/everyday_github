"""Tests for Environment Variable Manager."""


def test_basic():
    """Basic smoke test."""
    import env_manager
    assert hasattr(env_manager, 'main')
    print("✅ Basic test passed")


if __name__ == "__main__":
    test_basic()
    print("\n🎉 All tests passed!")
