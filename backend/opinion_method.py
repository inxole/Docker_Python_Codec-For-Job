"""pdf to dxf converter script"""

import uuid
from typing import Optional
from pydantic import BaseModel
from fastapi import APIRouter
from sqlmodel import Field, Session, SQLModel, create_engine


class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    secret_name: str
    age: Optional[int] = None


hero_1 = Hero(name="Deadpond", secret_name="Dive Wilson")
hero_2 = Hero(name="Spider-Boy", secret_name="Pedro Parqueador")
hero_3 = Hero(name="Rusty-Man", secret_name="Tommy Sharp", age=48)

engine = create_engine("mysql://test:test@db/test")

SQLModel.metadata.create_all(engine)

with Session(engine) as session:
    session.add(hero_1)
    session.add(hero_2)
    session.add(hero_3)
    session.commit()


router = APIRouter()


class Opinion(BaseModel):
    """test"""
    id: str
    content: str


def save_opinion(opinion: Opinion):
    """test"""
    with open("opinions.txt", "a", encoding="utf-8") as file:
        file.write(f"{opinion.id}:{opinion.content}\n")


def load_opinions():
    """test"""
    opinions = []
    try:
        with open("opinions.txt", "r", encoding="utf-8") as file:
            for line in file:
                opinion_id, content = line.strip().split(":")
                opinions.append(Opinion(id=opinion_id, content=content))
    except FileNotFoundError:
        pass
    return opinions


@router.post("/opinions/")
def create_opinion(opinion: Opinion):
    """test"""
    opinion.id = str(uuid.uuid4())
    save_opinion(opinion)
    return opinion


@router.get("/opinions/")
def read_opinions():
    """test"""
    return load_opinions()


@router.delete("/opinions/{opinion_id}")
def delete_opinion(opinion_id: str):
    """test"""
    opinions = load_opinions()
    opinions = [opinion for opinion in opinions if opinion.id != opinion_id]
    with open("opinions.txt", "w", encoding="utf-8") as file:
        for opinion in opinions:
            file.write(f"{opinion.id}:{opinion.content}\n")
    return {"message": "Opinion deleted"}
