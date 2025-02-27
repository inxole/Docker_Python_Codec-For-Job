"""pdf to dxf converter script"""

from fastapi import APIRouter, HTTPException, status
from sqlmodel import Session, SQLModel, create_engine, Field, select


class Opinion(SQLModel, table=True):
    id: str = Field(default_factory=None, primary_key=True)
    content: str


engine = create_engine("mysql://test:test@db/test")
SQLModel.metadata.create_all(engine)

router = APIRouter()


def save_opinion(opinion: Opinion):
    with Session(engine) as session:
        session.add(opinion)
        session.commit()
        session.refresh(opinion)
    return opinion


def load_opinions():
    with Session(engine) as session:
        opinions = session.exec(select(Opinion)).all()
    return opinions


@router.post("/opinions/")
def create_opinion(opinion: Opinion):
    try:
        saved_opinion = save_opinion(opinion)
        return saved_opinion
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error saving opinion") from e


@router.get("/opinions/")
def read_opinions():
    try:
        return load_opinions()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Error loading opinions") from e


@router.delete("/opinions/{opinion_id}")
def delete_opinion(opinion_id: str):
    with Session(engine) as session:
        opinion = session.get(Opinion, opinion_id)
        if not opinion:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f'Opinion with id {opinion_id} not found')
        session.delete(opinion)
        session.commit()
    return {"message": "Opinion deleted"}
