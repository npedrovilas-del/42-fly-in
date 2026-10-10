from models import StartHub, EndHub, Hub, Conections

path = "/home/npe/42/Fly-in/maps/hard/02_capacity_hell.txt"

def extract_file(path: str)-> None:
    hub = {}
    try:
        with open(path) as f:
            data = list(f)
        i = int(0)
        while i < len(data):
            if data[i].startswith("nb"):
                drones = extract_number_drones(data[i])
            if data[i].startswith("start_hub:"):
                start = extract_start(data[i])
                print(start)
            if data[i].startswith("end_hub:"):
                end = extract_end(data[i])
                print(end)
            if data[i].startswith("hub:"):
                z = extract_hub(data[i])
                print(z)
            if data[i].startswith("connection:"):
                connection = extract_connection(data[i])
                print(connection)
            i += 1
    except ValueError as e:
        print(e)

def extract_connection(str: str):
    total = str.split(" ")
    names = total[1].strip().split("-")
    if len(total) > 2: 
        metadata = total[2].replace("]\n", "")
        f = metadata.replace("[", "")
        proc_metadata = dict(item.split("=") for item in f.split(" "))
    else:
        proc_metadata = {}
    return Conections(name_1 = names[0], name_2 = names[1], capacity = proc_metadata.get("max_link_capacity", 1))

def extract_hub(str: str):
    total = str.split("[")
    info = total[0].split(" ")
    name = info[1]
    x = int(info[2])
    y = int(info[3])
    metadata = total[1].replace("]\n", "")
    proc_metadata = dict(item.split("=") for item in metadata.split(" "))
    return Hub(color = proc_metadata.get("color", None), pos_x = x, pos_y = y, name = name, capacity = proc_metadata.get("max_drones", None), zone = proc_metadata.get("zone", "normal"))

def extract_start(str: str):
    total = str.split("[")
    info = total[0].split(" ")
    x = int(info[2])
    y = int(info[3])
    metadata = total[1].replace("]\n", "")
    proc_metadata = dict(item.split("=") for item in metadata.split(" "))
    return StartHub(color = proc_metadata["color"], pos_x = x, pos_y = y)

def extract_end(str: str):
    total = str.split("[")
    info = total[0].split(" ")
    x = int(info[2])
    y = int(info[3])
    metadata = total[1].replace("]\n", "")
    proc_metadata = dict(item.split("=") for item in metadata.split(" "))
    return EndHub(color = proc_metadata["color"], pos_x = x, pos_y = y)

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
        
if __name__ == "__main__":
    extract(path)