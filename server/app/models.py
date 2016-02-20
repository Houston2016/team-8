import json
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime, Boolean
engine = create_engine('sqlite:///Neighborhood.db', echo=False) #Move string to constants 
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class Admin(Base):
    __tablename__ = 'admin'
    id = Column(Integer, primary_key=True)
    username = Column(String(30), nullable=False)
    first_name = Column(String(30), nullable=False)
    last_name = Column(String(30), nullable=False)
    email = Column(String(75), nullable=False)
    password = Column(String(128), nullable=False)

    def __str__(self):
        return "<Admin('%s')>" % (self.username)


admin_table = Admin.__table__

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(30), nullable=False)
    name = Column(String(50), nullable=False)
    address = Column(String(150), nullable=True)
    phone = Column(String(10), nullable=True)
    email = Column(String(75), nullable=False)
    password = Column(String(75), nullable=False)


    def __repr__(self):
        return "<User('%s')>" % (self.username)

        
user_table = User.__table__

metadata = Base.metadata


def create_all():
    metadata.create_all(engine)


class AlchemyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data) # this will fail on non-encodable values, like other classes
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            # a json-encodable dict
            return fields

        return json.JSONEncoder.default(self, obj)


#use like this 
#c = YourAlchemyClass()
#print json.dumps(c, cls=AlchemyEncoder)
