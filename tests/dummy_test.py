# Import test from backend

import os
import src

# Print current working directory

# from src.backend import test

class test():
    def test():
        # Return current working directory files

        # Print the src directory within the current working directory
        print(dir(src))
        print("=====================================")

        return("Backend is operational")
    


# No module called backend erorr



# Will run any functions of form test_* in this file
# Can import directly from backend and frontend 
    # May need to run pip install -e . in root directory

# Can add @pytest.mark.skip(reason="") to skip tests

def test_one():
    print(test.test())

    assert test.test() =="Backend is operational"

if __name__ == "__main__":
    test_one()

