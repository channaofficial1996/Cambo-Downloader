from telegram.ext import Updater, MessageHandler, Filters
import yt_dlp
import os

SUPPORTED_SITES = [
    'youtube.com', 'youtu.be', 'tiktok.com', 'facebook.com', 'fb.watch', 'instagram.com', 'instagr.am'
]

def is_supported_url(url):
    return any(site in url for site in SUPPORTED_SITES)

DOWNLOAD_DIR = "./downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def download_media(update, context):
    url = update.message.text.strip()
    if is_supported_url(url):
        update.message.reply_text("🔄 Downloading...")
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
            update.message.reply_text(f"✅ Downloaded:\n{os.path.basename(filename)}")
        except Exception as e:
            update.message.reply_text(f"❌ Error: {e}")
    else:
        update.message.reply_text(
            "⚠️ Only YouTube, TikTok, Facebook, or Instagram links are supported."
        )

def main():
    import os
    TOKEN ="7554977187:AAFDghX_WsB1cGU43cYOTRzHGDO1PWj8Zrg"
    updater = Updater(TOKEN, use_context=True)
    updater.dispatcher.add_handler(
        MessageHandler(Filters.text & ~Filters.command, download_media)
    )
    print("🤖 Bot Started! Paste any supported link in Telegram.")
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

