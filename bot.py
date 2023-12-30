import hydrogram as hg
from dotenv import load_dotenv
import os
import numpy as np
import io
from faster_whisper import WhisperModel
model = WhisperModel(model_size_or_path="tiny", device="cpu", compute_type="int8")
import tempfile
import gc

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

bot_app = hg.Client("MrBot", api_hash=os.getenv("TELEGRAM_API_HASH"),api_id=os.getenv("TELEGRAM_API_ID"), bot_token=os.getenv("BOT_TOKEN"))


@bot_app.on_message(hg.filters.voice & hg.filters.user(os.getenv("TELEGRAM_PERSONAL_SESH")))
async def handle_docs_audio(client, message):
    chat_id = message.chat.id
    voice = message.voice

    audio = await bot_app.download_media(voice, in_memory=True)

    with open(convert_byte_to_mp3(bytes(audio.getbuffer())), 'rb') as a:
            # Pass the audio array to your model for transcription
            segments, _ = model.transcribe(a, beam_size=5)
            text = ''
            for segment in segments:
                text += segment.text + ' '  # Concatenate the sentence and add a space betwee
    del audio
    gc.collect()
    await message.reply(text)

@bot_app.on_message(hg.filters.group & hg.filters.user(os.getenv("TELEGRAM_PERSONAL_SESH")))
async def from_hydrogramchat(client, message):
    print("New less in @ArasakaChat")
    
@bot_app.on_message(hg.filters.group)
async def from_hydrogramchat(client, message):
    print("New message in @ArasakaChat")


    
bot_app.run()
