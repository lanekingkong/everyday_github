"""Tests for Rate Limiter — Token Bucket & Sliding Window."""


def test_basic():
    """Basic smoke test."""
    import rate_limiter
    assert hasattr(rate_limiter, 'main')
    print("✅ Basic test passed")


if __name__ == "__main__":
    test_basic()
    print("\n🎉 All tests passed!")
