from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///activities.db', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False, bind=engine))
Base = declarative_base()

Base.query = db_session.query_property()


class Person(Base):
    __tablename__ = 'person'
    id = Column(Integer, primary_key=True)
    name = Column(String(40), index=True)
    age = Column(Integer)

    def __repr__(self):
        return "<Person {}>".format(self.name)

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()


class Activities(Base):
    __tablename__ = 'activities'
    id = Column(Integer, primary_key=True)
    name = Column(String(80))
    description = Column(String(150), index=True)
    person_id = Column(Integer, ForeignKey('person.id'))
    person = relationship("Person")

    def __repr__(self):
        return "<Activities {}>".format(self.name)

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()


def int_db():
    Base.metadata.create_all(bind=engine)


if __name__ == '__main__':
    int_db()