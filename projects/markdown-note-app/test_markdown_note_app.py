"""Tests for Markdown Note-Taking App."""


def test_basic():
    """Basic smoke test."""
    import markdown_note_app
    assert hasattr(markdown_note_app, 'main')
    print("✅ Basic test passed")


if __name__ == "__main__":
    test_basic()
    print("\n🎉 All tests passed!")
