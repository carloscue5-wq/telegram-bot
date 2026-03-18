import os
import random
import asyncio
import json
from datetime import datetime, timedelta

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    MessageHandler,
    CallbackQueryHandler,
    CommandHandler,
    filters,
)

TOKEN = os.getenv("TELEGRAM_TOKEN")

PAUSA_HORAS = 3

ARTISTAS = [
"Jimi Hendrix",
"Guns N Roses",
"Metallica",
"MEUTE",
"ZHU",
"INXS",
"Teddy Swims",
"Gorillaz",
"Simple Minds",
"RÜFÜS DU SOL",
"Unknown Artist",
"MONOLINK",
"MOBY",
"SENDA"
]

USUARIOS_FILE = "usuarios.txt"
MENSAJES_FILE = "mensajes.txt"
ESTADO_FILE = "estado_chat.json"

ultima_cancion = None


def cargar_estado():
    if not os.path.exists(ESTADO_FILE):
        return {}
    with open(ESTADO_FILE) as f:
        return json.load(f)


def guardar_estado(data):
    with open(ESTADO_FILE,"w") as f:
        json.dump(data,f)


def bot_puede_responder(user_id):

    estado = cargar_estado()

    if str(user_id) not in estado:
        return True

    ultima = datetime.fromisoformat(estado[str(user_id)])

    if datetime.now() - ultima > timedelta(hours=PAUSA_HORAS):
        return True

    return False


def registrar_respuesta_humana(user_id):

    estado = cargar_estado()

    estado[str(user_id)] = datetime.now().isoformat()

    guardar_estado(estado)


def guardar_usuario(user):

    linea = f"{user.id} | {user.first_name} | @{user.username}\n"

    if not os.path.exists(USUARIOS_FILE):
        open(USUARIOS_FILE,"w").close()

    with open(USUARIOS_FILE,"r") as f:
        usuarios = f.read()

    if str(user.id) not in usuarios:

        with open(USUARIOS_FILE,"a") as f:
            f.write(linea)


def guardar_mensaje(user,contenido):

    fecha = datetime.now().strftime("%Y-%m-%d %H:%M")

    linea = f"{fecha} | {user.first_name} | {contenido}\n"

    with open(MENSAJES_FILE,"a") as f:
        f.write(linea)


def obtener_musica():

    global ultima_cancion

    opciones = [a for a in ARTISTAS if a != ultima_cancion]

    artista = random.choice(opciones)

    ultima_cancion = artista

    return artista


def crear_menu(artista):

    query = artista.replace(" ","%20")

    botones = [

    [InlineKeyboardButton("🎧 Spotify",url=f"https://open.spotify.com/search/{query}")],
    [InlineKeyboardButton("🎶 YouTube Music",url=f"https://music.youtube.com/search?q={query}")],
    [InlineKeyboardButton("🍎 Apple Music",url=f"https://music.apple.com/search?term={query}")],

    [InlineKeyboardButton("🤖 Hablar con ChatGPT",url="https://chat.openai.com")],

    [InlineKeyboardButton("💼 Sobre Charly",callback_data="sobre")],
    [InlineKeyboardButton("📩 Dejar mensaje",callback_data="mensaje")],
    [InlineKeyboardButton("📊 Estadísticas",callback_data="stats")]

    ]

    return InlineKeyboardMarkup(botones)


async def responder(update:Update,context:ContextTypes.DEFAULT_TYPE):

    user = update.effective_user

    guardar_usuario(user)

    contenido = "mensaje"

    if update.message.text:
        contenido = update.message.text

    guardar_mensaje(user,contenido)

    if not bot_puede_responder(user.id):
        return

    artista = obtener_musica()

    mensaje = (

    f"Hola {user.first_name} 👋\n\n"
    "Charly no está disponible ahora.\n"
    "Pero puedes hacer varias cosas:\n\n"
    "🎧 escuchar música\n"
    "🤖 hablar con ChatGPT\n"
    "📩 dejar un mensaje\n\n"
    f"🎵 Recomendación:\n{artista}"

    )

    await update.message.reply_text(
    mensaje,
    reply_markup=crear_menu(artista)
    )


async def botones(update:Update,context:ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    if query.data == "sobre":

        texto = (
        "💼 Sobre Charly\n\n"
        "Profesional en tecnología, estrategia digital "
        "y desarrollo de soluciones."
        )

        await query.message.reply_text(texto)

    if query.data == "mensaje":

        await query.message.reply_text(
        "Escribe tu mensaje y Charly lo verá cuando esté disponible."
        )

    if query.data == "stats":

        usuarios = 0
        mensajes = 0

        if os.path.exists(USUARIOS_FILE):
            with open(USUARIOS_FILE) as f:
                usuarios = len(f.readlines())

        if os.path.exists(MENSAJES_FILE):
            with open(MENSAJES_FILE) as f:
                mensajes = len(f.readlines())

        texto = (

        f"📊 Estadísticas\n\n"
        f"👥 Usuarios: {usuarios}\n"
        f"💬 Mensajes: {mensajes}"

        )

        await query.message.reply_text(texto)


async def humano(update:Update,context:ContextTypes.DEFAULT_TYPE):

    if update.message.reply_to_message:

        user_id = update.message.reply_to_message.from_user.id

        registrar_respuesta_humana(user_id)

        await update.message.reply_text(
        "🤖 Bot pausado por 3 horas para este usuario"
        )


async def main():

    print("🤖 Bot activo")

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(MessageHandler(filters.ALL,responder))

    app.add_handler(CallbackQueryHandler(botones))

    app.add_handler(CommandHandler("humano",humano))

    await app.initialize()
    await app.start()
    await app.updater.start_polling()

    while True:
        await asyncio.sleep(3600)


if __name__ == "__main__":
    asyncio.run(main())
