from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from  model import Base, Comentario


class Service(Base):
    __tablename__ = 'service'

    id = Column("pk_service", Integer, primary_key=True)
    developer_code = Column(String(140), unique=True)
    description = Column(String(140))
    quantidade = Column(Integer)
    valor = Column(Float)
    data_insercao = Column(DateTime, default=datetime.now())

    comentarios = relationship("Comentario")

    def __init__(self, developer_code:str, description:str, quantidade:int, valor:float,
                 data_insercao:Union[DateTime, None] = None):

        self.developer_code = developer_code
        self.description = description
        self.quantidade = quantidade
        self.valor = valor

        if data_insercao:
            self.data_insercao = data_insercao

    def adiciona_comentario(self, comentario:Comentario):

        self.comentarios.append(comentario)