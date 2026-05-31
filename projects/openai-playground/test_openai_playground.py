"""Tests for OpenAI API Playground CLI."""


def test_basic():
    """Basic smoke test."""
    import openai_playground
    assert hasattr(openai_playground, 'main')
    print("✅ Basic test passed")


if __name__ == "__main__":
    test_basic()
    print("\n🎉 All tests passed!")
