
from pyrogram import Client, filters
import re

BOT_TOKEN = "PUT_YOUR_BOT_TOKEN_HERE"

API_ID = 12345
API_HASH = "your_api_hash"

SOURCE = "@source_channel_username"
TARGET = "@your_target_channel"

url_regex = re.compile(r"https?://|www\.|t\.me/|telegram\.me/")

def has_link(msg):
    text = (msg.text or "") + " " + (msg.caption or "")
    if url_regex.search(text):
        return True
    if getattr(msg, "entities", None):
        for e in msg.entities:
            if e.type in ("url","text_link"):
                return True
    if getattr(msg, "caption_entities", None):
        for e in msg.caption_entities:
            if e.type in ("url","text_link"):
                return True
    return False

def is_apk(msg):
    doc = getattr(msg, "document", None)
    if not doc:
        return False
    name = (doc.file_name or "").lower()
    mime = (doc.mime_type or "").lower()
    if name.endswith(".apk") or "apk" in mime:
        return True
    return False

app = Client(
    "fwd_bot",
    bot_token=BOT_TOKEN,
    api_id=API_ID,
    api_hash=API_HASH
)

@app.on_message(filters.chat(SOURCE))
async def fwdr(client, msg):
    try:
        if has_link(msg):
            return
        if is_apk(msg):
            return
        await client.copy_message(
            chat_id=TARGET,
            from_chat_id=msg.chat.id,
            message_id=msg.id
        )
    except Exception as e:
        print("Error:", e)

app.run()
