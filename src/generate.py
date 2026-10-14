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