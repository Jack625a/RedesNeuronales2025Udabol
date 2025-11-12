#Importacion de las librerias
import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters,ContextTypes
import requests
from io import BytesIO

#Configuracion de telegram
#PASO 2. CONFIGURAR LOS TOKENS
apiGoogleCloud=""
tokenTelegram=""

# PASO 3. CONFIGURAR EL MODELO
genai.configure(api_key=apiGoogleCloud)
modelo = genai.GenerativeModel("gemini-2.5-flash-lite-preview-09-2025")

# PASO 4. COMANDO /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Bienvenido a Udabol Cual es tu consulta \n\nEscríbeme tu consulta y te ayudaré enseguida 😊")

#PASO 4. CONFIGURAR EL ANALISIS DE IMAGENES
async def procesarImagen(update:Update, context:ContextTypes.DEFAULT_TYPE):
    try:
        foto=update.message.photo[-1]
        archivo= await foto.get_file()
        archivoBinario=BytesIO()
        await archivo.download_to_memory(out=archivoBinario)
        #seek
        archivoBinario.seek(0)
        update.message.reply_text("Analisando la imagen...")

        #respuesta
        respuesta=modelo.generate_content([
            "Obten el nombre, nit y el monto total que aparece en la imagen",
            {
                "mime_type":"image/jpeg","data":archivoBinario.getvalue()
            }
        ])
        #Envio de la respuesta en formato texto
        texto=respuesta.text.strip()
        await update.message.reply_text(f"Resultado: \n {texto}") 
    except Exception as error:
        await update.message.reply_text("Error al procesar la imagen...")

def main():
    app=ApplicationBuilder().token(tokenTelegram).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, procesarImagen))
    print("Bot activo...")
    app.run_polling()

if __name__=="__main__":
    main()

