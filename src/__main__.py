from .extract import extract_file
import argparse
from .generate import dijkstra, run
from .models import Drone, Hub, Conections
import sys

def parse_args() -> argparse.Namespace:
    """Parser of the terminal code """
    parser = argparse.ArgumentParser(
        description="Path File to the Maze "
    )
    parser.add_argument(
        "--path",
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
            drone = Drone(id_drone=drones, position=start.name, path=path)
            drones_list.append(drone)
            drones -= 1
        stack = {}
        for drone in drones_list:
            stack[drone.id_drone] = [drone.position]
        ret = run(drones_list, path, stack, zones, end, connections)
        if ret == True:
            sys.exit(0)
    except ValueError as e:
        print(e)