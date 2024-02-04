import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.backend.actioner import Actioner


def test_requirements():
    actioner = Actioner()

    # Simple test
    requirements = actioner.get_requirements("What is the average salary of a data scientist?")
    print(requirements)
    assert len(requirements) == 1

    # Test with multiple requirements
    requirements = actioner.get_requirements("What are our most popular products?")
    print(requirements)
    assert 1 < len(requirements) == len(set(requirements))


if __name__ == "__main__":
    test_requirements()