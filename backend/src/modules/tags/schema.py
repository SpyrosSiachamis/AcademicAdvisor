from pydantic import BaseModel, Field
from typing import Annotated


class Tag(BaseModel):
    id: Annotated[int, Field(gt=0)]
    name: Annotated[str, Field(min_length=2, max_length=50)]


class TagUpdate(BaseModel):
    name: Annotated[str, Field(min_length=2, max_length=50)] | None = None
