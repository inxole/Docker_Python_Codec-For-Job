import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from opinion_method import router as opinion_router
from Converter.jpg_png_method import router as jpg_png_router
from Converter.pdf_method import router as pdf_router
from Trans_dxf.dxf_method import router as dxf_router
from Split_Tie.pdf_split_or_tie_method import router as pdf_split_or_tie_router
from Cutout.flv_cut_method import router as flv_cut_router

app = FastAPI(root_path="/api")

dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path)
front_url = os.environ['Front_URL']
origins = [front_url]

# CORSの設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 各モジュールのルーターを登録
app.include_router(opinion_router)
app.include_router(jpg_png_router)
app.include_router(pdf_router)
app.include_router(dxf_router)
app.include_router(pdf_split_or_tie_router)
app.include_router(flv_cut_router)
