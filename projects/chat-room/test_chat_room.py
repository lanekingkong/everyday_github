"""Tests for WebSocket Chat Room."""


def test_basic():
    """Basic smoke test."""
    import chat_room
    assert hasattr(chat_room, 'main')
    print("✅ Basic test passed")


if __name__ == "__main__":
    test_basic()
    print("\n🎉 All tests passed!")
