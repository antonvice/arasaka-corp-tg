import hydrogram as hg
from dotenv import load_dotenv
import os


import logging
logging.basicConfig(level=logging.INFO)

# Load environment variables
load_dotenv()

app = hg.Client(os.getenv("TELEGRAM_PERSONAL_SESH"), os.getenv("TELEGRAM_API_ID"), os.getenv("TELEGRAM_API_HASH"))


@app.on_message(hg.filters.private)
async def hello(client, message):
    await message.reply("Привет")
    
    
app.run()