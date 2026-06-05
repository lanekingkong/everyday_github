"""Tests for E-commerce Price Tracker."""


def test_basic():
    """Basic smoke test."""
    import price_tracker
    assert hasattr(price_tracker, 'main')
    print("✅ Basic test passed")


if __name__ == "__main__":
    test_basic()
    print("\n🎉 All tests passed!")
