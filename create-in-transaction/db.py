from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///countries.db', echo=True)
LocalSession = sessionmaker(engine)
