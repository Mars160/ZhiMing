from dbconfig import MYSQL_STRING
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine(MYSQL_STRING, echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)

db = Session()
