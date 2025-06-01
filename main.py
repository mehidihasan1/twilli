from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from user_data_store import set_user_twilio, get_user_twilio
import twilio_utils
import os

TELEGRAM_BOT_TOKEN = os.getenv("BOT_TOKEN") or "7676974479:AAEERPH7cYOjTWms3votUOnjZAGunVyXJAY"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome to the Twilio Number Manager Bot!\nUse /set_twilio <SID> <TOKEN> to begin.")

async def set_twilio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if len(args) != 2:
        await update.message.reply_text("Usage:\n/set_twilio <TWILIO_ACCOUNT_SID> <TWILIO_AUTH_TOKEN>")
        return
    set_user_twilio(update.effective_user.id, args[0], args[1])
    await update.message.reply_text("✅ Twilio credentials saved!")

async def search_number(update: Update, context: ContextTypes.DEFAULT_TYPE):
    creds = get_user_twilio(update.effective_user.id)
    if not creds:
        await update.message.reply_text("❌ Please set your Twilio credentials using /set_twilio first.")
        return
    if len(context.args) < 2:
        await update.message.reply_text("Usage:\n/search_number <country_code> <type> [contains]")
        return
    country, type = context.args[0], context.args[1]
    contains = context.args[2] if len(context.args) > 2 else None
    try:
        client = twilio_utils.create_client(creds['sid'], creds['token'])
        numbers = twilio_utils.search_numbers(client, country, type, contains)
        if not numbers:
            await update.message.reply_text("❌ No numbers found.")
            return
        msg = "\n".join([f"{n.phone_number} ({n.friendly_name})" for n in numbers])
        await update.message.reply_text(f"📞 Available Numbers:\n{msg}")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")

async def buy_number(update: Update, context: ContextTypes.DEFAULT_TYPE):
    creds = get_user_twilio(update.effective_user.id)
    if not creds:
        await update.message.reply_text("❌ Please set your Twilio credentials using /set_twilio first.")
        return
    if not context.args:
        await update.message.reply_text("Usage:\n/buy_number <phone_number>")
        return
    number = context.args[0]
    try:
        client = twilio_utils.create_client(creds['sid'], creds['token'])
        purchased = twilio_utils.buy_number(client, number)
        await update.message.reply_text(f"✅ Number purchased: {purchased.phone_number}")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")

async def release_number(update: Update, context: ContextTypes.DEFAULT_TYPE):
    creds = get_user_twilio(update.effective_user.id)
    if not creds:
        await update.message.reply_text("❌ Please set your Twilio credentials using /set_twilio first.")
        return
    if not context.args:
        await update.message.reply_text("Usage:\n/release_number <number_sid>")
        return
    sid = context.args[0]
    try:
        client = twilio_utils.create_client(creds['sid'], creds['token'])
        twilio_utils.release_number(client, sid)
        await update.message.reply_text("✅ Number released.")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")

async def list_numbers(update: Update, context: ContextTypes.DEFAULT_TYPE):
    creds = get_user_twilio(update.effective_user.id)
    if not creds:
        await update.message.reply_text("❌ Please set your Twilio credentials using /set_twilio first.")
        return
    try:
        client = twilio_utils.create_client(creds['sid'], creds['token'])
        numbers = twilio_utils.list_numbers(client)
        if not numbers:
            await update.message.reply_text("📭 No active Twilio numbers.")
            return
        msg = "\n".join([f"{n.phone_number} - SID: {n.sid}" for n in numbers])
        await update.message.reply_text(f"📱 Your Twilio Numbers:\n{msg}")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")

async def check_sms(update: Update, context: ContextTypes.DEFAULT_TYPE):
    creds = get_user_twilio(update.effective_user.id)
    if not creds:
        await update.message.reply_text("❌ Please set your Twilio credentials using /set_twilio first.")
        return
    if not context.args:
        await update.message.reply_text("Usage:\n/check_sms <your_twilio_number>")
        return
    to_number = context.args[0]
    try:
        client = twilio_utils.create_client(creds['sid'], creds['token'])
        messages = twilio_utils.get_sms_messages(client, to_number)
        if not messages:
            await update.message.reply_text("📭 No SMS received.")
            return
        msg = "\n".join([f"{m.from_}: {m.body}" for m in messages])
        await update.message.reply_text(f"📨 Recent SMS:\n{msg}")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")

def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("set_twilio", set_twilio))
    app.add_handler(CommandHandler("search_number", search_number))
    app.add_handler(CommandHandler("buy_number", buy_number))
    app.add_handler(CommandHandler("release_number", release_number))
    app.add_handler(CommandHandler("list_numbers", list_numbers))
    app.add_handler(CommandHandler("check_sms", check_sms))
    print("✅ Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
