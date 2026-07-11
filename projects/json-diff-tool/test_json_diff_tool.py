"""Tests for JSON Deep Diff Tool."""


def test_basic():
    """Basic smoke test."""
    import json_diff_tool
    assert hasattr(json_diff_tool, 'main')
    print("✅ Basic test passed")


if __name__ == "__main__":
    test_basic()
    print("\n🎉 All tests passed!")
