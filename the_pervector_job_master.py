from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

import logging

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


class ThePervectorJobMaster:

    def __init__(self):
        """Start the bot."""
        # Create the Application and pass it your bot's token.
        self.__application = Application.builder().token("").build()

        # on different commands - answer in Telegram
        self.__application.add_handler(CommandHandler("start", self.__start))
        self.__application.add_handler(CommandHandler("help", self.__help_command))

        # on non command i.e message - echo the message on Telegram
        self.__application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.__echo))

        # Run the bot until the user presses Ctrl-C


    async def __start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Send a message when the command /start is issued."""
        user = update.effective_user
        await update.message.reply_html(
            rf"Hi {user.mention_html()}!",
            reply_markup=ForceReply(selective=True),
        )


    async def __help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Send a message when the command /help is issued."""
        await update.message.reply_text("Help!")


    async def __echo(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Echo the user message."""
        await update.message.reply_text(update.message.text)

    def launch(self):
        self.__application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    jm = ThePervectorJobMaster()
    jm.launch()
