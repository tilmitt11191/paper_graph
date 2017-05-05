import sys,os

from sqlalchemy import create_engine, Column
from sqlalchemy.dialects.mysql import INTEGER, TINYTEXT
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
class Table_authors(Base):
    __tablename__ = 'authors'

    id = Column("id", INTEGER, primary_key=True)
    name = Column("name", TINYTEXT)
    belonging = Column("belonging", TINYTEXT)

    def __init__(self, id="", name="", belonging=""):
    
        sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../lib/utils")
        from log import Log as l
        self.log = l.getLogger()
        
        import mysql_operator
        self.db = mysql_operator.Mysql_operator()

        self.id = id
        self.name = name
        self.belonging = belonging

    def __repr__(self):
        return 'Table_authors'

    def insert(self):
        if self.id == "":
            self.id = self.db.get_available_id(__class__)
        self.db.insert(self)
        self.db.session.expunge(self)
        self.db.session.close()

    def renewal_insert(self):
        self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")
        self.log.debug("self: " + self.get_vars())
        #check duplication and insert
        from sqlalchemy import and_
        records = self.db.session.query(__class__).filter(and_(__class__.name==self.name), (__class__.belonging==self.belonging)).all()
        self.log.debug("records = self.db.session.query(__class__).filter(__class__.name==self.name).all()")
        self.log.debug("len(records)[" + str(len(records)) + "]")
        if len(records) == 0: #new record
            self.log.debug("new author")
            self.id = self.db.get_available_id(__class__)
            self.insert()
        elif len(records) == 1:
            self.log.debug("already registed")
        else:
            self.log.debug("duplicated")
    
    def close(self):
        self.db.close()
    
    def get_vars(self):
        return("{"+
            "id: " + str(self.id) + ", " + 
            "name: " + str(self.name) + ", " + 
            "belonging: " + str(self.belonging) + 
        "}")

