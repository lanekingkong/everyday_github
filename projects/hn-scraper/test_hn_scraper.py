"""Tests for Hacker News Top Stories Scraper."""


def test_basic():
    """Basic smoke test."""
    import hn_scraper
    assert hasattr(hn_scraper, 'main')
    print("✅ Basic test passed")


if __name__ == "__main__":
    test_basic()
    print("\n🎉 All tests passed!")
