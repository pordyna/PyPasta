import argparse
from pathlib import Path
from .read_input import process_input

def run_pypasta_cli():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--version', action='version')
    arg_parser.add_argument('input_file', type=lambda f: Path(f).resolve())
    arg_parser.add_argument('--output_file', type=lambda f: Path(f).resolve(), default=Path.cwd() / 'scan.csv')

    args = arg_parser.parse_args()
    parameters = process_input(args.input_file)
    parameters = parameters.to_data_frame()
    parameters.to_csv(args.output_file, index_label="case_index")
