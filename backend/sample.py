from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# CORSの設定
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 本番環境では適切なオリジンに限定
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Item(BaseModel):
    """a"""
    name: str
    description: str = None
    price: float
    tax: float = None


@app.post("/item")
def create_item(item: Item):
    # save item
    # ファイルを書き込みモードで開く（'w'を使用）。ファイルが存在しない場合は新しく作成される
    with open('example.txt', 'a') as file:
        file.write('こんにちは、Python!\n')
        file.write('これはテキストファイルへの書き込みの例です。\n')

    return {"msg": "test", "item": item}


@app.get("/item")
def get_date():
    # pull
    with open('example.txt', 'r') as file:
        content = file.read()
    return {content}

# should be created example.txt file
