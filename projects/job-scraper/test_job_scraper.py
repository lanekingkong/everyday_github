"""Tests for Job Listing Aggregator."""


def test_basic():
    """Basic smoke test."""
    import job_scraper
    assert hasattr(job_scraper, 'main')
    print("✅ Basic test passed")


if __name__ == "__main__":
    test_basic()
    print("\n🎉 All tests passed!")
