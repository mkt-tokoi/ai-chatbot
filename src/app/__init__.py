import os
from fastapi import FastAPI
from fastapi.responses import FileResponse
import app.linebot as linebot_handlers
from app.linebot.dalle2 import Dalle2Bot

# FastAPIのインスタンス作成
fast_api = FastAPI(title="study/dall.e_linebot", description="")

@fast_api.get(path="/",
              summary="For connectivity test only (GET)")
async def index():
    return FileResponse("static/index.html")


@fast_api.post(path="/",
               summary="For connectivity test only (POST))")
async def index_post():
    return FileResponse("static/index.html")


# ハンドラのロード。これがないと、ハンドラが登録されないので消さないこと
bot = Dalle2Bot(fast_api)
