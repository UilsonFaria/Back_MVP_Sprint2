from pydantic import BaseModel

class CepSchema(BaseModel):
    """ Define como a chamada ao serviço externo deve ser representada
    """
    cep: str = "20000-100"
    logradouro: str
    complemento: str
    bairro: str 
    localidade: str
    uf: str
    ibge: str
    gia: str
    ddd: str
    siafi: str


class CepViewSchema(BaseModel):
    """ Define como um CEP consultado deve ser representada
    """
    cep: str = "20000-100"
    logradouro: str
    complemento: str
    bairro: str 
    localidade: str
    uf: str
    ibge: str
    gia: str
    ddd: str
    siafi: str


class CepBuscaDadosSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca pelos dados do CEP.
        Será feita apenas com base no cep.
    """
    cep: str = "20000-100"