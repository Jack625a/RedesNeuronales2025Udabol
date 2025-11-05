#token de Telegram:
#apiGoogleCloud: 
#nombreModelo: gemini-2.5-flash-lite-preview-09-2025

#PASO 1. importar las librerias
import google.generativeai as genai
from telegram.ext import ApplicationBuilder,CommandHandler, MessageHandler, filters, ContextTypes
from telegram import Update


#PASO 2. CONFIGURAR LOS TOKENS
apiGoogleCloud=""
tokenTelegram=""

#PASO 3. CONFIGURAR EL MODELO
genai.configure(api_key=apiGoogleCloud)
modelo=genai.GenerativeModel("gemini-2.5-flash-lite-preview-09-2025")

#PASO4. CONFIGURAR LOS COMANDOS /start
async def start(update:Update,context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hola bienvenido... cual es tu consulta")

#PASO 5. CONFIGURAR LAS RESPUESTAS
async def responder(update:Update,context:ContextTypes.DEFAULT_TYPE):
    mensajeUsuario=update.message.text
    
    #await update.message.chat_action="Escribiendo..."

    try:
        respuesta=modelo.generate_content(mensajeUsuario)
        texto=respuesta.text.strip() if respuesta.text else "No se entendio la pregunta"
    except Exception as error:
        texto=f"Error al conectar con el servidor {error}"
    
    await update.message.reply_text(texto)

#PASO 6. CONFIGURACION DEL BOT
def bot():
    app=ApplicationBuilder.builder().token(tokenTelegram).build() 
    app.add_handler(CommandHandler("start",start)) 
    app.add_handler(MessageHandler(filters.text & ~filters.COMMAND, responder))
    print("Bot esta activo")
    app.run_polling()

#PASO 7. INICIAR EL BOT
if __name__=="__main__":
    bot()