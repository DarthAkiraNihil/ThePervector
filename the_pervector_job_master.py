import subprocess

from telegram import Update
from telegram.ext import Application, ContextTypes, MessageHandler, filters

import logging
from config import config

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


class ThePervectorJobMaster:

    def __init__(self, token, chat_id):
        self.__last_job_id = 0
        self.__token = token
        self.__chat_id = chat_id
        self.__application = Application.builder().token(self.__token).build()

        self.__application.add_handler(MessageHandler(filters.TEXT, self.__spawn_job))

    async def __spawn_job(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

        query = update.message.text.split()
        subprocess.Popen(
            [
                'python',
                'the_pervector_job_executor.py',
                f'{self.__last_job_id}',
                self.__token,
                self.__chat_id,
                query[0],
                query[1],
                query[2]
            ]
        )

        self.__last_job_id += 1

    def launch(self):
        self.__application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    jm = ThePervectorJobMaster(config['TOKEN'], config['CHAT_ID'])
    jm.launch()
