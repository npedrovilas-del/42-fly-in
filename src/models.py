from pydantic import BaseModel, Field

class StartHub(BaseModel):
    color: str
    pos_x: int
    pos_y: int

class EndHub(BaseModel):
    color: str
    pos_x: int
    pos_y: int

class Hub(BaseModel):
    name: str
    pos_x: int
    pos_y: int
    color: str
    capacity: int | None = Field(default=None)
    zone: str = Field(default="normal")

class Conections(BaseModel):
    name_1: str
    name_2: str
    capacity: int = Field(default=int(1))
