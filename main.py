import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
import yt_dlp

SUPPORTED_SITES = [
    'youtube.com', 'youtu.be', 'tiktok.com', 'facebook.com', 'fb.watch', 'instagram.com', 'instagr.am'
]
DOWNLOAD_DIR = "./downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def is_supported_url(url):
    return any(site in url for site in SUPPORTED_SITES)

async def download_media(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    if is_supported_url(url):
        await update.message.reply_text("🔄 Downloading...")
        try:
            ydl_opts = {
                'format': 'bestvideo+bestaudio/best',
                'outtmpl': os.path.join(DOWNLOAD_DIR, '%(title)s.%(ext)s'),
                'merge_output_format': 'mp4',
                'noplaylist': True,
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
            await update.message.reply_text(f"✅ Downloaded:\n{os.path.basename(filename)}")
        except Exception as e:
            await update.message.reply_text(f"❌ Error: {e}")
    else:
        await update.message.reply_text("⚠️ Only YouTube, TikTok, Facebook, or Instagram links are supported.")

async def main():
    TOKEN ="7554977187:AAFDghX_WsB1cGU43cYOTRzHGDO1PWj8Zrg"
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), download_media))
    print("🤖 Bot Started! Paste any supported link in Telegram.")
    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
