from scipy.stats import qmc
from . import ureg
from .ParamDict import ParamDict
from typing import Dict, List


class HaltonGenerator:

    @staticmethod
    def from_toml_table(table: Dict):
        return HaltonGenerator(table['bounds'],
                               table['n_samples'],
                               table['units'],
                               table['seed'],
                               )

    def __init__(self, bounds: Dict, n_samples: int, units: Dict[str, str], seed: int):
        self.bounds = bounds
        self.parameters = list(bounds.keys())
        self.n_samples = n_samples
        self._l_bounds = [bound[0] for bound in self.bounds.values()]
        self._u_bounds = [bound[1] for bound in self.bounds.values()]
        self.units = units
        n_dims = len(self.parameters)
        self.sampler = qmc.Halton(d=n_dims, seed=seed, scramble=True)

    def __call__(self) -> ParamDict:
        samples = self.sampler.random(self.n_samples)
        samples = qmc.scale(samples, self._l_bounds, self._u_bounds)
        param_dict = {}
        for ii, param in enumerate(self.parameters):
            param_dict[param] = samples[:, ii] * ureg.Unit(self.units[param])
        return ParamDict(param_dict)
