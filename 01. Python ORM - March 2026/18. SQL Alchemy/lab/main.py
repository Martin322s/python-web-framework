from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = 'postgresql+psycopg2://postgres:root@localhost:5432/sqlalch'

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)


