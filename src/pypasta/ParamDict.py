from copy import deepcopy

import pint

try:
    from typing import Self
except ImportError:
    from typing_extensions import Self
from typing import Union, Dict
import numpy as np
from . import ureg
import pandas as pd


class ParamDict(dict[str, pint.Quantity]):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        keys = list(self.keys())
        self.n_samples = len(self[keys[0]])
        for key in keys[1:]:
            assert self.n_samples == len(self[key])
            assert isinstance(self[key], pint.Quantity)

    def __add__(self, other: Union[Self, Dict[str, pint.Quantity]]) -> Self:
        assert self.keys() == other.keys()
        result_dict = deepcopy(self)
        for key in other.keys():
            result_dict[key] = np.concatenate([self[key], other[key]])
        return result_dict

    def __or__(self, other: Union[Self, Dict[str, pint.Quantity]]) -> Self:
        assert set(self.keys()).isdisjoint(other.keys())
        for param_values in other.values():
            assert len(param_values) == self.n_samples
        return ParamDict(dict(self) | dict(other))

    def __ror__(self, other: Union[Self, Dict[str, pint.Quantity]]) -> Self:
        assert set(self.keys()).isdisjoint(other.keys())
        for param_values in other.values():
            assert len(param_values) == self.n_samples
        return ParamDict(dict(other) | dict(self))

    def __mul__(self, other: Union[Self, Dict[str, pint.Quantity]]) -> Self:
        if not isinstance(other, ParamDict):
            other = ParamDict(other)
        assert set(self.keys()).isdisjoint(other.keys())
        res_dict = {}
        for key in self.keys():
            param_values = np.concatenate([self[key] for _ in range(other.n_samples)])
            res_dict[key] = param_values
        for key in other.keys():
            param_values = ureg.Quantity(np.empty(self.n_samples * other.n_samples), units=other[key].units)
            for ii in range(other.n_samples):
                param_values[ii * self.n_samples:(ii + 1) * self.n_samples] = np.ones(self.n_samples) * other[key][ii]
                res_dict[key] = param_values

        return ParamDict(res_dict)

    def to_data_frame(self) -> pd.DataFrame:
        renamed_dict = {f"{key} [{value.units:~C}]": value.magnitude for key, value in self.items()}
        return pd.DataFrame(renamed_dict)
