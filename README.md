*This project has been created as part of the 42 curriculum by pneto-vi.*

# Fly-in
## Description
Fly-in is a project whose objective is to optimize a pathfinding algorithm under constraints that make it harder: moving a given number of drones from the start zone to the end zone in as few turns as possible. I implemented a multi-path algorithm capable of finding multiple paths that, together, are optimized and meet every requirement of the project. Besides the algorithm, the project also includes a parser and a visual simulation, for which I chose to build a graphical representation.

## Instructions
### Requirements
- Python >=3.10
- uv
- pygame-ce, pydantic, flake8, mypy
### Install and run
```
make install
make run
```
To run a map other than the default:
```
uv run python -m src --path maps/folder_difficulty/map.txt
make run MAP="maps/folder_difficulty/map.txt"
```
### Run all maps
bash:
```
for m in maps/*/*.txt; do echo "$m: $(uv run python -m src --path $m < /dev/null 2>&1 | grep -E 'Moves|rror' | head -1)"; done
```
fish:
```
for m in maps/*/*.txt; echo "$m: "(uv run python -m src --path $m < /dev/null 2>&1 | grep -E "Moves|rror" | head -1); end
```
### Lint
```
make lint
```
## Map format (Input Format)
A map is made up of several pieces of required information:
```
nb_drones  : Number of drones that will travel the path
start_hub  : Starting position of every drone
end_hub    : Goal position the drones must reach
hub        : A position on the map, with metadata that constrains the drones
metadata   :
  max_drones        -> maximum number of drones allowed in the zone at the same time
  zone              -> zone type ("normal", "restricted", "blocked", "priority");
                       blocked zones cannot be accessed and restricted zones
                       have a movement penalty
  color             -> color of the zone
  max_link_capacity -> maximum number of drones that can use a connection in a single turn
connection : Links between zones that the drones follow to reach the end
```
## Output Format (non-graphical)

Example:
```
D1-gate_hell1
D1-maze_trap_a1 D2-gate_hell1
D1-maze_trap_a2 D2-maze_trap_a1 D3-gate_hell1
D1-micro_gate1 D2-maze_trap_a2 D3-maze_trap_a1 D4-gate_hell1
D1-micro_gate1-overflow_hell1 D2-micro_gate1 D3-maze_trap_a2 D4-maze_trap_a1 D5-gate_hell1
(...)
```
Each line is one turn. Each move is written as D<id>-<zone>, where <id> is the
drone's number and <zone> is where it moved to on that turn. A move such as
D1-micro_gate1-overflow_hell1 means the drone is in transit on a connection
to a restricted zone.

Drones that already reached the end zone and the start zone (shared by every
drone) are omitted, so only the actual moves are shown.

## Algorithm
The algorithm handles multiple penalties. For a single drone, the pipeline works like this:

1. The heap starts with the start position. Each heap entry holds:
   - turn: the current turn. This is always the first and most important value,
     since it represents the moves needed to get there.
   - priority_value: makes the algorithm prefer priority zones when two paths
     arrive on the same turn.
   - zone: the name of the current zone.
   - path: the positions visited so far, including the current one. When a zone
     is restricted, an intermediate step (zone-neighbor) is added to the path.
2. heappop always returns the entry with the lowest turn, using priority_value
   to break ties.
3. For each neighbor, the arrival turn is computed: +1 for normal zones and +2
   for restricted zones (which is why a drone may spend an extra round
   in transit).
4. Before moving, the algorithm checks that the zone has free capacity on that
   turn and that the connection is not full.
5. If everything is valid, heappush adds the next position, carrying over the
   previous values (turn, path, etc.).
6. The drone can also wait one turn in its current zone if there is space.

This repeats until the drone reaches the end zone. The resulting path is then
reserved, so the next drones plan around it, which is how the multiple paths
are built.

## Visualization

The simulation uses pygame-ce for the graphical visualization. It reuses each
drone's path (drone.path) already computed by the algorithm: on every turn it
loops through all the drones and moves each one to its next position, so the
visualization matches the terminal output turn by turn.

- Drones are drawn with a drone PNG image.
- The background is filled with black.
- Zones are drawn as rectangles using pygame's draw functions, and each drone
  is centered on its current zone.
- A turn counter and the moves made on that turn are displayed on screen.

## Error handling

Each error has its own custom message to make debugging easier, especially
for the input file. Input validation is handled in extract.py.

## Results

| Map | Moves |
|---|---|
| easy/01_linear_path | 4 |
| easy/02_simple_fork | 4 |
| easy/03_basic_capacity | 4 |
| medium/01_dead_end_trap | 8 |
| medium/02_circular_loop | 10 |
| medium/03_priority_puzzle | 6 |
| hard/01_maze_nightmare | 13 |
| hard/02_capacity_hell | 16 |
| hard/03_ultimate_challenge | 26 |
| challenger/01_the_impossible_dream | 43 |


## Resources

- References used to build the first structure:
  - [Dijkstra's shortest path algorithm (GeeksforGeeks)](https://www.geeksforgeeks.org/dsa/dijkstras-shortest-path-algorithm-greedy-algo-7/)
  - [pygame documentation](https://www.pygame.org/docs/)
  - [EOFError on user input (Stack Overflow)](https://stackoverflow.com/questions/74283683/eof-error-occurs-when-trying-to-give-a-user-input)
  - [Python raise (W3Schools)](https://www.w3schools.com/python/gloss_python_raise.asp)
  - [Storing class instances in a Python app (Stack Overflow)](https://stackoverflow.com/questions/34712078/proper-way-to-store-class-instances-in-python-app)
  - [Class attributes with pydantic's BaseModel (Stack Overflow)](https://stackoverflow.com/questions/70852331/how-to-define-class-attributes-after-inheriting-pydantics-basemodel)
- AI usage: AI was used mostly at the end of the project. During the design
  and implementation I kept my distance from it as much as I could, around 95% of the time. It was used to learn pygame faster, to review my reasoning, and to help with repetitive tasks such as fixing flake8 errors and correcting the English in messages and documentation.