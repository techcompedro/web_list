from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine('sqlite:///lista.db', echo=True)

Base = declarative_base()

class Lista(Base):
    __tablename__ = 'lista'
    id = Column(Integer, primary_key=True)
    lista = Column(String(150), nullable=False)
    feita = Column(Boolean,  default=False)
    
    
Session = sessionmaker(bind=engine)
session = Session()    

#Base.metadata.create_all(engine)



    
    