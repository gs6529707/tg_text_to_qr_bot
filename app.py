import qrcode
from io import BytesIO
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import os

# Function to start the bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Hi! Send me any text, and I'll generate a QR code for it.")

# Function to generate QR code from text
async def generate_qr(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_text = update.message.text
    if user_text:
        # Generate the QR code
        qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)
        qr.add_data(user_text)
        qr.make(fit=True)

        # Create an image of the QR code
        qr_img = qr.make_image(fill_color="black", back_color="white")
        qr_io = BytesIO()
        qr_img.save(qr_io, format="PNG")
        qr_io.seek(0)

        # Send the QR code back to the user
        await update.message.reply_photo(photo=qr_io, caption="Here is your QR code!")
        qr_io.close()
    else:
        await update.message.reply_text("Please send some text!")

# Main function to run the bot
def main():
    # Replace 'YOUR_BOT_TOKEN' with your bot token
    TOKEN = os.getenv("token")

    # Create the Application
    app = Application.builder().token(TOKEN).build()

    # Add handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, generate_qr))

    # Start the bot
    app.run_polling()

if __name__ == "__main__":
    main()
