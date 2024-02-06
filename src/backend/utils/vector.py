import numpy as np
from typing import List, Dict

def findClosest(vectordb: Dict[str, List[float]], target: List[float]) -> str:
    dotdb = {index:np.dot(vector, target) for index,vector in vectordb}
    return max(dotdb, key = lambda k: dotdb[k])