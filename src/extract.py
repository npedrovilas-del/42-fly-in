from models import Hub, Conections

path = "/home/npe/42/Fly-in/maps/hard/02_capacity_hell.txt"

def extract_file(path: str)-> None:
    zones = {}
    connections = {}
    try:
        with open(path) as f:
            data = list(f)
        i = int(0)
        while i < len(data):
            if data[i].startswith("nb"):
                drones = extract_number_drones(data[i])
            if data[i].startswith("start_hub:"):
                start = extract_hub(data[i])
                zones[start.name] = start
            if data[i].startswith("end_hub:"):
                end = extract_hub(data[i])
                zones[end.name] = end
            if data[i].startswith("hub:"):
                hub = extract_hub(data[i])
                zones[hub.name] = hub
            if data[i].startswith("connection:"):
                connection = extract_connection(data[i])
                connections.setdefault(connection.name_1, []).append(connection)
                connections.setdefault(connection.name_2, []).append(connection)
            i += 1
    except ValueError as e:
        print(e)
    return (start, end, drones, zones, connections)

def extract_connection(str: str):
    total = str.split(" ")
    names = total[1].strip().split("-")
    if len(total) > 2: 
        metadata = total[2].replace("]\n", "")
        f = metadata.replace("[", "")
        proc_metadata = dict(item.split("=") for item in f.split(" "))
    else:
        proc_metadata = {}
    return Conections(name_1 = names[0], name_2 = names[1], capacity = proc_metadata.get("max_link_capacity", 1), moves = 0)

def extract_hub(str: str):
    total = str.split("[")
    info = total[0].split(" ")
    name = info[1]
    x = int(info[2])
    y = int(info[3])
    metadata = total[1].replace("]\n", "")
    proc_metadata = dict(item.split("=") for item in metadata.split(" "))
    return Hub(color = proc_metadata.get("color", None), pos_x = x, pos_y = y, name = name, capacity = proc_metadata.get("max_drones", 1), zone = proc_metadata.get("zone", "normal"))

def extract_number_drones(str: str):
    n = ""
    for i in str:
        if i.isnumeric():
            n += i
        else:
            continue
    try:
        number = int(n)
        return(number)
    except ValueError as e:
        print(e)
