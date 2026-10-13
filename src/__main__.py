from extract import extract_file
import argparse
from generate import dijkstra
from models import Drone, Hub


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


def run(drone: Drone, path: list, stack: list, zones: Hub, num: int, total: int):
    if total == num:
        stack.append(drone.position)
    total += 1
    for x in path:
        if x != drone.position and x not in stack:
            if zones[x].capacity <= zones[x].drones and x != "goal":
                return None, stack
            zones[x].drones += 1
            zones[stack[-1]].drones -= 1
            drone.position = x
            break
    print(drone)
    print(zones[x])
    return drone, stack


if __name__ == "__main__":
    try:
        args = parse_args()
        start, end, drones, zones, connections = extract_file(args.path)
        num = drones
        path = dijkstra(start, end, zones, connections)
        drones_list = []
        while drones > 0:
            drone = Drone(id_drone=drones, position=start.name, path=path)
            drones_list.append(drone)
            drones -= 1
        while True:
            stack = []
            total = 0
            for i in drones_list:
                result, stack, num = run(i, path, stack, zones, num, total)
                if result is None:
                    continue
                if drones_list[0].position == "goal":
                    break
                i.position = result.position
    except ValueError as e:
        print(e)