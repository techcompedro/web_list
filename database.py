from sqlalchemy import create_engine, Column, Integer, String, Boolean, func, Date, extract
from sqlalchemy.orm import declarative_base, sessionmaker 
from datetime import datetime 

engine = create_engine('sqlite:///lista.db', echo=True)

Base = declarative_base()

class Lista(Base):
    __tablename__ = 'lista'
    id = Column(Integer, primary_key=True)
    lista = Column(String(150), nullable=False)
    descricao = Column(String(300), nullable=True)
    feita = Column(Boolean,  default=False)
    data = Column(Date, nullable=True)
    

Session = sessionmaker(bind=engine)
session = Session()
Base.metadata.create_all(engine)    
