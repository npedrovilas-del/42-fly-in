import heapq


def dijkstra(start , end , zones: dict, connections: dict) -> list[str]:
    cost = {name: (float("inf") , float("inf")) for name in zones}
    cost[start.name] = (0, 0)
    previous: dict[str, str] = {}
    queue = [((0, 0) , start.name)]
    while queue:
        current_cost, zone = heapq.heappop(queue)
        if zone == end.name:
            break
        if current_cost > cost[zone]:
            continue
        for link in connections.get(zone, []):
            if link.name_1 == zone:
                neighbor = link.name_2
            else:
                neighbor = link.name_1
            zone_type = zones[neighbor].zone
            if zone_type == "blocked":
                continue
            if zone_type == "restricted":
                step = (2, 1) 
            elif zone_type == "normal":
                step = (1, 1)
            elif zone_type == "priority":
                step = (1, 0)
            new_cost = (current_cost[0] + step[0], current_cost[1] + step[1])
            if new_cost < cost[neighbor]:
                cost[neighbor] = new_cost
                previous[neighbor] = zone
                heapq.heappush(queue, (new_cost, neighbor))
    if end.name not in previous:
        return []
    path = [end.name]
    while path[0] != start.name:
        path.insert(0, previous[path[0]])
    return path


def run(drones_list: list, path: list, stack: dict, zones: Hub, end: Hub, connections: Connections):
    i = 0
    finished = False
    while not finished:
        cont = 0
        f = ""
        for pos in connections:
            for hubs in connections[pos]:
                hubs.move = 0
        for drone in drones_list:
            result, stack= move_drones(drone, path, stack, zones, end, connections)
            if result is None:
                continue
            if result.transit is not None:
                f += f"D{result.id_drone}-{result.position}-{result.transit} "
                continue
            if result.position == end.name and result.id_drone == int(1):
                f += f"D{result.id_drone}-{result.position} "
                drone.position = result.position
                finished = True
                break
            stack.setdefault(drone.id_drone, []).append(result.position)
            if drone.position == end.name and result.goal != 1:
                f += f"D{result.id_drone}-{result.position} "
                result.goal = 1
                continue
            if drone.position == end.name and result.goal == 1:
                continue
            f += f"D{result.id_drone}-{result.position} "
            drone.position = result.position
        i += 1
        f_clean = f.strip()
        print(f_clean)
    print("Moves", i)
    print("All completed all drones on the goal destination")
    return True


def move_drones(drone: Drone, path: list, stack: dict, zones: Hub, end: Hub, connections: Connections):
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