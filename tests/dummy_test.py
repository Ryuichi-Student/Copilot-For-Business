import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

print(sys.path)

# Import test from backend
from src.backend.test import *


class Backend_Test():
    def t(self):
        return dummy_test()


# Will run any functions of form test_* in this file
# Can import directly from backend and frontend 
    # May need to run pip install -e . in root directory

# Can add @pytest.mark.skip(reason="") to skip tests

def test_one():
    t = Backend_Test()

    assert t.t() == "Backend is operational!"

    print(t.t())


if __name__ == "__main__":
    test_one()

