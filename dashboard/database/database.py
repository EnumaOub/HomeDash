# -*- coding: utf-8 -*-
"""
Created on Wed Mar  8 20:13:18 2023

@author: rayan
"""

from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
try:
    from set_config import set_config
except:
    from dashboard.database.set_config import set_config

params = set_config()
engine = create_engine(f'postgresql://{params["user"]}:{params["password"]}@{params["host"]}/{params["database"]}',
                        connect_args= dict(host=params["host"], port=params["port"]))
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

# inspector = inspect(engine)
# schemas = inspector.get_schema_names()

# for schema in schemas:
#     print("schema: %s" % schema)
#     for table_name in inspector.get_table_names(schema=schema):
#         for column in inspector.get_columns(table_name, schema=schema):
#             print("Column: %s" % column)

def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    import models
    Base.metadata.create_all(bind=engine)