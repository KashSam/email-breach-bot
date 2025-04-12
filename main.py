import telebot
import requests
import time
import random
import os
bot = telebot.TeleBot(os.getenv("BOT_TOKEN"))

loading_bar = [
    "[■□□□□□□□□□] 10%",
    "[■■□□□□□□□□] 20%",
    "[■■■□□□□□□□] 30%",
    "[■■■■□□□□□□] 40%",
    "[■■■■■□□□□□] 50%",
    "[■■■■■■□□□□] 60%",
    "[■■■■■■■□□□] 70%",
    "[■■■■■■■■□□] 80%",
    "[■■■■■■■■■□] 90%",
    "[■■■■■■■■■■] 100%"
]

connecting_steps = [
    "`Connecting to secure server...`",
    "`Injecting email fingerprint...`",
    "`Launching vulnerability scan...`",
    "`Bypassing firewall...`",
    "`Decrypting data packets...`",
    "`Access granted!`"
]

@bot.message_handler(commands=['start'])
def welcome(msg):
    bot.send_message(msg.chat.id,
        "╔═════════════════════════╗\n"
        "   ⚠️ *Email Breach Scanner* ⚠️\n"
        "╚═════════════════════════╝\n\n"
        "Send any email address to begin scanning.\n"
        "_Use for educational purposes only._\n\n"
        "🔐 *Developed by CrackA*", parse_mode="Markdown")

@bot.message_handler(func=lambda m: '@' in m.text)
def scan_email(message):
    email = message.text.strip()
    chat_id = message.chat.id

    # Connecting animation
    con_msg = bot.send_message(chat_id, "⏳ Starting scan...", parse_mode="Markdown")
    for step in connecting_steps:
        bot.edit_message_text(f"⚡ {step}", chat_id, con_msg.message_id)
        time.sleep(0.7)

    # Loading bar animation
    load_msg = bot.send_message(chat_id, "`[□□□□□□□□□□] 0%`", parse_mode="Markdown")
    for frame in loading_bar:
        bot.edit_message_text(f"`{frame}`", chat_id, load_msg.message_id)
        time.sleep(0.3)
    bot.delete_message(chat_id, load_msg.message_id)

    # Scanning message
    bot.send_message(chat_id, f"🔍 *Scanning email:* `{email}`", parse_mode="Markdown")

    # LeakCheck API call
    api = f"https://leakcheck.io/api/public?check={email}"
    try:
        r = requests.get(api)
        data = r.json()

        if data.get("found", 0) > 0:
            msg = (
                f"╭───[ ⚠️ Breach Report ]───╮\n"
                f"📧 Email: `{email}`\n"
                f"📂 Found in: *{data['found']}* breaches\n"
                f"🧾 Sources:\n"
            )
            for src in data.get("sources", []):
                msg += f"  └─ `{src}`\n"
            msg += "\n⚠️ _Your data has been leaked!_\nPlease change your passwords immediately.\n"
        else:
            msg = (
                f"╭───[ ✅ Result Safe ]───╮\n"
                f"📧 Email: `{email}`\n"
                f"🔒 No breaches found!\n"
            )
    except Exception as e:
        msg = f"❌ *Error during scan:*\n`{str(e)}`"

    msg += "\n\n🔐 *Developed by CrackA*"

    # Send result
    bot.send_message(chat_id, msg, parse_mode="Markdown")

    # Add Facebook button (replace your FB link)
    markup = telebot.types.InlineKeyboardMarkup()
    fb_button = telebot.types.InlineKeyboardButton("🌐 Facebook Profile", url="https://www.facebook.com/cracka56")
    markup.add(fb_button)
    bot.send_message(chat_id, "🔗 Connect with developer:", reply_markup=markup)

bot.polling()
