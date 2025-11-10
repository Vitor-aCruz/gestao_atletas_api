from typing import Annotated
from pydantic import BaseModel, Field
from datetime import datetime


class BaseSchema(BaseModel):
    class Config:
        extra = "forbid"
        from_attributes = True


class OutMixin(BaseSchema):
    pk_id: Annotated[int, Field(description="Identificador")]
    created_at: Annotated[datetime, Field(description="Data de criação")]         