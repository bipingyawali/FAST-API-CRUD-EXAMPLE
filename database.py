from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# DATABASEURL = 'postgresql://postgres:bipin123@localhost/FasApiCRUD'

DATABASEURL = 'postgresql://fast_api_crud_user:QQu12CfPkwueNe8z3KBlcyshunkH3vl4@dpg-ctfjskt6l47c73b9e1kg-a.frankfurt-postgres.render.com/fast_api_crud'

engine = create_engine(DATABASEURL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()