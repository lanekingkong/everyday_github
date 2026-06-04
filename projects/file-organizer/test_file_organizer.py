"""Tests for Smart File Organizer."""


def test_basic():
    """Basic smoke test."""
    import file_organizer
    assert hasattr(file_organizer, 'main')
    print("✅ Basic test passed")


if __name__ == "__main__":
    test_basic()
    print("\n🎉 All tests passed!")
