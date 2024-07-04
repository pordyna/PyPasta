import tomllib
from .HaltonGenerator import HaltonGenerator
from .StaticGenerator import StaticGenerator
from .LinSpace import LinSpace
from functools import reduce
from .ParamDict import ParamDict


def _process_scan_set(scan_set: dict) -> ParamDict:
    method = scan_set['sampling_method']
    if method == "halton":
        generator = HaltonGenerator.from_toml_table(scan_set)
    elif method == "static":
        generator = StaticGenerator.from_toml_table(scan_set)
    elif method == "lin_space":
        generator = LinSpace.from_toml_table(scan_set)
    else:
        raise ValueError(f"Unknown sampling method {method}")
    return generator()


def _process_group(group: dict) -> ParamDict:
    table_type = group.pop('type')
    assert table_type == 'group'
    op = group.pop('combine_method')
    # now there should be only groups and scan_sets left
    if op == "stack_cases":
        return reduce(lambda a, b: _process_table(a) + _process_table(b), group.values())
    if op == "insert_columns":
        return reduce(lambda a, b: _process_table(a) | _process_table(b), group.values())
    if op == "product":
        return reduce(lambda a, b: _process_table(a) * _process_table(b), group.values())
    else:
        raise ValueError(f"Unknown combination method {op}")


def _process_table(table) -> ParamDict:
    if isinstance(table, ParamDict):
        return table
    assert 'type' in table, f"{table}"
    if table['type'] == 'set':
        return _process_scan_set(table)
    if table['type'] == 'group':
        return _process_group(table)
    else:
        raise ValueError(f"Unknown table type {table['type']}")


def process_input(toml_file) -> ParamDict:
    with open(toml_file, "rb") as f:
        scan = tomllib.load(f)
    # at the top there is only one scan_set or one group allowed
    # version param is required
    assert len(scan) == 2, f"{len(scan)} != 2, scan: {scan.keys()}"
    assert "PyPasta_version" in scan.keys()
    assert scan['PyPasta_version'] == '0.0.1'
    assert 'scan' in scan.keys()
    return _process_table(scan['scan'])
