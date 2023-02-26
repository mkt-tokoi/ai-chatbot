import io
from copy import copy

import openai
import requests
from linebot.models import MessageEvent, TemplateSendMessage, CarouselTemplate, CarouselColumn, PostbackAction, \
    MessageAction, PostbackEvent, SendMessage
from linebot.models import (BoxComponent, BubbleContainer, FlexSendMessage,
                            ImageComponent, TextComponent, TextSendMessage, URIAction, ImageSendMessage)
import urllib.parse
from fastapi import FastAPI

from app.linebot import LineBot

# LINE Botに関するインスタンス作成

conversations = {}


class Davinci3Bot(LineBot):
    def __init__(self, fast_api: FastAPI):
        super().__init__(fast_api, '/linebot/davinci3')

    def handle_message(self, event: MessageEvent, dest) -> SendMessage:
        line_user_id = event.source.user_id
        user_msg = event.message.text

        if (user_msg in {"reset", "リセット"}):
            self.reset_conversation(line_user_id)
            return TextSendMessage(text='(会話をリセットしました)')
        else:
            # 会話を更新（ユーザ発言）
            self.add_user_msg_to_conversation(line_user_id, user_msg)
            conversation = self.get_conversation(line_user_id)
            conversation = conversation + "\n" + f"AI: "

            response = openai.Completion.create(
                engine='text-davinci-003',
                prompt=conversation,
                max_tokens=1000,
                temperature=0.9,  # ランダムさ。創造的にするには0.9、答えがある場合は0推奨。top_pと同時変更は非推奨（デフォルト:1）
                stop='.')
            r_text = response['choices'][0]['text']
            r_text = r_text.strip()
            token_usage = response['usage']['total_tokens']
            token_remain = 4000 - token_usage

            # 会話を更新（AI発言）
            self.add_ai_msg_to_conversation(line_user_id, r_text)
            if token_remain < 1000:
                return TextSendMessage(text=r_text + f"\n(残トークン: {token_remain} です。'リセット'と入力すると会話をリセットできます)")
            else:
                return TextSendMessage(text=r_text)

    def handle_postback(self, event: PostbackEvent, dest) -> SendMessage:
        return TextSendMessage(text="？？")

    def reset_conversation(self, line_user_id):
        if line_user_id in conversations:
            del conversations[line_user_id]

    def check_conversation(self, line_user_id):
        if line_user_id not in conversations:
            conversations[line_user_id] = f""

    def get_conversation(self, line_user_id):
        self.check_conversation(line_user_id)
        return conversations[line_user_id]

    def add_ai_msg_to_conversation(self, line_user_id, ai_msg):
        self.check_conversation(line_user_id)
        conversations[line_user_id] = conversations[line_user_id] + "/n" + f"AI: " + ai_msg

    def add_user_msg_to_conversation(self, line_user_id, usr_msg):
        user_name = self.get_user_name(line_user_id)
        self.check_conversation(line_user_id)
        conversations[line_user_id] = conversations[line_user_id] + "/n" + f"{user_name}: " + usr_msg

    def get_user_name(self, line_user_id):
        try:
            profile = self.linebot_api.get_profile(line_user_id)
            return profile.display_name
        except:
            return f"{line_user_id[:3]}さん"
