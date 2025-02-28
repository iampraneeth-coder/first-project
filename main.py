import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Get the Telegram Bot token from the environment variable
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    logging.error("TELEGRAM_BOT_TOKEN environment variable not set!")
    exit(1)

# --- Command Handlers ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles the /start command."""
    user = update.effective_user
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                text=f"Hello {user.first_name}! I'm your bot.  Use /help to see available commands.")
    logging.info(f"User {user.username} started the bot.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles the /help command."""
    help_text = """
I am a versatile Telegram bot! Here are the commands I understand:

/start - Starts the bot and greets you.
/help - Displays this help message.
/caps <text> - Converts the given text to uppercase.
/echo <text> - Repeats the given text back to you.
/about - Provides information about the bot.
<any text> - Responds with a general reply.
"""
    await context.bot.send_message(chat_id=update.effective_chat.id, text=help_text)


async def caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles the /caps command."""
    try:
        text_caps = ' '.join(context.args).upper()
        await context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)
        logging.info(f"User {update.effective_user.username} used /caps: {text_caps}")
    except IndexError:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                    text="Please provide some text after /caps.")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles the /echo command."""
    try:
        text = ' '.join(context.args)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
        logging.info(f"User {update.effective_user.username} used /echo: {text}")
    except IndexError:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                        text="Please provide some text after /echo.")

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles the /about command."""
    about_text = "This is a simple Telegram bot created as an example."
    await context.bot.send_message(chat_id=update.effective_chat.id, text=about_text)

# --- Message Handler (for general text) ---

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles general text messages."""
    user_message = update.message.text
    response = f"You said: {user_message}. I'm just a simple bot, so that's all I can do right now."
    await context.bot.send_message(chat_id=update.effective_chat.id, text=response)
    logging.info(f"User {update.effective_user.username} sent a message: {user_message}")

# --- Error Handler ---

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles errors."""
    logging.error(f"Update {update} caused error {context.error}")
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                text="Oops! Something went wrong.  Check the server logs for details.")


# --- Main Function ---

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()

    # Command Handlers
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('help', help_command))
    application.add_handler(CommandHandler('caps', caps))
    application.add_handler(CommandHandler('echo', echo))
    application.add_handler(CommandHandler('about', about))

    # Message Handler (Must be added after command handlers)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Error Handler
    application.add_error_handler(error_handler)

    # Start the Bot
    logging.info("Bot started. Polling for updates...")
    application.run_polling()
