import os
from pyrogram import Client as AFK, idle
from pyrogram.enums import ChatMemberStatus, ChatMembersFilter
from pyrogram import enums
from pyrogram.types import ChatMember
import asyncio
import logging
import tgcrypto
from pyromod import listen
import logging
from tglogging import TelegramLogHandler

# Config 
class Config(object):
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "7048745210:AAEGqNT9HhWBQzglDafW2T3g_UQTUX0aoPo")
    API_ID = int(os.environ.get("API_ID",  "25933223"))
    API_HASH = os.environ.get("API_HASH", " 6ef5a426d85b7f01562a41e6416791d3")
    DOWNLOAD_LOCATION = "./DOWNLOADS"
    SESSIONS = "./SESSIONS"

    AUTH_USERS = os.environ.get('AUTH_USERS', '6488911325').split(',')
    for i in range(len(AUTH_USERS)):
        AUTH_USERS[i] = int(AUTH_USERS[i])

    GROUPS = os.environ.get('GROUPS', '-1002075880942').split(',')
    for i in range(len(GROUPS)):
        GROUPS[i] = int(GROUPS[i])

    LOG_CH = os.environ.get("LOG_CH", "-1002059340064")

# TelegramLogHandler is a custom handler which is inherited from an existing handler. ie, StreamHandler.
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt='%d-%b-%y %H:%M:%S',
    handlers=[
        TelegramLogHandler(
            token=Config.BOT_TOKEN, 
            log_chat_id= Config.LOG_CH, 
            update_interval=2, 
            minimum_lines=1, 
            pending_logs=200000),
        logging.StreamHandler()
    ]
)

LOGGER = logging.getLogger(__name__)
LOGGER.info("live log streaming to telegram.")


# Store
class Store(object):
    CPTOKEN = "eyJhbGciOiJIUzM4NCIsInR5cCI6IkpXVCJ9.eyJzb3VyY2UiOjUwLCJzb3VyY2VfYXBwIjoiY2xhc3NwbHVzIiwic2Vzc2lvbl9pZCI6IjdmODNhNzkxLTliM2YtNGM5Ni05Mjg1LWZjNWU0ZTYyOTVjYSIsInZpc2l0b3JfaWQiOiJjZmEzZmU0Mi1jNDNiLTQwNzYtYWMxYy03OTE3ZTU3NDVhYmIiLCJjcmVhdGVkX2F0IjoxNzUwNDg1MzQzNDAyLCJuYW1lIjoiU2hyZW5payBKYWluLSBTdHVkeSBTaW1wbGlmaWVkIiwib3JnX2NvZGUiOiJueHBnZCIsIm9yZ19pZCI6NTk5NywicGhvbmUiOiI5MTY3NTQ2NzU0ODAiLCJzb3VyY2VfdXNlcl9pZCI6IjE1NDQwMjgyNCIsInVzZXJfdHlwZSI6MSwiZW1haWwiOiJtb3lvdDI5ODI2QGNhbG9ycGcuY29tIiwiaXNfdXNlcmlkX2V2ZW4iOnRydWUsImNhdGVnb3J5IjoiSzEyIiwiY29ob3J0IjoiRmF0IEhlYWQiLCJpc19zdG9yZSI6MSwiaWF0IjoxNzUwNDg1MzQ0LCJleHAiOjE3NTE3ODEzNDR9.AoPHr3O3o_lH2XuZPjQd2DvfNNXS0UylVBMs6D60KA8DCkwNitBZxGtVgq2NBSs3"
    SPROUT_URL = "https://discuss.oliveboard.in/"
    ADDA_TOKEN = "eyJhbGciOiJSUzI1NiIsImtpZCI6IjFiYjc3NGJkODcyOWVhMzhlOWMyZmUwYzY0ZDJjYTk0OGJmNjZmMGYiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJhY2NvdW50cy5nb29nbGUuY29tIiwiYXpwIjoiMTE3NTc1Nzc2MzYwLXNlM3ViYWtybWlqMnE1bW91azJyazQ2NzQwaXB1cmNhLmFwcHMuZ29vZ2xldXNlcmNvbnRlbnQuY29tIiwiYXVkIjoiMTE3NTc1Nzc2MzYwLXNlM3ViYWtybWlqMnE1bW91azJyazQ2NzQwaXB1cmNhLmFwcHMuZ29vZ2xldXNlcmNvbnRlbnQuY29tIiwic3ViIjoiMTA0NjYxMDkyNTIzODE0NzUxODQyIiwiZW1haWwiOiJjaGF2ZGFzdWphbDAwMkBnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiYXRfaGFzaCI6Ik5Wd3VkWE50WnR5blFCY1hLaFVfU0EiLCJuYmYiOjE3NTA0ODU0NzgsIm5hbWUiOiJjaGF2ZGEgc3VqYWwiLCJwaWN0dXJlIjoiaHR0cHM6Ly9saDMuZ29vZ2xldXNlcmNvbnRlbnQuY29tL2EvQUNnOG9jSmdQQ0pIeXE0ckpscmZqSktDN1VMYi1mbF9aR0xRX19PQWFVSVFzSWtoWlFla3hnPXM5Ni1jIiwiZ2l2ZW5fbmFtZSI6ImNoYXZkYSIsImZhbWlseV9uYW1lIjoic3VqYWwiLCJpYXQiOjE3NTA0ODU3NzgsImV4cCI6MTc1MDQ4OTM3OCwianRpIjoiYWU5MzZiNjY4YWFkNjNlYjVhYThiMzc5MDI1NDg0YjJhOTQyZDk4NiJ9.lUE6U-hRXt8vKuFEYD-a6iE7cO6cMTmx-5nAmXGU3qz1WOruktEzdjyqpvK5iui_877m9VEKWiKugN_4WWyTBmlwYhTj468LI0w5jgEmLYSZVksZzGq693A3PiRXC8kkRvPhW_-2CiTNl60TlnVVu1mlqO5_ml5gIzKIvOLldl6Osug0l1WzYnZW1SARezE4ONqYUNtafadaTFhEA7i3xDXARcEQ9PY6ChbxMPBPfnRkKrBnAMI9PgDJoFOGsmmXAAPz_IwpPlpsGUNMs_msKzJ8UtOEiqE3FsUu-f_T_RRzZS22RuNxYCtudy_r0YMo-lNzFJRReOKHcAhuwj5OWw"
    THUMB_URL = "https://telegra.ph/file/84870d6d89b893e59c5f0.jpg"

# Format
class Msg(object):
    START_MSG = "**/pro**"

    TXT_MSG = "Hey <b>{user},"\
        "\n\n`I'm Multi-Talented Robot. I Can Download Many Type of Links.`"\
            "\n\nSend a TXT or HTML file :-</b>"

    ERROR_MSG = "<b>DL Failed ({no_of_files}) :-</b> "\
        "\n\n<b>Name: </b>{file_name},\n<b>Link:</b> `{file_link}`\n\n<b>Error:</b> {error}"

    SHOW_MSG = "<b>Downloading :- "\
        "\n`{file_name}`\n\nLink :- `{file_link}`</b>"

    CMD_MSG_1 = "`{txt}`\n\n**Total Links in File are :-** {no_of_links}\n\n**Send any Index From `[ 1 - {no_of_links} ]` :-**"
    CMD_MSG_2 = "<b>Uploading :- </b> `{file_name}`"
    RESTART_MSG = "✅ HI Bhai log\n✅ PATH CLEARED"

# Prefixes
prefixes = ["/", "~", "?", "!", "."]

# Client
plugins = dict(root="plugins")
if __name__ == "__main__":
    if not os.path.isdir(Config.DOWNLOAD_LOCATION):
        os.makedirs(Config.DOWNLOAD_LOCATION)
    if not os.path.isdir(Config.SESSIONS):
        os.makedirs(Config.SESSIONS)

    PRO = AFK(
        "AFK-DL",
        bot_token=Config.BOT_TOKEN,
        api_id=Config.API_ID,
        api_hash=Config.API_HASH,
        sleep_threshold=120,
        plugins=plugins,
        workdir= f"{Config.SESSIONS}/",
        workers= 2,
    )

    chat_id = []
    for i, j in zip(Config.GROUPS, Config.AUTH_USERS):
        chat_id.append(i)
        chat_id.append(j)
    
    
    async def main():
        await PRO.start()
        # h = await PRO.get_chat_member(chat_id= int(-1002115046888), user_id=6695586027)
        # print(h)
        bot_info = await PRO.get_me()
        LOGGER.info(f"<--- @{bot_info.username} Started --->")
        
        for i in chat_id:
            try:
                await PRO.send_message(chat_id=i, text="**Bot Started! ♾ /pro **")
            except Exception as d:
                print(d)
                continue
        await idle()

    asyncio.get_event_loop().run_until_complete(main())
    LOGGER.info(f"<---Bot Stopped--->")
