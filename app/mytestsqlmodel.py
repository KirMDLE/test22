from typing import Annotated, List

from fastapi import Depends, FastAPI, HTTPException, Query

from sqlmodel import Field, Session, SQLModel, create_engine, select

class Hero(SQLModel, table=True):
    id: int | None  = Field (default=None, primary_key=True)
    name: str = Field(index=True)
    age: int | None = Field(default=None, index=True)
    secret_name: str

sqlite_file_name = 'database.db'
sqlite_url = f'sqlite:///{sqlite_file_name}'    

connect_args = {'check_same_thread': False}
engine = create_engine(sqlite_url, connect_args=connect_args)


def create_db_and_table():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)] 


app = FastAPI()

@app.on_event('start_up')
def on_startup():
    create_db_and_table()

@app.post('/heroes/')
def create_hero(hero: Hero, session: SessionDep) -> Hero:
    session.add(hero)
    session.commit()
    session.refresh(hero)
    return hero    


@app.get('/heroes/')
def read_heroes(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> List[Hero]:
    heroes = session.exec(select(Hero).offset(offset).limit(limit)).all()
    return heroes

@app.get('/heroes/{hero_id}')
def read_hero(hero_id: int, session: SessionDep) -> Hero:
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="hero not found")
    return hero

@app.delete('/heroes/{hero_id}')
def delete_hero(hero_id: int, session: SessionDep) -> Hero:
    hero= session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="hero not found")
    session.delete(Hero)
    session.commit()
    return {'ok': True}


class HeroBase(SQLModel):
    name: str = Field(index=True)
    age: int | None = Field(default=None, index=True)


class Hero(HeroBase):
    id: int |  None = Field(default=None, primary_key=True)
    secret_name: str


class HeroPublic(HeroBase):
    id: int   


class HeroCreate(HeroBase):
    secret_name: str


class HeroUpdate(HeroBase): 
    name: str | None = None
    age: int | None = None
    secret_name: str | None = None


@app.post('/heroes', response_model=HeroPublic)
def create_hero(hero: HeroCreate, session: SessionDep):
    db_hero = Hero.model_validate(hero)
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero    

@app.get('/heroes/', resposne_model=list[HeroPublic])
def read_heroes(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
):
    heroes = session.exec(select(Hero).offset(offset).limit(limit)).all()
    return heroes

@app.get('/heroes/{hero_id}', response_model=HeroPublic)
def read_hero(hero_id: int, session: SessionDep):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404,detail="hero not found")
    return hero


@app.patch('/heroes/{hero_id}', response_model= HeroPublic)
def update_hero(hero_id: int, hero: HeroUpdate, session: SessionDep):
    hero_db = session.get(Hero, hero_id)
    if not hero_db:
        raise HTTPException(status_code=404, detail='hero not found')
    hero_data = hero.model_dump(exclude_unset = True)
    hero_db.sqlmodel_update(hero_data)
    session.add(hero_db)
    session.commit()
    session.refresh(hero_db)
    return hero_db


@app.delete('/heroes/{hero_id}')
def delete_hero(hero_id: int, session: SessionDep):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail='user not found')
        session.delete(hero)
        session.commit()
        return {'ok': True}
    
    