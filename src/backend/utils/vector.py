import numpy as np
from typing import List, Dict, Union

def closestTable(tableJSON: Dict[str, Dict[str, Union[str, List[float]]]], target: List[float]) -> str:
    dotdb = {index:np.dot(data['embedding'], target) for index,data in tableJSON.items()}
    return max(dotdb, key = lambda k: dotdb[k])