from extract import extract_file
import argparse


def parse_args() -> argparse.Namespace:
    """Parser of the terminal code """
    parser = argparse.ArgumentParser(
        description="Path File to the Maze "
    )
    parser.add_argument(
        "path",
        default="data/input/functions_definition.json",
    )
    return parser.parse_args()

if __name__ == "__main__":
    try:
        args = parse_args()
        extract_file(args.path)