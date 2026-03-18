import os
import random
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    MessageHandler,
    CallbackQueryHandler,
    filters,
)

# 🔐 TOKEN desde variables de entorno (Render)
TOKEN = os.getenv("TELEGRAM_TOKEN")
print("TOKEN:", TOKEN)

# 🎵 LISTA DE CANCIONES
CANCIONES = [
    "Daft Punk - Get Lucky",
    "Coldplay - Viva La Vida",
    "The Weeknd - Blinding Lights",
    "Bad Bunny - Monaco",
    "Taylor Swift - Anti-Hero",
    "Karol G - Provenza",
    "Imagine Dragons - Believer",
]

# 📨 MENSAJE BASE
MENSAJE_BASE = (
    "No estoy disponible por el momento 😅\n"
    "pero mientras puedes escuchar música en lo que respondo 🎶"
)

# 🔗 GENERAR BOTONES
def generar_botones(cancion):
    query = cancion.replace(" ", "%20")

    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🎧 Spotify", url=f"https://open.spotify.com/search/{query}")],
        [InlineKeyboardButton("🎶 YouTube Music", url=f"https://music.youtube.com/search?q={query}")],
        [InlineKeyboardButton("🍎 Apple Music", url=f"https://music.apple.com/search?term={query}")],
        [InlineKeyboardButton("🟦 Amazon Music", url=f"https://music.amazon.com/search/{query}")],
        [InlineKeyboardButton("⏳ Prefiero esperar", callback_data="esperar")]
    ])

# 📥 RESPONDER A TODO
async def responder_todo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return

    cancion = random.choice(CANCIONES)

    mensaje = (
        f"{MENSAJE_BASE}\n\n"
        f"🎧 Recomendación para ti:\n"
        f"🎵 {cancion}"
    )

    await update.message.reply_text(
        mensaje,
        reply_markup=generar_botones(cancion)
    )

# 🖱️ BOTÓN "ESPERAR"
async def botones(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "esperar":
        await query.message.reply_text(
            "Perfecto 😊\n"
            "Cuando esté disponible te respondo. Gracias por tu paciencia 🙌"
        )

# 🚀 FUNCIÓN PRINCIPAL
async def main():

    print("🤖 Bot activo...")

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(MessageHandler(filters.ALL, responder_todo))
    app.add_handler(CallbackQueryHandler(botones))

    print("Bot iniciado correctamente")

    await app.initialize()
    await app.start()
    await app.updater.start_polling()

    # Mantener el bot vivo
    while True:
        await asyncio.sleep(3600)


if __name__ == "__main__":
    asyncio.run(main())
