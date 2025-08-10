import os
import requests
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes
)

# Konstantalar
ADMIN_ID = 1042437313  # Adminning Telegram user ID si
BOT_TOKEN = '8029676035:AAESll5Mwov9Hn8eUufX_0W3Z_qchmEFOlo'  # Token ni o'zgartiring
API_URL = "https://toocars.tj/api/trackcode"  # API endpoint-i (o'zingizni API manzilingizni kiriting)

# Buttonlar ro'yxatini yaratish
def get_custom_keyboard():
    custom_keyboard = [
        ["Тафтиши трек код"],  # Trek kodni qidirishf
        ["Нархнома::"],       # Narxnomani ko'rsatish
        ["Алока бо администратор"],
        ["Адреси карго!!"],
        ["Молҳои маъншуда!!"]
    ]
    return ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True)

# /start buyrug'i
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Салом! Ман боти ҷустуҷӯи кодҳои трек ҳастам.", reply_markup=get_custom_keyboard())


async def send_address_image(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Statik fayldagi rasm manzili
    image_path = os.path.join(os.getcwd(), "statics", "cargo_address_image.jpg")

    try:
        # Rasmni lokal fayldan jo'natish
        with open(image_path, "rb") as photo:
            await update.message.reply_photo(
    photo=photo,
    caption="🏢 Манзили карго: Zafarobod cargo:\n"
            "```text\n"
            "ZAFAROBOD CARGO\n 15157940200\n 浙江省金华市义乌市\n 福田街道兴港小区 77幢2单元1楼库房 ZAF Номи худатон номер телефон\n"
            "```",
    parse_mode="MarkdownV2"
)
    except Exception as e:
        await update.message.reply_text(f"❌ Рассм жунатишда хато: {str(e)}")

# Trek kod qidirish
async def search_track(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    track_code = update.message.text.strip()

    try:
        # API ga POST so'rov yuborish
        payload = {"trackcode": track_code}
        headers = {"Content-Type": "application/json"}
        response = requests.post(API_URL, json=payload, headers=headers)
        data = response.json()

        if response.status_code == 200 and "message" in data:
            # Agar javob muvaffaqiyatli bo'lsa
            message = data["message"]
            await update.message.reply_text(f"✅ {message}")
        else:
            # Agar kod topilmagan bo'lsa
            await update.message.reply_text(f"🔍 Барои шумо бо код трек: ({track_code}) бор дар анбори мо намеёбад!")
    except Exception as e:
        await update.message.reply_text(f"❌ Хато рух дод: {str(e)}")

# Narxnomani ko'rsatish
async def show_pricing(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    pricing_info = """
Нархномаи мо ⤵️⤵️⤵️
Қабули борҳо аз 0.5кг ҳисоб карда мешавад.
Аз 0.1–0.5 кг → 1.5$
Аз 0.51–1 кг → 3$
1 куб → 300$ ҳисоб карда мешавад
"""
    await update.message.reply_text(pricing_info)

# Tugma bosilganda harakat
async def handle_button_press(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text

    if text == "Тафтиши трек код":
        # Qidiruv rejimiga o'tkazamiz
        context.user_data['search_mode'] = True
        await update.message.reply_text("🔍 Лутфан, код трекро ворид намоед:")
    elif text == "Нархнома::":
        context.user_data['search_mode'] = False
        await show_pricing(update, context)
    elif text == "Алока бо администратор":
        context.user_data['search_mode'] = False
        await update.message.reply_text("📞 Барои тамос: Ватсап +992003304329 ,@Zafarobod_cargo ,@foz1lov_0118 ")
    elif text == "Адреси карго!!":
        context.user_data['search_mode'] = False
        await send_address_image(update,context)
    elif text == "Молҳои маъншуда!!":
        context.user_data['search_mode'] = False
        await update.message.reply_text("""
КАРГОИ МО ИН НАМУДИ БОРХОРО КАБУЛ НАМЕКУНАД!

• Ашёҳои шишагӣ
• Яроқ ва ашёҳои ҳарбӣ
• Маводҳои хатарнок
• Маводҳои наркотикӣ ва психотропӣ
• Ҳайвонот ва растаниҳо
• Маводҳои порнографӣ
• Маҳсулотҳои хӯрока ва тиббӣ
• Пул ва ҳуҷҷатҳои қалбакӣ
""")
    else:
        await search_track(update, context)

# Botni ishga tushirish
if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_button_press))

   print("Polling mode.")
    app.run_polling(
        poll_interval=2.0,
        timeout=30,
        allowed_updates=None,
        drop_pending_updates=True
    )