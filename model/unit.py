from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from datetime import datetime
from typing import Union

from  model import Base


class Unit(Base):
    __tablename__ = 'unit'

    id = Column(Integer, primary_key=True)
    unit = Column(String(50), unique=True)
    abbreviation = Column(String(15), unique=True)
    data_insercao = Column(DateTime, default=datetime.now())

    service = Column(Integer, ForeignKey("service.pk_service"), nullable=False)

    def __init__(self, unit:str, abbreviation:str, data_insercao:Union[DateTime, None] = None):

        self.unit = unit
        self.abbreviation = abbreviation
        
        if data_insercao:
            self.data_insercao = data_insercao