"""Tests for Docker Container Health Monitor."""


def test_basic():
    """Basic smoke test."""
    import docker_healthcheck
    assert hasattr(docker_healthcheck, 'main')
    print("✅ Basic test passed")


if __name__ == "__main__":
    test_basic()
    print("\n🎉 All tests passed!")
