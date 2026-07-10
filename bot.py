from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import pandas as pd
import os

TOKEN = os.getenv("BOT_TOKEN")

df = None

if os.path.exists("products.xlsx"):
    df = pd.read_excel("products.xlsx")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 أهلاً بيك في O.M. BIM\n\nابعت اسم المنتج وأنا هجيب الكود."
    )


async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global df

    if df is None:
        await update.message.reply_text("❌ ملف المنتجات غير موجود.")
        return

    text = update.message.text.strip()

    result = df[df.iloc[:,1].astype(str).str.contains(text, case=False, na=False)]

    if result.empty:
        await update.message.reply_text("❌ المنتج غير موجود.")
        return

    row = result.iloc[0]

    await update.message.reply_text(
        f"📦 {row.iloc[1]}\n"
        f"🆔 الكود: {row.iloc[0]}"
    )


app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search))

app.run_polling()
