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


def run(drone: Drone, path: list, stack: dict, zones: Hub):
    for x in path:
        if x != drone.position and x not in stack[drone.id_drone]:
            if zones[x].capacity <= zones[x].drones and x != "goal":
                return None, stack
            zones[x].drones += 1
            zones[drone.position].drones -= 1
            drone.position = x
            break
    print(drone)
    return drone, stack


if __name__ == "__main__":
    try:
        args = parse_args()
        start, end, drones, zones, connections = extract_file(args.path)
        path = dijkstra(start, end, zones, connections)
        drones_list = []
        n = drones
        while drones > 0:
            drone = Drone(id_drone=drones, position=start.name, path=path)
            drones_list.append(drone)
            drones -= 1
        stack = {}
        for drone in drones_list:
            stack[drone.id_drone] = [drone.position]
        finished = False
        while not finished:
            for drone in drones_list:
                result, stack= run(drone, path, stack, zones)
                if result is None:
                    continue
                if result.position == "goal" and result.id_drone == int(1):
                    finished = True
                    break
                stack.setdefault(drone.id_drone, []).append(result.position)
                drone.position = result.position
            print("-------------")
    except ValueError as e:
        print(e)