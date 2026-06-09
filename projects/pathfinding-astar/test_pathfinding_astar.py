"""Tests for A* Pathfinding Visualizer."""


def test_basic():
    """Basic smoke test."""
    import pathfinding_astar
    assert hasattr(pathfinding_astar, 'main')
    print("✅ Basic test passed")


if __name__ == "__main__":
    test_basic()
    print("\n🎉 All tests passed!")
