from sqlalchemy import Column, String, Integer, DateTime, Float, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from  models import Base, Servico


class Cliente(Base):

    __tablename__ = 'clientes'

    # o sufixo pk está sendo utilizado para indicar que é uma chave primária    
    telefone = Column("pk_cliente", Integer, primary_key=True)
    nome = Column(String(140))
    email = Column(String(100))
    logradouro = Column(String(200))
    numero = Column(Integer)
    complemento = Column(String(400))
    bairro = Column(String(60))
    cidade = Column(String(60))
    uf = Column(String(2))
    cep = Column(String(10))
    data_cadastro = Column(DateTime, default=datetime.now())

    # Criando um requisito de unicidade
    __table_args__ = (UniqueConstraint("email", name="cliente_unique_email"),)

    # Estabelecendo o relacionamento entre cliente e serviço
    servicos = relationship("Servico", cascade="all, delete")

    def __init__(self, telefone, nome, email, logradouro, numero, complemento, bairro, cidade, uf, cep,
                 data_cadastro:Union[DateTime, None] = None):
        """
        Cria um Cliente

        Arguments:
            telefone: telefone do cliente
            nome: nome completo do cliente
            email: e-mail do cliente
            logradouro: logradouro do cliente
            numero: numero do logradouro
            complemento: complemento do logradouro
            bairro: bairro do logradouro
            cidade: cidade do logradouro
            uf: UF do logradouro
            cep: cep do logradouro
            data_cadastro: data de quando o cliente foi inserido na base
        """
        self.telefone = telefone
        self.nome = nome
        self.email = email
        self.logradouro = logradouro
        self.numero = numero
        self.complemento = complemento
        self.bairro = bairro
        self.cidade = cidade
        self.uf = uf
        self.cep = cep

        # será sempre a data exata da inserção no banco
        self.data_cadastro = data_cadastro

    def to_dict(self):
        """
        Retorna a representação em dicionário do Objeto Cliente.
        """
        return{
            "nome": self.nome,
            "telefone": self.telefone,
            "e-mail": self.email,
            "logradouro": self.logradouro,
            "numero": self.numero,
            "complemento": self.complemento,
            "bairro": self.bairro,
            "cidade": self.cidade,
            "UF": self.uf,
            "CEP": self.cep,
            "data_cadastro": self.data_cadastro,
            "serviços": [c.to_dict() for c in self.servicos]
        }

    def __repr__(self):
        """
        Retorna uma representação do Cliente em forma de texto.
        """
        return f"Cliente(telefone={self.telefone}, nome='{self.nome}', e-mail='{self.email}')"

    def adiciona_servico(self, servico:Servico):
        """ Adiciona um novo serviço solicitado pelo cliente
        """
        self.servicos.append(servico)
