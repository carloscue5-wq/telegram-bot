import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    MessageHandler,
    CallbackQueryHandler,
    filters,
)

# 🔐 TU TOKEN REAL AQUÍ
TOKEN = "8483595648:AAEaffJHFSlwlFuenv_Z3LOuaM3OvC4a1Uw"

# 🎵 LISTA DE RECOMENDACIONES (PUEDES AGREGAR MÁS)
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
    "pero mientras puedes escuchar música en lo que respondo 🎶\n\n"
)

# 🔗 GENERAR LINKS POR PLATAFORMA
def generar_botones(cancion):
    query = cancion.replace(" ", "%20")

    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🎧 Spotify", url=f"https://open.spotify.com/search/{query}")],
        [InlineKeyboardButton("🎶 YouTube Music", url=f"https://music.youtube.com/search?q={query}")],
        [InlineKeyboardButton("🍎 Apple Music", url=f"https://music.apple.com/search?term={query}")],
        [InlineKeyboardButton("🟦 Amazon Music", url=f"https://music.amazon.com/search/{query}")],
        [InlineKeyboardButton("⏳ Prefiero esperar", callback_data="esperar")]
    ])

# 📥 RESPONDER A CUALQUIER MENSAJE
async def responder_todo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cancion = random.choice(CANCIONES)

    mensaje = (
        MENSAJE_BASE +
        f"🎧 *Recomendación para ti:*\n"
        f"🎵 {cancion}"
    )

    await update.message.reply_text(
        mensaje,
        reply_markup=generar_botones(cancion),
        parse_mode="Markdown"
    )

# 🖱️ BOTÓN ESPERAR
async def botones(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "esperar":
        await query.message.reply_text(
            "Perfecto 😊\n"
            "Cuando esté disponible te respondo. Gracias por tu paciencia 🙌"
        )

# 🚀 MAIN
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(MessageHandler(filters.ALL, responder_todo))
    app.add_handler(CallbackQueryHandler(botones))

    print("🤖 Bot activo...")
    app.run_polling()

if __name__ == "__main__":
    main()
