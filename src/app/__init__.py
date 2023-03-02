import os
from fastapi import FastAPI
from fastapi.responses import FileResponse
import app.linebot as linebot_handlers
from app.linebot.dalle2 import Dalle2Bot
from app.linebot.davinci3 import Davinci3Bot
from app.linebot.gpt35turbo import GPT35TurboBot

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
bot1 = Dalle2Bot(fast_api)
bot2 = Davinci3Bot(fast_api)
bot3 = GPT35TurboBot(fast_api)
