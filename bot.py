import logging
import os
import re
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

TOKEN = os.getenv("TOKEN")
CHANNEL_USERNAME = "@AmitExploit_bot"
FOOTER = "\n━━━━━━━━━━━━━━━\nPowered by AmitExploits™"

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

# ✅ Force Join Check
async def is_user_joined(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    try:
        member = await context.bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False

# ✅ Start Command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_user_joined(update, context):
        keyboard = [
            [InlineKeyboardButton("🔔 Join Channel", url="https://t.me/AmitExploit_bot")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            "⚠️ Please join our channel to use the bot!",
            reply_markup=reply_markup,
        )
        return

    banner = """
╔════════════════════╗
   🔎 Number Lookup Bot
╚════════════════════╝

Welcome! Choose an option below:
"""

    keyboard = [
        [InlineKeyboardButton("📱 Lookup Number", callback_data="lookup")],
        [InlineKeyboardButton("👨‍💻 Developer", callback_data="developer")],
    ]

    await update.message.reply_text(
        banner + FOOTER,
        reply_markup=InlineKeyboardMarkup(keyboard),
    )

# ✅ Button Handler
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "lookup":
        context.user_data["awaiting_number"] = True
        await query.message.reply_text("📥 Please enter mobile number:")

    elif query.data == "developer":
        await query.message.reply_text(
            "👨‍💻 Developer Contact:\n@AmitShrirao" + FOOTER
        )

# ✅ Handle Number Input
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get("awaiting_number"):
        number = update.message.text.strip()

        if not re.match(r"^\+?\d{10,15}$", number):
            await update.message.reply_text(
                "❌ Invalid or unavailable data!" + FOOTER
            )
            return

        result = f"""
━━━━━━━━━━━━━━━
📱 Number: {number}
🌍 Country: India
📶 Status: Valid Format
━━━━━━━━━━━━━━━
"""
        await update.message.reply_text(result + FOOTER)
        context.user_data["awaiting_number"] = False

# ✅ Main Function
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot Running...")
    app.run_polling()

if _name_ == "_main_":
    main()
