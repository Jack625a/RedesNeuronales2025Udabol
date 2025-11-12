#token de Telegram:8294447544:AAHZ4iEPujsOAWsu1Pf60HoUWv25s94eoBs
#apiGoogleCloud: AIzaSyDK2ZT1TnCyjX3TbxrrcJIR08S7GuDnc5I
#nombreModelo: gemini-2.5-flash-lite-preview-09-2025
#cuentaServicio: redesneuronales@redesneuronalesudabol2025.iam.gserviceaccount.com 


# PASO 1. IMPORTAR LIBRERÍAS
import google.generativeai as genai
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from telegram import Update
import gspread
from google.oauth2.service_account import Credentials



#PASO 2. CONFIGURAR LOS TOKENS
apiGoogleCloud=""
tokenTelegram=""

# PASO 3. CONFIGURAR EL MODELO
genai.configure(api_key=apiGoogleCloud)
modelo = genai.GenerativeModel("gemini-2.5-flash-lite-preview-09-2025")


#PASO 1.1.Conexion a la hoja de calculo
def hojaCalculoData():
    try: 
        #Definir el alcance
        alcances=["https://www.googleapis.com/auth/spreadsheets.readonly"]
        credenciales=Credentials.from_service_account_file("cuentaServicio.json",scopes=alcances)

        #Autentificacion
        cliente=gspread.authorize(credenciales)
        hoja=cliente.open_by_url("https://docs.google.com/spreadsheets/d/1CqeTyMQ1QhVE3eLpxBzCmMJq9Rk-Rddeo31bKIVcMHQ")
        hojaDatos=hoja.sheet1

        #Obtener los datos de la hoja de calculo
        datos=hojaDatos.get_all_records()
        return datos
    except Exception as error:
        print(f"Error al cargar los datos de la hoja de calculo... {error}")
        return []

entrenamiento=hojaCalculoData()

# PASO 4. COMANDO /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Bienvenido a Udabol Cual es tu consulta \n\nEscríbeme tu consulta y te ayudaré enseguida 😊")

# PASO 5. RESPUESTA A MENSAJES
async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mensaje_usuario = update.message.text

    # Enviar mensaje de "escribiendo..."
    await update.message.chat.send_action(action="typing")

    try:
        contexto="En base a este entrenamiento en fomato tabla para adeuarte a las respuesta que daras"
        for fila in entrenamiento:
            contexto+=str(fila)+"\n"
        ordenFinal=f"""Eres un vendedor de la empresa Udabol tu nombre es Edit 
        deberas responder de forma cordial basandote en la informacion de esta base de datos: 
        {contexto} 

        restricciones: No responder mensajes que no sean relacionados  a la empresa
        precio es en Bs
        Usuario:{mensaje_usuario}
        """

        respuesta = modelo.generate_content(ordenFinal)
        texto = respuesta.text.strip() if hasattr(respuesta, "text") and respuesta.text else "No se entendió la pregunta 🤔"
    except Exception as error:
        texto = f"⚠️ Error al conectar con el servidor:\n{error}"

    await update.message.reply_text(texto)

# PASO 6. CONFIGURACIÓN DEL BOT
def main():
    app = ApplicationBuilder().token(tokenTelegram).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder))

    print(" Bot activo...")
    app.run_polling()

# PASO 7. EJECUTAR EL BOT
if __name__ == "__main__":
    main()
