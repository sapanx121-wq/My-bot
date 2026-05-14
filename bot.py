from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)

BOT_TOKEN = "8842288824:AAHD_fMA4uAQQzVOGZslWnT100kfixCSqvA"

# 🔒 Your Telegram User ID
ADMIN_ID = 7013235694

# 📂 File Storage
FILES = {}

# 🧠 Upload States
waiting_name = {}
waiting_file = {}

# ✅ Admin Check
def is_admin(user_id):
    return user_id == ADMIN_ID

# 🚀 /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not is_admin(update.effective_user.id):

        await update.message.reply_text(
            "🔒 Private Bot\n⛔ Access Denied"
        )
        return

    if not FILES:

        await update.message.reply_text(
            "📂 No Files Uploaded Yet 😅"
        )
        return

    keyboard = []

    for name in FILES:

        keyboard.append(
            [
                InlineKeyboardButton(
                    f"🚀 {name}",
                    callback_data=name
                )
            ]
        )

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "🔥 Welcome To File Store Bot 🔥\n\n📥 Select Your File Below 👇",
        reply_markup=reply_markup
    )

# 📤 /upload
async def upload(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not is_admin(update.effective_user.id):

        await update.message.reply_text(
            "🔒 Private Bot\n⛔ Access Denied"
        )
        return

    user_id = update.effective_user.id

    waiting_name[user_id] = True

    await update.message.reply_text(
        "📝 Send File Name"
    )

# 📝 Receive File Name
async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    if user_id in waiting_name:

        context.user_data["file_name"] = update.message.text

        waiting_name.pop(user_id)

        waiting_file[user_id] = True

        await update.message.reply_text(
            "📤 Now Upload Your File"
        )

# 📁 Receive File
async def file_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    if not is_admin(user_id):

        await update.message.reply_text(
            "🔒 Private Bot"
        )
        return

    if user_id in waiting_file:

        file_name = context.user_data["file_name"]

        file_id = update.message.document.file_id

        # 🔄 Replace old file automatically
        FILES[file_name] = file_id

        waiting_file.pop(user_id)

        await update.message.reply_text(
            f"✅ File Uploaded Successfully\n\n📁 {file_name}"
        )

# ⬇️ Button Click
async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()

    file_id = FILES.get(query.data)

    if file_id:

        await context.bot.send_document(
            chat_id=query.message.chat_id,
            document=file_id,
            caption="🔥 Here Is Your File 🚀"
        )

# 🗑 /delete
async def delete(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not is_admin(update.effective_user.id):

        await update.message.reply_text(
            "🔒 Private Bot"
        )
        return

    msg = update.message.text.split(" ", 1)

    if len(msg) < 2:

        await update.message.reply_text(
            "⚠️ Usage:\n/delete file_name"
        )
        return

    file_name = msg[1]

    if file_name in FILES:

        del FILES[file_name]

        await update.message.reply_text(
            f"🗑 File Deleted Successfully\n\n❌ {file_name}"
        )

    else:

        await update.message.reply_text(
            "❌ File Not Found"
        )

# 🤖 App
app = Application.builder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("upload", upload))
app.add_handler(CommandHandler("delete", delete))

app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        text_handler
    )
)

app.add_handler(
    MessageHandler(
        filters.Document.ALL,
        file_handler
    )
)

app.add_handler(
    CallbackQueryHandler(button_click)
)

print("🔥 Bot Running Successfully...")
app.run_polling()