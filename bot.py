import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import yt_dlpimport os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import yt_dlp

TOKEN = "8899546618:AAESiqhHXH139zQoe3VuJP19y5x9sEnGdJA"
bot = telebot.TeleBot(TOKEN)

search_results = {}

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = (
        "<b>Xoş gəldiniz!</b> 🎵\n\n"
        "Sadəcə mahnı adı göndərin, axtarıb tapacağam!\n"
        "Və ya birbaşa YouTube linki göndərə bilərsiniz."
    )
    bot.send_message(message.chat.id, welcome_text, parse_mode="HTML")

def download_and_send(chat_id, url, message_id):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': '%(id)s.%(ext)s',
        'noplaylist': True,
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            audio_file = filename.rsplit(".", 1)[0] + ".mp3"
            
            with open(audio_file, 'rb') as audio:
                title = info.get('title', 'Musiqi')
                performer = info.get('uploader', 'MP3 AZ')
                bot.send_audio(chat_id, audio, title=title, performer=performer)
                
            
            try:
                os.remove(audio_file)
            except:
                pass
            bot.delete_message(chat_id, message_id)
    except Exception as e:
        bot.send_message(chat_id, f"❌ Xəta baş verdi: {e}")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    text = message.text.strip()
    chat_id = message.chat.id

    if text.startswith("http://") or text.startswith("https://"):
        msg = bot.send_message(chat_id, "⏳ <b>Mahnı yüklənir, gözləyin...</b>", parse_mode="HTML")
        download_and_send(chat_id, text, msg.message_id)
        return

    bot.send_message(chat_id, f"🔍 <b>{text}</b> axtarılır...", parse_mode="HTML")

    try:
        ydl_opts = {
            'extract_flat': True,
            'max_downloads': 5,
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch5:{text}", download=False)
            entries = info.get('entries', [])

        if not entries:
            bot.send_message(chat_id, "❌ Heç nə tapılmadı.")
            return

        search_results[chat_id] = entries
        markup = InlineKeyboardMarkup()

        result_text = f"🔍 <b>{text}</b> üçün nəticələr:\n\n"
        for i, entry in enumerate(entries, 1):
            title = entry.get('title', 'Naməlum')
            duration = entry.get('duration_string', 'N/A')
            result_text += f"{i}. {title} ({duration})\n"
            markup.add(InlineKeyboardButton(str(i), callback_data=f"dl_{i-1}"))

        bot.send_message(chat_id, result_text, parse_mode="HTML", reply_markup=markup)
    except Exception as e:
        bot.send_message(chat_id, f"❌ Axtarış zamanı xəta: {e}")

@bot.callback_query_handler(func=lambda call: call.data.startswith('dl_'))
def callback_inline(call):
    chat_id = call.message.chat.id
    index = int(call.data.split('_')[1])
    
    if chat_id in search_results and index < len(search_results[chat_id]):
        entry = search_results[chat_id][index]
        url = entry.get('url') or f"https://www.youtube.com/watch?v={entry.get('id')}"
        
        msg = bot.send_message(chat_id, "⏳ <b>Mahnı yüklənir, gözləyin...</b>", parse_mode="HTML")
        bot.answer_callback_query(call.id, "Yükləmə başladı...")
        download_and_send(chat_id, url, msg.message_id)
    else:
        bot.answer_callback_query(call.id, "Məlumat tapılmadı, yenidən axtarış edin.")

bot.infinity_polling()

TOKEN = "8899546618:AAESiqhHXH139zQoe3VuJP19y5x9sEnGdJA"
bot = telebot.TeleBot(TOKEN)

search_results = {}

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = (
        "<b>Xoş gəldiniz!</b> 🎵\n\n"
        "Sadəcə mahnı adı göndərin, axtarıb tapacağam!\n"
        "Və ya birbaşa YouTube linki göndərə bilərsiniz."
    )
    bot.send_message(message.chat.id, welcome_text, parse_mode="HTML")

def download_and_send(chat_id, url, message_id):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': '%(id)s.%(ext)s',
        'noplaylist': True,
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            audio_file = filename.rsplit(".", 1)[0] + ".mp3"
            
            with open(audio_file, 'rb') as audio:
                bot.send_audio(chat_id, audio)
            
            try:
                os.remove(audio_file)
            except:
                pass
            bot.delete_message(chat_id, message_id)
    except Exception as e:
        bot.send_message(chat_id, f"❌ Xəta baş verdi: {e}")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    text = message.text.strip()
    chat_id = message.chat.id

    if text.startswith("http://") or text.startswith("https://"):
        msg = bot.send_message(chat_id, "⏳ <b>Mahnı yüklənir, gözləyin...</b>", parse_mode="HTML")
        download_and_send(chat_id, text, msg.message_id)
        return

    bot.send_message(chat_id, f"🔍 <b>{text}</b> axtarılır...", parse_mode="HTML")

    try:
        ydl_opts = {
            'extract_flat': True,
            'max_downloads': 5,
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch5:{text}", download=False)
            entries = info.get('entries', [])

        if not entries:
            bot.send_message(chat_id, "❌ Heç nə tapılmadı.")
            return

        search_results[chat_id] = entries
        markup = InlineKeyboardMarkup()

        result_text = f"🔍 <b>{text}</b> üçün nəticələr:\n\n"
        for i, entry in enumerate(entries, 1):
            title = entry.get('title', 'Naməlum')
            duration = entry.get('duration_string', 'N/A')
            result_text += f"{i}. {title} ({duration})\n"
            markup.add(InlineKeyboardButton(str(i), callback_data=f"dl_{i-1}"))

        bot.send_message(chat_id, result_text, parse_mode="HTML", reply_markup=markup)
    except Exception as e:
        bot.send_message(chat_id, f"❌ Axtarış zamanı xəta: {e}")

@bot.callback_query_handler(func=lambda call: call.data.startswith('dl_'))
def callback_inline(call):
    chat_id = call.message.chat.id
    index = int(call.data.split('_')[1])
    
    if chat_id in search_results and index < len(search_results[chat_id]):
        entry = search_results[chat_id][index]
        url = entry.get('url') or f"https://www.youtube.com/watch?v={entry.get('id')}"
        
        msg = bot.send_message(chat_id, "⏳ <b>Mahnı yüklənir, gözləyin...</b>", parse_mode="HTML")
        bot.answer_callback_query(call.id, "Yükləmə başladı...")
        download_and_send(chat_id, url, msg.message_id)
    else:
        bot.answer_callback_query(call.id, "Məlumat tapılmadı, yenidən axtarış edin.")

bot.infinity_polling()
