from pydantic import BaseModel
from typing import Optional, List
from models.cliente import Cliente


class ClienteSchema(BaseModel):
    """ Define como um novo cliente a ser inserido deve ser representado
    """
    telefone: int = "21998889999"
    nome: str = "Jose da Silva"
    email: str = "jose@gmail.com"
    cep: str = "20730-320"
    logradouro: str = "Av. Brasil"
    numero: int = "15"
    complemento: str = "Apto. 101"
    bairro: str = "Centro"
    cidade: str = "Rio de Janeiro"
    uf: str = "RJ"


class ClienteViewSchema(BaseModel):
    """ Define como um cliente consultado deve ser representado
    """
    telefone: int = "21998889999"
    nome: str = "Jose da Silva"
    email: str = "jose@gmail.com"
    cep: str = "20730-320"
    logradouro: str = "Av. Brasil"
    numero: int = "15"
    complemento: str = "Apto. 101"
    bairro: str = "Centro"
    cidade: str = "Rio de Janeiro"
    uf: str = "RJ"
    servicos: List[str] = ["Instalação elétrica em residencia"]


class ClienteBuscaPorNomeSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no nome do cliente.
    """
    termo: str = "Jose"


class ClienteBuscaPorTelefoneSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no telefone do cliente.
    """
    id: int = "21998889999"


class ListagemClientesSchema(BaseModel):
    """ Define como uma listagem de clientes será retornada.
    """
    clientes:List[ClienteViewSchema]


def apresenta_clientes(clientes: List[Cliente]):
    """ Retorna uma representação do cliente seguindo o schema definido em
        ListagemClientesSchema.
    """
    result = []
    for cliente in clientes:
        result.append({
            "nome": cliente.nome,
            "telefone": cliente.telefone,
            "e-mail": cliente.email,
            "servicos": [c.descricao for c in cliente.servicos]
        })

    return {"Clientes": result}


class ClienteViewSchema(BaseModel):
    """ Define como um cliente será retornado: cliente + serviços.
    """
    telefone: int = "21998889999"
    nome: str = "Jose da Silva"
    email: str = "jose@gmail.com"
    cep: str = "20730-320"
    logradouro: str = "Av. Brasil"
    numero: int = "15"
    complemento: str = "Apto. 101"
    bairro: str = "Centro"
    cidade: str = "Rio de Janeiro"
    uf: str = "RJ"
    total_servicos: int = 1
    servicos: List[str] = ["Instalação elétrica em residencia"]


class ClienteDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    id: int


def apresenta_cliente(cliente: Cliente):
    """ Retorna uma representação do cliente seguindo o schema definido em
        ClienteViewSchema.
    """
    return {
        "nome": cliente.nome,
        "email": cliente.email,
        "cep": cliente.cep,
        "logradouro": cliente.logradouro,
        "numero": cliente.numero,
        "complemento": cliente.complemento, 
        "bairro": cliente.bairro,
        "cidade": cliente.cidade,
        "uf": cliente.uf,
        "tiposervico": [c.tipo_servico for c in cliente.servicos], 
        "descricao": [c.descricao for c in cliente.servicos]
    }


class ClienteUpdSchema(BaseModel):
    """ Define como um cliente a ser alterado deve ser representado
    """
    telefone: int
    nome: str
    email: str
    cep: str
    logradouro: str
    numero: int
    complemento: str
    bairro: str
    cidade: str
    uf: str
