from sqlalchemy import create_engine, Column, String, Float, DateTime, Boolean, Integer, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import json
from app.settings import Config

Base = declarative_base()

class Transaction(Base):
    __tablename__ = 'transactions'
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    trans_num = Column(String)
    trans_date = Column(String)
    trans_time = Column(String)
    cc_num = Column(String)
    merchant = Column(String)
    first = Column(String)
    last = Column(String)
    gender = Column(String)
    category = Column(String)
    amt = Column(Float)
    dob = Column(String)
    is_fraud = Column(Boolean)
    predicted_at = Column(DateTime, default=datetime.utcnow)
    lag_in_seconds = Column(Integer)

    def to_dict(self):
        return {
            'id': self.id,
            'trans_num': self.trans_num,
            'trans_date': self.trans_date,
            'trans_time': self.trans_time,
            'cc_num': self.cc_num,
            'merchant': self.merchant,
            'first': self.first,
            'last': self.last,
            'gender': self.gender,
            'category': self.category,
            'amt': self.amt,
            'dob': self.dob,
            'is_fraud': self.is_fraud,
            'predicted_at': str(self.predicted_at),
            'lag_in_seconds': self.lag_in_seconds,
        }
    
    def to_json(self):
        return json.dumps(self.to_dict())

# Initialize database
engine = create_engine(Config.POSTGRES_URI)
Base.metadata.create_all(engine)
