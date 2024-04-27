from pydantic import BaseModel
from typing import List
from models.servico import Servico


class ServicoSchema(BaseModel):
    """ Define como um novo serviço a ser inserido deve ser representado
    """
    cliente_tel: int = "21998889999"
    tipo_servico: str = "Eletricista"
    descricao: str = "Instalação elétrica em residencia"

class ServicoDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    id: int

class ServicoBuscaPorTelefoneSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no telefone do cliente.
    """
    id: int = "21998889999"

class ServicoViewSchema(BaseModel):
    """ Define como um serviço consultado deve ser representado
    """
    telefone: int = "21998889999"
    tiposervico: str = "Marceneiro"
    descricao: str = "Fabricar um armário de cozinha"

class ListagemServicosSchema(BaseModel):
    """ Define como uma listagem de serviços será retornada.
    """
    servicos:List[ServicoViewSchema]

def apresenta_servicos(servicos: List[Servico]):
    """ Retorna uma representação do serviço seguindo o schema definido em
        ListagemClientesSchema.
    """
    result = []
    for servico in servicos:
        result.append({
            "telefone": servico.cliente,
            "tipo_servico": servico.tipo_servico,
            "descricao": servico.descricao
        })

    return {"Serviços": result}