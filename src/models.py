from pydantic import BaseModel, Field


class Hub(BaseModel):
    """Base Class of the position on the maps."""
    name: str
    pos_x: int
    pos_y: int
    color: str | None = Field(default=None)
    drones: int = Field(default=0)
    capacity: int = Field(default=1)
    zone: str = Field(default="normal")


class Connections(BaseModel):
    """Base Class of each connection on the map."""
    name_1: str
    name_2: str
    capacity: int = Field(default=int(1))
    move: int = Field(default=int(0))


class Drone(BaseModel):
    """Base Class of drone and its location on the map."""
    id_drone: int
    position: str
    path: list[str] = Field(default_factory=list)
    transit: str | None = Field(default=None)
    goal: int = Field(default=0)
