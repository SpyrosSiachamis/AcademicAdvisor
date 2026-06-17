from pydantic import BaseModel, Field, HttpUrl
from typing import Annotated

class University(BaseModel):
    id: Annotated[int, Field(gt=0)]
    name: Annotated[str, Field(min_length=3)]
    website_url: HttpUrl | None