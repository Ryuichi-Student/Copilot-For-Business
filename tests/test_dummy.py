import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import test from backend
from src.backend.test import dummy_test

# Will run any functions of form test_* in this file
# Can import directly from backend and frontend 
    # May need to run pip install -e . in root directory

# Can add @pytest.mark.skip(reason="") to skip tests
def test_one():
    assert dummy_test() == "Backend is operational"

if __name__ == "__main__":
    test_one()

