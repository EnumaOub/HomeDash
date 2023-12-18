from sqlalchemy import Column, Integer, String, Date, DateTime
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION

try:
    from dashboard.database.database import Base
except:
    from database import Base

class SP_CON(Base):
    __tablename__ = 'sp_con'
    id = Column(Integer, primary_key=True)
    testtime = Column(DateTime, unique=True, default=func.now())
    ul = Column(DOUBLE_PRECISION, unique=True)
    dl = Column(DOUBLE_PRECISION, unique=True)

    def __init__(self, ul=None, dl=None):
        self.ul = ul
        self.dl = dl

    def __repr__(self):
        return '<DATETIME %r>' % (self.testtime)

