from typing import Annotated
from pydantic import ConfigDict, Field
from schemas.base import BaseSchema

class CentroTreinamentoIn(BaseSchema):
    nome: Annotated[str, Field(description="Nome do centro de treinamento", example="CT Alpha", max_length=100)]
    localizacao: Annotated[str, Field(description="Localização do centro de treinamento", example="São Paulo", max_length=100)]
    proprietario: Annotated[str, Field(description="Proprietário do centro de treinamento", example="Carlos Silva", max_length=100)]
    
class CentroTreinamentoAtleta(BaseSchema):
    nome: Annotated[str, Field(description="Nome do centro de treinamento", max_length=100)]
    
class CentroTreinamentoOut(CentroTreinamentoAtleta):
    id: Annotated[int, Field(description="Identificador")]
    model_config = ConfigDict(from_attributes=True)