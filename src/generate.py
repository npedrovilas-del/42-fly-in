import heapq
from .models import Hub, Connections, Drone
from .visual import running


def multiple_paths(drones: list[Drone], start: Hub, end: Hub,
                   zones: dict[str, Hub],
                   connections: dict[str, list[Connections]]) -> None:
    """Forms each individual path for a drone.

    Makes sure it takes into account the return reservations
    that will have a cost associated not only to the
    type of zone but the wait because of
    other drones wait time
    """
    reserv: dict[tuple[str | tuple[str, ...], int], int] = {}
    for drone in drones:
        path_new = time_dijkstra(start, end, zones, connections, reserv)
        if path_new is None:
            raise ValueError("No path Available")
        c = 0
        for j in path_new:
            reserv[(j, c)] = reserv.get((j, c), 0) + 1
            if c > 0 and path_new[c - 1] != j:
                if "-" in j:
                    x = (
                        tuple(sorted([path_new[c - 1],
                                      path_new[c + 1]])), c - 1)
                    reserv[x] = reserv.get(x, 0) + 1
                elif "-" in path_new[c - 1]:
                    pass
                else:
                    x = (tuple(sorted([path_new[c - 1], path_new[c]])), c - 1)
                    reserv[x] = reserv.get(x, 0) + 1
            c += 1
        drone.path = path_new


def time_dijkstra(start: Hub, end: Hub, zones: dict[str, Hub],
                  connections: dict[str, list[Connections]],
                  reserv: dict[tuple[str | tuple[str, ...],
                               int], int]) -> list[str] | None:
    """Algorithm that chooses the lowest cost path to each drone.

    Takes into account wait, type of zone and link capacity,
    returning an individual path optimized for each drone
    """
    heap = [(0, 0, start.name, [start.name])]
    visited = set()
    while heap:
        turn, priority_value, zone, path = heapq.heappop(heap)
        if turn > 200:
            continue
        if (zone, turn) in visited:
            continue
        visited.add((zone, turn))
        if zone == end.name:
            return path
        for x in connections.get(zone, []):
            if x.name_1 == zone:
                neighbor = x.name_2
            else:
                neighbor = x.name_1
            zone_type = zones[neighbor].zone
            if zone_type == "blocked":
                continue
            if zone_type == "restricted":
                arrive = turn + 2
            else:
                arrive = turn + 1
            priority_count = priority_value
            if zone_type == "normal":
                priority_count += 1
            if zone_type == "priority":
                priority_count -= 1
            if neighbor != end.name and reserv.get(
                    (neighbor, arrive), 0) >= zones[neighbor].capacity:
                continue
            if reserv.get(
                    (tuple(sorted([zone, neighbor])),
                        (turn)), 0) >= x.capacity:
                continue
            if zone_type == "restricted":
                heapq.heappush(heap, (arrive, priority_count, neighbor, path +
                               [f"{zone}-{neighbor}", neighbor]))
            else:
                heapq.heappush(heap, (arrive, priority_count, neighbor,
                                      path + [neighbor]))
        wait = turn + 1
        if zone == start.name or reserv.get(
                (zone, wait), 0) < zones[zone].capacity:
            heapq.heappush(heap, (wait, priority_value, zone, path + [zone]))
    return None


def run(drones_list: list[Drone], zones: dict[str, Hub], end: Hub,
        connections: dict[str, list[Connections]], start: Hub) -> bool:
    """Loops through the drone internal path until it reaches the goal.

    Using its internal path (drone.path) and its
    internal position (drone.position) after completing every drone,
    it activates the simulation.
    """
    counter = 1
    while not all(d.position == end.name for d in drones_list):
        f = ""
        for drone in drones_list:
            if counter >= len(drone.path):
                continue
            if drone.path[counter] == drone.path[counter - 1]:
                continue
            drone.position = drone.path[counter]
            f += f"D{drone.id_drone}-{drone.path[counter]} "
        print(f.strip())
        counter += 1
    print(
        f"All completed, all {
            len(drones_list)} drones on the goal destination")
    print("Moves", counter - 1)
    try:
        choice = input("Watch simulation of the moves (Y/N)")
        if choice == "y" or choice == "Y":
            running(zones, connections, drones_list, start, end, counter)
    except EOFError:
        print("\nError EOFError, Exiting simulation")
    except KeyboardInterrupt:
        print("\nErro KeyboardInterrupt, Exiting simulation")
    return True
