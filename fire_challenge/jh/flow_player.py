import numpy as np
from fire_challenge.challenge_maps import CHALLENGE_MAPS
from numpy.typing import NDArray


def get_map_grid(map_num: int = 0) -> NDArray[np.int64]:
    return CHALLENGE_MAPS[map_num]["grid"]
