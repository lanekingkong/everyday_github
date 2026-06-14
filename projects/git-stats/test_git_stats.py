"""Tests for Git Contribution Analyzer."""


def test_basic():
    """Basic smoke test."""
    import git_stats
    assert hasattr(git_stats, 'main')
    print("✅ Basic test passed")


if __name__ == "__main__":
    test_basic()
    print("\n🎉 All tests passed!")
