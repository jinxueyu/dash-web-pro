from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint, Index, Text
from sqlalchemy.orm import sessionmaker, relationship, scoped_session
from sqlalchemy import create_engine
from sqlalchemy.util.compat import contextmanager


class BookstoreDao(object):
    def __init__(self, db_path):
        self.__db_path = db_path
        self.engine = create_engine('sqlite:///'+self.__db_path)
        self.SessionType = scoped_session(sessionmaker(bind=self.engine, expire_on_commit=False))

    def create_tables(self):
        Base.metadata.create_all(self.engine)

    def GetSession(self):
        return self.SessionType()

    @contextmanager
    def session_scope(self):
        session = self.GetSession()
        try:
            yield session
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

    def get_books(self):
        with self.session_scope() as session:
            return session.query(Book).all()

    def get_book(self, book_id):
        print('query book_id', book_id, type(book_id))
        with self.session_scope() as session:
            return session.query(Book).get(book_id)

    def get_article(self, article_id):
        with self.session_scope() as session:
            return session.query(Article).filter(Article.id == article_id).first()

    def get_catalog(self, book_id):
        with self.session_scope() as session:
            return session.query(Catalog).filter(Catalog.book_id == book_id).all()

    def write(self, obj):
        with self.session_scope() as session:
            return session.add(obj)


Base = declarative_base()


class Book(Base):
    __tablename__ = 'tb_book'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(32))
    author = Column(String(16))
    intro = Column(String(128))


class Catalog(Base):
    __tablename__ = 'tb_catalog'
    id = Column(Integer, primary_key=True, autoincrement=True)
    book_id = Column(Integer)
    chapter_id = Column(Integer)
    title = Column(String(32))
    intro = Column(String(128))


class Article(Base):
    __tablename__ = 'tb_article'
    id = Column(Integer, primary_key=True, autoincrement=True)
    author = Column(String(16))
    pub_date = Column(String(16))
    title = Column(String(32))
    content = Column(Text)
    footnotes = Column(Text)
    intro = Column(Text)
    translation = Column(Text)
    notes = Column(Text)


