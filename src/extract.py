from .models import Hub, Connections
import sys


def extract_file(path: str) -> tuple[Hub, Hub, int,
                                     dict[str, Hub],
                                     dict[str, list[Connections]]]:
    """Extracts and returns all the information of the input.

    Already taking into account possible input Errors
    that may occur and raising ValueErrors with custom messages
    """
    zones: dict[str, Hub] = {}
    connections: dict[str, list[Connections]] = {}
    try:
        with open(path) as f:
            data = list(f)
        i = int(0)
        start = None
        end = None
        line_counter = 0
        drones = None
        while i < len(data):
            data[i] = data[i].split("#")[0]
            if data[i].startswith("nb"):
                if line_counter != 0:
                    raise ValueError("Number of drones not on top of the file")
                drones = extract_number_drones(data[i])
            elif data[i].startswith("start_hub:"):
                line_counter += 1
                if start is not None:
                    raise ValueError("HUBS: Cannot have 2 starts")
                start = extract_hub(data[i])
                if start.name in zones:
                    raise ValueError("Start: Duplicated start name")
                zones[start.name] = start
            elif data[i].startswith("end_hub:"):
                line_counter += 1
                if end is not None:
                    raise ValueError("HUBS: Cannot have 2 ends")
                end = extract_hub(data[i])
                if end.name in zones:
                    raise ValueError("End: Duplicated end name")
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
                if (connection.name_1 not in zones or
                        connection.name_2 not in zones):
                    raise ValueError("Connections: Connection not in hubs")
                for c in connections.get(connection.name_1, []):
                    if (c.name_1 == connection.name_2 or
                            c.name_2 == connection.name_2):
                        raise ValueError(
                            "Connections: Duplication of connections")
                connections.setdefault(
                    connection.name_1, []).append(connection)
                connections.setdefault(
                    connection.name_2, []).append(connection)
            elif data[i].startswith("#") or data[i].strip() == "":
                pass
            else:
                raise ValueError("Trash in the Input File")
            i += 1
        if start is None:
            raise TypeError("Error no start position")
        if end is None:
            raise TypeError("Error no end position")
        if drones is None:
            raise TypeError("No number of drones defined")
    except ValueError as e:
        print(f"Error Line {i + 1}: {e}")
        sys.exit(1)
    except TypeError as e:
        print(f"{e}")
        sys.exit(1)
    return (start, end, drones, zones, connections)


def extract_connection(str: str) -> Connections:
    """Auxiliary function that extracts the connections from file.

    Returns a Connection class already somewhat parsed and pydantic verified
    """
    total = str.split("[")
    first = total[0].split()
    if len(first) < 2:
        raise ValueError("Not valid Connection")
    names = first[1].strip().split("-")
    if len(names) != 2:
        raise ValueError("Connection: must have exactly two zone names")
    if names[0] == names[1]:
        raise ValueError("Connection: cannot link a zone to itself")
    if len(total) > 1:
        if not str.strip().endswith("]"):
            raise ValueError("Connection: Invalid brackets on closing")
        metadata = total[1].strip().replace("]", "")
        try:
            proc_metadata = dict(item.split("=") for item in metadata.split())
        except ValueError:
            raise ValueError("Connection: The metadata should be"
                             " correctly formatted")
        try:
            max_link = int(proc_metadata.get("max_link_capacity", "1"))
        except ValueError:
            raise ValueError(
                "Connection: Max link capacity should be an integer")
        if max_link < 1:
            raise ValueError("Connection: Link capacity not valid")
    else:
        proc_metadata = {}
    return Connections(name_1=names[0], name_2=names[1],
                       capacity=int(proc_metadata.get("max_link_capacity", 1)))


def extract_hub(str: str) -> Hub:
    """Auxiliary function that extracts the hubs from file.

    Returns a Hub class already somewhat parsed and pydantic verified
    """
    name = ""
    total = str.strip().split("[")
    info = total[0].split()
    if len(info) != 4:
        raise ValueError("Hubs should have 3 "
                         "parameters: name, pos_x, pos_y")
    name = info[1]
    for veri in name:
        if veri == "-":
            raise ValueError("HUBS: Name cannot have -")
    try:
        x = int(info[2])
        y = int(info[3])
    except ValueError:
        raise ValueError("Coordinates should be integers")
    if len(total) > 1:
        if not str.strip().endswith("]"):
            raise ValueError("HUBS: Incorrect brackets on Hub")
        metadata = total[1].replace("]", "").strip()
        try:
            proc_metadata = dict(item.split("=") for item in metadata.split())
        except ValueError:
            raise ValueError("HUBS: The metadata should be"
                             " correctly formatted")
        for key in proc_metadata:
            if key != "zone" and key != "color" and key != "max_drones":
                raise ValueError("HUBS: Invalid metadata KEY")
        if len(metadata.split()) != len(proc_metadata):
            raise ValueError("HUBS: Two repetitive metadata key")
        if proc_metadata.get("zone", "normal") not in [
                "restricted", "normal", "priority", "blocked"]:
            raise ValueError("HUBS: Zone type Invalid")
        try:
            max_drones = int(proc_metadata.get("max_drones", 1))
        except ValueError:
            raise ValueError("Hubs: Max drones should be an intenger")
        if max_drones < 1:
            raise ValueError("HUBS: Number of Max Drones not valid")
    else:
        proc_metadata = {}
    return Hub(color=proc_metadata.get("color", None),
               pos_x=x, pos_y=y, name=name,
               capacity=int(proc_metadata.get("max_drones", 1)),
               zone=proc_metadata.get("zone", "normal"))


def extract_number_drones(str: str) -> int:
    """Auxiliary function that extracts the number of drones.

    From file and returns parsed and verified with the constraints
    """
    n = str.split()
    if len(n) != 2:
        raise ValueError("Should have the parameter of number of drones only")
    try:
        f = int(n[1])
    except ValueError:
        raise ValueError("Number of drones should be an integer")
    if f <= 0:
        raise ValueError("Number of drones has to be greater than 0")
    return f
