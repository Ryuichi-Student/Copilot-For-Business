# IMport test from backend
import backend.test as test


# Will run any functions of form test_* in this file
# Can import directly from backend and frontend 
    # May need to run pip install -e . in root directory

# Can add @pytest.mark.skip(reason="") to skip tests

def test_one():
    print(test.test())

    assert test.test() =="Backend is operational!"

if __name__ == "__main__":
    test_one()

