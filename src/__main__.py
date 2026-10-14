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

def run(drone: Drone, path: list, stack: dict, zones: Hub, end: Hub, connections: Connections):
    if drone.transit is not None:
        for i in connections[drone.position]:
            if i.name_1 == drone.transit or i.name_2 == drone.transit:
                i.move += 1
        zones[drone.position].drones -= 1
        drone.position = drone.transit
        drone.transit = None
        return drone, stack
    for x in path:
        if x != drone.position and x not in stack[drone.id_drone]:
            for i in connections[drone.position]:
                if i.name_1 == x or i.name_2 == x:
                    link = i
                    if i.move >= i.capacity:
                        return None, stack
            if zones[x].capacity <= zones[x].drones and x != end.name:
                return None, stack
            zones[x].drones += 1
            link.move += 1
            if zones[x].zone == "restricted":
                drone.transit = x
                return drone, stack
            zones[drone.position].drones -= 1
            drone.position = x
            break
    return drone, stack


if __name__ == "__main__":
    try:
        args = parse_args()
        start, end, drones, zones, connections = extract_file(args.path)
        path = dijkstra(start, end, zones, connections)
        drones_list = []
        n = drones
        i = 0
        while drones > 0:
            drone = Drone(id_drone=drones, position=start.name, path=path)
            drones_list.append(drone)
            drones -= 1
        stack = {}
        for drone in drones_list:
            stack[drone.id_drone] = [drone.position]
        finished = False
        while not finished:
            cont = 0
            f = ""
            for pos in connections:
                for hubs in connections[pos]:
                    hubs.move = 0
            for drone in drones_list:
                result, stack= run(drone, path, stack, zones, end, connections)
                if result is None:
                    continue
                if result.transit is not None:
                    f += f"D{result.id_drone}-{result.position}-{result.transit}  "
                    continue
                if result.position == end.name and result.id_drone == int(1):
                    f += f"D{result.id_drone}-{result.position}"
                    drone.position = result.position
                    finished = True
                    break
                stack.setdefault(drone.id_drone, []).append(result.position)
                if drone.position == end.name and result.goal != 1:
                    f += f"D{result.id_drone}-{result.position}  "
                    result.goal = 1
                    continue
                if drone.position == end.name and result.goal == 1:
                    continue
                f += f"D{result.id_drone}-{result.position}  "
                drone.position = result.position
            i += 1
            print(f)
            print("Moves", i)
            print("-------------")
    except ValueError as e:
        print(e)