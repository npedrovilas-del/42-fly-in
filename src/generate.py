import heapq


def dijkstra(start , end , zones: dict, connections: dict) -> list[str]:
    cost = {name: float("inf") for name in zones}
    cost[start.name] = 0
    previous: dict[str, str] = {}
    queue = [(0, start.name)]
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
            step = 2 if zone_type == "restricted" else 1
            new_cost = current_cost + step
            if new_cost < cost[neighbor]:
                cost[neighbor] = new_cost
                previous[neighbor] = zone
                heapq.heappush(queue, (new_cost, neighbor))

    print(current_cost)
    if end.name not in previous:
        return []
    path = [end.name]
    while path[0] != start.name:
        path.insert(0, previous[path[0]])
    return path