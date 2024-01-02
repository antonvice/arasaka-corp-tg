import hydrogram as hg
from dotenv import load_dotenv
import os
import numpy as np

from faster_whisper import WhisperModel

model = WhisperModel(model_size_or_path="tiny", device="cpu", compute_type="int8")
import tempfile
import gc
import asyncio

from pytgcalls import PyTgCalls
from pytgcalls import idle
from pytgcalls.types import MediaStream

groupchat=os.getenv("GROUP_CHAT_ID")

def convert_byte_to_mp3(audio_content):
    # If the audio content is a numpy array, convert it to bytes
    if isinstance(audio_content, np.ndarray):
        audio_content = audio_content.astype(np.int16).tobytes()

    # Create a temporary file with a .mp3 extension
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_file:
        temp_file.write(audio_content)
        temp_file_path = temp_file.name

    return temp_file_path

import logging
logging.basicConfig(level=logging.INFO)

# Load environment variables
load_dotenv()


async def transcribe_audio_message(client, message):
    chat_id = message.chat.id
    voice = message.voice

    audio = await client.download_media(voice, in_memory=True)

    with open(convert_byte_to_mp3(bytes(audio.getbuffer())), 'rb') as a:
            # Pass the audio array to your model for transcription
            segments, _ = model.transcribe(a, beam_size=5)
            text = ''
            for segment in segments:
                text += segment.text + ' '  # Concatenate the sentence and add a space betwee
    del audio
    gc.collect()
    await message.reply(text)

import re
async def play(app):
    await app.start()
    await app.join_group_call (
    os.getenv("GROUP_CHAT_ID"),
    MediaStream(
    'http://docs.evostream.com/sample_content/assets/sintel1m720p.mp4',
    )
    )
    await idle()




    
async def main():
    bot = hg.Client("MrBot", api_hash=os.getenv("TELEGRAM_API_HASH"),api_id=os.getenv("TELEGRAM_API_ID"), bot_token=os.getenv("BOT_TOKEN"))
        
    sigma = hg.Client("SIGMA_BOT", os.getenv("TELEGRAM_API_ID"), os.getenv("TELEGRAM_API_HASH"), bot_token=os.getenv("SIGMA_BOT_TOKEN"))
    ai = hg.Client("AI_BOT", os.getenv("TELEGRAM_API_ID"), os.getenv("TELEGRAM_API_HASH"), bot_token=os.getenv("AI_BOT_TOKEN"))
    client = hg.Client(os.getenv("TELEGRAM_PERSONAL_SESH"), os.getenv("TELEGRAM_API_ID"), os.getenv("TELEGRAM_API_HASH"))
    call = hg.Client("DJBOT", api_hash=os.getenv("TELEGRAM_API_HASH"),api_id=os.getenv("TELEGRAM_API_ID"), bot_token=os.getenv("DJ_BOT_TOKEN"))
    
    apps = [bot, sigma, ai, client]
    dj = PyTgCalls(call)
    
    async def request_song(client, message):
        print("New message in @ArasakaChat")
        match = re.search('hey dj(.*)', message.text.lower())
        if match:
            after_phrase = match.group(1)
            print(after_phrase)
            await play(dj)
    # apps[0].add_handler(hg.handlers.MessageHandler(request_song, filters=(hg.filters.group & hg.filters.user(os.getenv("TELEGRAM_PERSONAL_SESH")))))
    apps[0].add_handler(hg.handlers.MessageHandler(transcribe_audio_message, filters=(hg.filters.group & (hg.filters.voice & hg.filters.user(os.getenv("TELEGRAM_PERSONAL_SESH"))))))


    await hg.compose(apps)
    
if __name__ == '__main__':
    import uvloop
    uvloop.install()
    asyncio.run(main())