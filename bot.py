from pyrogram import Client, filters
from pytgcalls import PyTgCalls, idle
from pytgcalls.types import Update
from pytgcalls.types.stream import StreamAudioEnded
from pytgcalls.types.input_stream import InputStream, AudioPiped
from yt_dlp import YoutubeDL
import asyncio
from config import Config

app = Client(
    "MusicBot",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN
)

pytgcalls = PyTgCalls(app)
queues = {}

def yt_search(query):
    opts = {"format": "bestaudio", "noplaylist": True}
    with YoutubeDL(opts) as ydl:
        info = ydl.extract_info(f"ytsearch:{query}", download=False)['entries'][0]
    return info['url'], info['title']

@app.on_message(filters.command("play") & filters.group)
async def play(_, message):
    chat_id = message.chat.id
    if len(message.command) < 2:
        return await message.reply("Usage: /play <song name or YouTube link>")

    query = " ".join(message.command[1:])
    url, title = yt_search(query)

    if chat_id not in queues:
        queues[chat_id] = []

    queues[chat_id].append((url, title))
    await message.reply(f"Added to queue: **{title}**")

    if len(queues[chat_id]) == 1:
        await start_stream(chat_id)

async def start_stream(chat_id):
    url, title = queues[chat_id][0]
    await pytgcalls.join_group_call(
        chat_id,
        InputStream(AudioPiped(url))
    )

@pytgcalls.on_stream_end()
async def on_end(_, update: Update):
    if isinstance(update, StreamAudioEnded):
        chat_id = update.chat_id
        queues[chat_id].pop(0)
        if queues[chat_id]:
            await start_stream(chat_id)
        else:
            await pytgcalls.leave_group_call(chat_id)

async def main():
    await app.start()
    await pytgcalls.start()
    print("Bot is running...")
    await idle()

if __name__ == "__main__":
    asyncio.run(main())
