from . import ureg
from .ParamDict import ParamDict
from typing import Dict, List
import numpy as np


class LinSpace:
    @staticmethod
    def from_toml_table(table: Dict):
        return LinSpace(table['start'],
                        table['stop'],
                        table['n_samples'],
                        table['endpoint'],
                        table['name'],
                        table['units'],

                        )

    def __init__(self, start: float, stop: float, n_samples: int, endpoint: bool, name: str, units: Dict[str, str]):

        self.param_dict = {name: np.linspace(start,
                                             stop, n_samples,
                                             endpoint=endpoint) * ureg.Unit(units[name])}

    def __call__(self) -> ParamDict:
        return ParamDict(self.param_dict)
