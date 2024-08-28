"""pdf to dxf converter script"""

import uuid
from pydantic import BaseModel
from fastapi import APIRouter


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
