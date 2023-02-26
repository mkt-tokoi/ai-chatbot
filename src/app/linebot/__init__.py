import io
from copy import copy
from abc import abstractmethod
from abc import ABCMeta

import openai
import requests
from fastapi import Header, Request
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from starlette.exceptions import HTTPException
from app.conf_and_cert import *
from app.conf_and_cert import OPENAI_API_KEY
from linebot.models import MessageEvent, TemplateSendMessage, CarouselTemplate, CarouselColumn, PostbackAction, \
    MessageAction, PostbackEvent, SendMessage
from linebot.models import (BoxComponent, BubbleContainer, FlexSendMessage,
                            ImageComponent, TextComponent, TextSendMessage, URIAction, ImageSendMessage)
import urllib.parse
from fastapi import FastAPI

openai.api_key = OPENAI_API_KEY
# LINE Botに関するインスタンス作成

histories = {}


class LineBot(metaclass=ABCMeta):
    def __init__(self, fast_api: FastAPI, path: str):
        self.linebot_api: LineBotApi = LineBotApi(LINEBOT_CHANNEL_ACCESS_TOKEN)
        self.webhook_handler: WebhookHandler = WebhookHandler(LINEBOT_CHANNEL_SECRET)
        fast_api.post(path)(self.handle_line_webhook_call)
        self.webhook_handler.add(MessageEvent)(self.__handle_message)
        self.webhook_handler.add(PostbackEvent)(self.__handle_postback)

    async def handle_line_webhook_call(self, request: Request, x_line_signature=Header(None)):
        body = await request.body()
        try:
            self.webhook_handler.handle(body.decode("utf-8"), x_line_signature)
            return "OK"
        except InvalidSignatureError:
            raise HTTPException(status_code=400, detail="InvalidSignatureError")

    def __handle_message(self, *args):
        self.handle_with(self.handle_message, *args)

    def __handle_postback(self, *args):
        self.handle_with(self.handle_postback, *args)

    def handle_with(self, handler, *args):
        try:
            response = handler(*args)
            self.linebot_api.reply_message(args[0].reply_token, response)
        except Exception as e:
            response = TextSendMessage("Error（ごめん。ちょっとバグってます）")
            self.linebot_api.reply_message(args[0].reply_token, response)
            raise e

    @abstractmethod
    def handle_message(self, event: MessageEvent, dest) -> SendMessage:
        pass

    @abstractmethod
    def handle_postback(self, event: PostbackEvent, dest) -> SendMessage:
        pass
