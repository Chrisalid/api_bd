from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///activities.db', convert_unicode=True)

db_session = scoped_session(sessionmaker(autocommit=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


class Persons(Base):
    __tablename__ = 'persons'
    id = Column(Integer, primary_key=True)
    name = Column(String(40), index=True)
    age = Column(Integer)


    def __repr__(self):
        return f'<Person {self.name}>'


    def save(self):
        db_session.add(self)
        db_session.commit()


    def delete(self):
        db_session.delete(self)
        db_session.commit()


class Activities(Base):
    __tablename__ = 'activities'
    id = Column(Integer, primary_key=True)
    activity = Column(String(80))
    status = Column(String(60))
    person_id = Column(Integer, ForeignKey('persons.id'))
    person = relationship('Persons')


    def __repr__(self):
        return f'<Activities {self.activity}>'


    def save(self):
        db_session.add(self)
        db_session.commit()


    def delete(self):
        db_session.delete(self)
        db_session.commit()

def init_db():
    Base.metadata.create_all(bind=engine)


if __name__ == '__main__':
    init_db()
