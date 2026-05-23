"""Tests for Markdown to Static HTML Converter."""


def test_basic():
    """Basic smoke test."""
    import markdown_to_html
    assert hasattr(markdown_to_html, 'main')
    print("✅ Basic test passed")


if __name__ == "__main__":
    test_basic()
    print("\n🎉 All tests passed!")
