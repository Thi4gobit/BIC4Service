from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from datetime import datetime
from typing import Union

from  model import Base


class Classification(Base):
    __tablename__ = 'classification'

    id = Column(Integer, primary_key=True)
    code_n1 = Column(String(50), unique=True)
    title_n1 = Column(String(15), unique=True)
    code_n2 = Column(String(50), unique=True)
    title_n2 = Column(String(15), unique=True)
    code_n3 = Column(String(50), unique=True)
    title_n3 = Column(String(15), unique=True)
    code_n4 = Column(String(50), unique=True)
    title_n4 = Column(String(15), unique=True)
    data_insercao = Column(DateTime, default=datetime.now())

    service = Column(Integer, ForeignKey("service.pk_service"), nullable=False)

    def __init__(self, code_n1:str, title_n1:str, code_n2:str, title_n2:str,
                 code_n3:str, title_n3:str, code_n4:str, title_n4:str,
                 data_insercao:Union[DateTime, None] = None):
        
        self.code_n1 = code_n1
        self.title_n1 = title_n1
        self.code_n2 = code_n2
        self.title_n2 = title_n2
        self.code_n3 = code_n3
        self.title_n3 = title_n3
        self.code_n4 = code_n4
        self.title_n4 = title_n4

        if data_insercao:
            self.data_insercao = data_insercao