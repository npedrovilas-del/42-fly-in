from .models import Hub, Conections
import sys

def extract_file(path: str)-> None:
    zones = {}
    connections = {}
    try:
        with open(path) as f:
            data = list(f)
        i = int(0)
        start = None
        end = None
        line_counter = 0
        drones = None
        while i < len(data):
            if data[i].startswith("nb"):
                if line_counter  != 0:
                    raise ValueError("Number of drones not on top of the file")
                drones = extract_number_drones(data[i])
            elif data[i].startswith("start_hub:"):
                line_counter += 1
                if start != None:
                    raise ValueError("HUBS: Cannot have 2 starts")
                start = extract_hub(data[i])
                zones[start.name] = start
            elif data[i].startswith("end_hub:"):
                line_counter += 1
                if end != None:
                    raise ValueError("HUBS: Cannot have 2 ends")
                end = extract_hub(data[i])
                zones[end.name] = end
            elif data[i].startswith("hub:"):
                line_counter += 1
                hub = extract_hub(data[i])
                if hub.name in zones:
                    raise ValueError("HUBS: Duplicated zones names")
                zones[hub.name] = hub
            elif data[i].startswith("connection:"):
                line_counter += 1
                connection = extract_connection(data[i])
                if connection.name_1 not in zones or connection.name_2 not in zones:
                    raise ValueError("Connections: Connection not in hubs")
                for c in connections.get(connection.name_1, []):
                    if c.name_1 == connection.name_2 or c.name_2 == connection.name_2:
                        raise ValueError("Connections: Duplication of connections")
                connections.setdefault(connection.name_1, []).append(connection)
                connections.setdefault(connection.name_2, []).append(connection)
            elif data[i].startswith("#") or data[i].strip() == "":
                pass
            else:
                raise ValueError("Trash in the Input File")
            i += 1
        if start == None:
            raise TypeError("Error no start position")
        if end == None:
            raise TypeError("Error no end position")
        if drones == None:
            raise TypeError("No number of drones defined")
    except ValueError as e:
        print(f"Error Line {i + 1}: {e}")
        sys.exit(1)
    except TypeError as e:
        print(f"{e}")
        sys.exit(1)
    return (start, end, drones, zones, connections)


def extract_connection(str: str):
    total = str.split(" ")
    names = total[1].strip().split("-")
    if len(total) > 2:
        if not str.strip().endswith("]"):
            raise ValueError("Connection: Invalid brackets on closing")
        metadata = total[2].replace("]\n", "")
        f = metadata.replace("[", "")
        proc_metadata = dict(item.split("=") for item in f.split(" "))
        try:
            max_link = int(proc_metadata.get("max_link_capacity", "1"))
        except ValueError:
            raise ValueError("Connection: Max link capacity should be a integer")
        if max_link < 1:
            raise ValueError("Connection: Link capacity not valid")
    else:
        proc_metadata = {}
    return Conections(name_1 = names[0], name_2 = names[1], capacity = proc_metadata.get("max_link_capacity", 1))


def extract_hub(str: str):
    name = ""
    total = str.strip().split("[")
    info = total[0].split()
    name = info[1]
    for veri in name:
        if veri == "-":
            raise ValueError("HUBS: Name cannot have -")
    try:
        x = int(info[2])
        y = int(info[3])
    except ValueError:
        raise ValueError("Coordinates should be a integer")
    if len(total) > 1:
        if not str.strip().endswith("]"):
            raise ValueError("HUBS: Incorrect brackets on Hub")
        metadata = total[1].replace("]", "").strip()
        try:
            proc_metadata = dict(item.split("=") for item in metadata.split())
        except ValueError:
            raise ValueError("HUBS: The metadata should be formated corrected")
        if proc_metadata.get("zone", "normal") not in ["restricted", "normal", "priority", "blocked"]:
            raise ValueError("HUBS: Zone type Invalid")
        try:
            max_drones = int(proc_metadata.get("max_drones", 1))
        except ValueError:
            raise ValueError("Hubs: Max drones shoul be a intenger")
        if max_drones < 1:
            raise ValueError("HUBS: Number os Max Drones not valid")
    else:
        proc_metadata = {}
    return Hub(color = proc_metadata.get("color", None) , pos_x = x, pos_y = y, name = name, capacity = proc_metadata.get("max_drones", 1), zone = proc_metadata.get("zone", "normal"))

def extract_number_drones(str: str):
    n = ""
    for i in str:
        if i.isnumeric() or i == "-":
            n += i
        else:
            continue
    try:
        f = int(n)
    except ValueError:
        raise ValueError("Number of drones should be a integer")
    if f <= 0:
        raise ValueError("Number of drones has to be greater than 0")
    return f
