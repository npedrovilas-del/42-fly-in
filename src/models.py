from pydantic import BaseModel, Field


class Hub(BaseModel):
    name: str
    pos_x: int
    pos_y: int
    color: str | None = Field(default=None)
    drones: int = Field(default=0)
    capacity: int | None = Field(default=1)
    zone: str = Field(default="normal")

class Conections(BaseModel):
    name_1: str
    name_2: str
    capacity: int = Field(default=int(1))
    move: int = Field(default=int(0))

class Drone(BaseModel):
    id_drone: int
    position: str
    path: list
    transit: str | None = Field(default=None)
    goal: int = Field(default=0)

