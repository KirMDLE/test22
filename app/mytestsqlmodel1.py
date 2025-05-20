from typing import Annotated, List, Optional
from fastapi import Depends, FastAPI, HTTPException
from sqlmodel import Field, Relationship, SQLModel, Session, create_engine, select


class Book(SQLModel, table=True):
    id: int = Field(primary_key=True)
    title: str
    author: str
    year: int
    reader_id: int = Field(foreign_key='reader_.id')
    reader: "Reader" = Relationship(back_populates="books")


class BookCreate(SQLModel):
    title: str
    author: str
    year: int



class BookUpdate(SQLModel):
    title: str | None = None
    author: str | None = None
    year: int | None = None


class Reader(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str
    email: str
    age: int
    books: List['Book'] = Relationship(back_populates='reader')

    

class ReaderUpdate(SQLModel):
    name: Optional[str] = None
    email: Optional[str] = None
    age: Optional[int] = None



sqlite_db = 'database.db'
sqlite_url= f'sqlite:///{sqlite_db}'
connect_args = {'check_same_thread' : False}
engine = create_engine(sqlite_url, connect_args=connect_args)

def create_db_and_table():
    SQLModel.metadata.create_all(engine)


app=FastAPI()    


def get_session():
    with Session(engine) as session:
        yield session

SessionDepends = Annotated[Session, Depends(get_session)]

@app.post('/books/')
def add_book(book: Book, session: SessionDepends):
    db_book = Book.model_validate(book)
    session.add(db_book)
    session.commit()
    session.refresh(db_book)
    return db_book


@app.get('/books/')
def get_books(session: SessionDepends,
    offset: int = 0,
    limit: int = 10
 ) -> List[Book]:   
    books = session.exec(select(Book).offset(offset).limit(limit)).all()
    return books


@app.get('/books/{book_id}')
def get_book_id(book_id: int, session: SessionDepends) -> Book:
    get_book = session.get(Book, book_id)
    if not get_book:
        raise HTTPException(status_code=404, detail='book not found')
    return get_book


@app.patch('/books/{book_id}')
def update_book(book_id: int,book: BookUpdate, session: SessionDepends) -> Book:
    upd_book = session.get(Book, book_id)
    if not upd_book:
        raise HTTPException(status_code=404, detail='book not found')
    upd_inf= book.model_dump(exclude_unset = True)
    upd_book.sqlmodel_update(upd_inf)
    session.add(upd_book)
    session.commit()
    session.refresh(upd_book)
    return upd_book


@app.delete('/books/{book_id}')
def del_book(book_id: int, session: SessionDepends) -> Book:
    de_book = session.get(Book, book_id)
    if not de_book:
        raise HTTPException(status_code=404, detail='book not found')
    session.delete(de_book)
    session.commit()
    return {"ok": True}


@app.post('/readers/')
def add_reader(reader: Reader, session: SessionDepends) -> Reader:
    db_reader = Reader.model_validate(reader)
    session.add(db_reader)
    session.commit()
    session.refresh(db_reader)
    return db_reader

@app.get('/readers/')
def get_readers(
    session: SessionDepends,
    name: Optional[str] = None,
    age: Optional[int] = None,
    email: Optional[str] = None,
    offset: int = 0,
    limit: int = 10
)-> List[Reader]:
    
    query = select(Reader)

    if name:
        query = query.where(Reader.name == name)

    if age:
        query=query.where(Reader.age == age)

    if email:
        query=query.where(Reader.email == email)

    query = query.offset(offset).limit(limit)

    readers = session.exec(query).all()

    return readers


@app.get('/readers/{reader_id}')
def get_reader(reader_id: int, session: SessionDepends) -> Reader:
    get_reader_db = session.get(Reader, reader_id)
    if not get_reader_db:
        raise HTTPException(status_code=404, detail='reader not found')
    return get_reader_db


@app.patch('/readers/{reader_id}')
def update_reader(reader_id: int, reader: ReaderUpdate, session: SessionDepends) -> Reader:
    upd_reader = session.get(Reader, reader_id)
    if not upd_reader:
        raise HTTPException(status_code=404, detail='reader not found')
    upd_info = reader.model_dump(exclude_unset=True)
    upd_reader.sqlmodel_update(upd_info)
    session.add(upd_reader)
    session.commit()
    session.refresh(upd_reader)

    return upd_reader

@app.delete('/readers/{reader_id}')
def del_reader(reader_id: int, session: SessionDepends) -> Reader:
    reader_to_delete = session.get(Reader, reader_id)
    if not reader_to_delete:
        raise HTTPException(status_code=404,detail="reader not found")
    session.delete(reader_to_delete)
    session.commit()
    return {'ok': True}


@app.get('/readers/{reader_id}/books')
def get_books_of_reader(reader_id: int, session:SessionDepends) -> Book:
    reader = session.get(Reader, reader_id)
    if not reader:
        raise HTTPException(status_code=404, detail='reader nof found')
    return reader.books




