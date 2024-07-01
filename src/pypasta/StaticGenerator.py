from . import ureg
from .ParamDict import ParamDict
from typing import Dict, List


class StaticGenerator:

    @staticmethod
    def from_toml_table(table: Dict):
        return StaticGenerator(table['values'],
                               table['units'],
                               )

    def __init__(self, parameters: Dict, units: List[str]):
        self.param_dict = parameters
        for param, param_array in self.param_dict.items():
            self.param_dict[param] = param_array * ureg.Unit(units[param])

    def __call__(self) -> ParamDict:
        return ParamDict(self.param_dict)
