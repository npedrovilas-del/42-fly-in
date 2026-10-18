from .extract import extract_file
import argparse
from .generate import run, multiple_paths
from .models import Drone
import sys


def parse_args() -> argparse.Namespace:
    """Parser of the terminal code/path."""
    parser = argparse.ArgumentParser(
        description="Path File to the Maze "
    )
    parser.add_argument(
        "--path",
        default="maps/challenger/01_the_impossible_dream.txt",
    )
    return parser.parse_args()


if __name__ == "__main__":
    try:
        args = parse_args()
        start, end, drones, zones, connections = extract_file(args.path)
        drones_list = []
        i = 1
        while i <= drones:
            drone = Drone(id_drone=i, position=start.name)
            drones_list.append(drone)
            i += 1
        multiple_paths(drones_list, start, end, zones, connections)
        run(drones_list, zones, end, connections, start)
    except ValueError as e:
        print(e)
        sys.exit(1)
