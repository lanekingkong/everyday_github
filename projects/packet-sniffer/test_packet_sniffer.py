"""Tests for Network Packet Analyzer."""


def test_basic():
    """Basic smoke test."""
    import packet_sniffer
    assert hasattr(packet_sniffer, 'main')
    print("✅ Basic test passed")


if __name__ == "__main__":
    test_basic()
    print("\n🎉 All tests passed!")
