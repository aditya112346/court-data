from sqlalchemy import create_engine
from models import Base
import os

DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///courtdata.db')

def init_db():
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)

if __name__ == '__main__':
    init_db()
    print('DB created')
