from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from datetime import datetime
from typing import Union

from  models import Base


class Servico(Base):

    __tablename__ = 'servicos'

    id = Column(Integer, primary_key=True)
    tipo_servico = Column(String(100))
    descricao = Column(String(4000))
    data_insercao = Column(DateTime, default=datetime.now())

    # Definição do relacionamento entre o serviço e o cliente.
    # Aqui está sendo definido a coluna 'cliente' que vai guardar
    # a referencia ao cliente, a chave estrangeira que relaciona
    # um cliente ao serviço.
    cliente = Column(Integer, ForeignKey("clientes.pk_cliente"), nullable=False)

    def __init__(self, tipo_servico:str, descricao:str, data_insercao:Union[DateTime, None] = None):
        """
        Cria um Serviço

        Arguments:
            tipo_servico: Classificação do serviço solicitado
            descricao: Texto descritivo do serviço solicitado
            data_insercao: data de quando o serviço foi inserido à base
        """
        self.tipo_servico = tipo_servico
        self.descricao = descricao
        if data_insercao:
            self.data_insercao = data_insercao

    def to_dict(self):
        """
        Retorna a representação em dicionário do Objeto Serviço.
        """
        return{
            "id": self.id,
            "tipo_serviço": self.tipo_servico,
            "descricao": self.descricao,
            "data_insercao": self.data_insercao,
            "cliente_id": self.cliente.telefone
        }

    def __repr__(self):
        """
        Retorna uma representação do Serviço em forma de texto.
        """
        return f"Serviço(id={self.id}, tipo_servico='{self.tipo_servico}', descricao='{self.descricao}')"