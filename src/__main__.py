from extract import extract_file
import argparse
from generate import dijkstra
from models import Drone

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
        start, end, drones, zones, connections = extract_file(args.path)
        path = dijkstra(start, end, zones, connections)
        drones_list = []
        while drones > 0:
            drone = Drone(id_drone = drones, position = start.name, path = path)
            drones_list += drone
            drones -= 1
        while drones_list:
            run(drones_list)
    except ValueError as e:
        print(e)