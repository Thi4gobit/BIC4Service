from pydantic import BaseModel
from typing import Optional, List
from model.service import Service

from schemas import ComentarioSchema


class ServiceSchema(BaseModel):
    """ Define como um novo service a ser inserido deve ser representado
    """
    developer_code:str = "00000"
    base_description:str = "teste descricao"
    especification:str = "teste especificacao"
    manufactory_reference:str = "teste reference"


class ServiceBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no nome do service.
    """
    nome: str = "Teste"


class ListagemServiceSchema(BaseModel):
    """ Define como uma listagem de services será retornada.
    """
    services:List[ServiceSchema]


def apresenta_services(services: List[Service]):
    """ Retorna uma representação do service seguindo o schema definido em
        ServiceViewSchema.
    """
    result = []
    for service in services:
        result.append({
            "developer_code": produto.developer_code,
            "base_description": produto.base_description,
            "especification": produto.especification,
            "manufactory_reference": produto.manufactory_reference,
        })

    return {"services": result}


class ServiceViewSchema(BaseModel):
    """ Define como um service será retornado: service + comentários.
    """
    id: int = 1
    developer_code:str = "00000"
    base_description:str = "teste descricao"
    especification:str = "teste especificacao"
    manufactory_reference:str = "teste reference"
    total_cometarios: int = 1
    comentarios:List[ComentarioSchema]


class ServiceDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    developer_code: str

def apresenta_service(service: Service):
    """ Retorna uma representação do service seguindo o schema definido em
        ServiceViewSchema.
    """
    return {
        "id": produto.id,
        "developer_code": produto.developer_code,
        "base_description": produto.base_description,
        "especification": produto.especification,
        "manufactory_reference": produto.manufactory_reference,
        "total_cometarios": len(produto.comentarios),
        "comentarios": [{"texto": c.texto} for c in service.comentarios]
    }