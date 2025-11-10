from typing import Annotated

from pydantic import ConfigDict, Field
from schemas.base import BaseSchema

class CategoriaIn(BaseSchema):
    nome: Annotated[str, Field(description="Nome da categoria", example="Leve", max_length=50)]
    
class CategoriaOut(BaseSchema):
    id: Annotated[int, Field(description="Identificador")]
    nome: Annotated[str, Field(description="Nome da categoria", example="Leve")]
    
    model_config = ConfigDict(from_attributes=True)
    