from sqlalchemy import Column, String, Integer, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from  model import Base, Unit, Classification


class Service(Base):
    __tablename__ = 'service'

    id = Column("pk_service", Integer, primary_key=True)

    # quantities list
    code = relationship("Classification")
    base_description = Column(String(1024), unique=True)
    unit = relationship("Unit")

    # especification
    especification_title = Column(String(256), unique=True)
    especification = Column(String(4096))
    manufactory_reference = Column(String(255))

    # developer/bim
    bim = Column(Boolean)
    developer_code = Column(String(16), unique=True)
    countable = Column(Boolean)
    schedule = Column(String(64))
    script = Column(String(64))
    ifc = Column(String(64))

    # approver
    technical_approver = Column(Boolean)
    bim_approver = Column(Boolean)

    # system register
    data_register = Column(DateTime, default=datetime.now())
    # data_technical_approver = Column(DateTime, default=datetime.now())
    # data_bim_approver = Column(DateTime, default=datetime.now())

    # user_register = Column(String(64))
    # user_technical_approver = Column(String(64))
    # user_bim_approver = Column(String(64))
    

    def __init__(self, base_description:str, especification:str,
                 especification_title: str, manufactory_reference:str, bim:bool,
                 developer_code:str, countable:bool, schedule:str, script:str,
                 ifc:str, technical_approver:bool, bim_approver:bool,
                 data_insercao:Union[DateTime, None] = None,
                 ):
        
        self.base_description = base_description
        self.especification_title = especification_title
        self.especification = especification
        self.manufactory_reference = manufactory_reference
        self.bim = bim
        self.developer_code = developer_code
        self.countable = countable
        self.schedule = schedule
        self.script = script
        self.ifc = ifc
        self.technical_approver = technical_approver
        self.bim_approver = bim_approver
        
        if data_insercao:
            self.data_insercao = data_insercao

    def add_unit(self, unit:Unit):

        self.unit.append(unit)