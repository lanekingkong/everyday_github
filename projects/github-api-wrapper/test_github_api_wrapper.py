"""Tests for GitHub REST API Python Wrapper."""


def test_basic():
    """Basic smoke test."""
    import github_api_wrapper
    assert hasattr(github_api_wrapper, 'main')
    print("✅ Basic test passed")


if __name__ == "__main__":
    test_basic()
    print("\n🎉 All tests passed!")
