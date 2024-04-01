how to run

bash
poetry install
poetry shell
uvicorn main:app --reload --host 0.0.0.0

flowchart TD
A[PDFファイルを選択] --> |post script| B[PDFをfastAPIに送信]
B --> C{fastAPIバックエンド}
C --> |PDFファイル名を変更 uuid_name.pdf| E[UUIDを作成]
C --> |リクエストボディにUUIDを送信| F[リクエストボディ]
E --> |DXFに変換| G[PDF to DXFスクリプト]
F --> |ブラウザにUUIDを保持| H[ブラウザ]
G --> |DXFファイルを作成 uuid_name.dxf| I[ZIPファイル作成]
I --> |ZIPファイルを送信| J[get request]
J --> |UUIDを照合| K[UUID照合処理]
K --> L[一致したブラウザにファイル送信]
