"""Tests for Text Classifier with TF-IDF + Naive Bayes."""


def test_basic():
    """Basic smoke test."""
    import text_classifier
    assert hasattr(text_classifier, 'main')
    print("✅ Basic test passed")


if __name__ == "__main__":
    test_basic()
    print("\n🎉 All tests passed!")
