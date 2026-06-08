"""Tests for SQL Query Parser & Optimizer."""


def test_basic():
    """Basic smoke test."""
    import query_parser
    assert hasattr(query_parser, 'main')
    print("✅ Basic test passed")


if __name__ == "__main__":
    test_basic()
    print("\n🎉 All tests passed!")
