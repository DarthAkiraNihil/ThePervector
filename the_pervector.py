from kemono_downloader import KemonoDownloader
from config import config

import utils
import shutil
import os


class ThePervector:

    def __init__(self, job_id: int, update_bot_token: str, chat_id: str):
        self.__id = job_id
        self.__token = update_bot_token
        self.__chat_id = chat_id
        self.__status_message_id = 0

    def download_and_send(self, provider: str, service: str, creator_id: int):

        self.__status_message_id = utils.send_telegram_message(
            self.__token,
            self.__chat_id,
            f'Created job_id_{self.__id}.\ncreator_id: {creator_id}, from: {provider}/{service}\n'
            f'Status: initializing'
        )

        kd = KemonoDownloader(provider, service, creator_id, {
            'update_message': self.__status_message_id,
            'token': self.__token,
            'chat_id': self.__chat_id,
            'job_id': self.__id,
            'creator_id': creator_id,
            'provider': provider,
            'service': service
        })

        for i in range(kd.get_post_count()):

            utils.edit_telegram_message(
                self.__token,
                self.__chat_id,
                self.__status_message_id,
                f"Running job_id_{self.__id}.\n"
                f"creator_id: {creator_id},"
                f"from: {provider}/{service}\n"
                "Status: downloading\n"
                f'Post {i+1}/{kd.get_post_count()}\n'
                'Status: getting files'
            )

            def clean_cache(cleaned: str, with_split: bool):
                shutil.rmtree(cleaned)
                os.remove(f'{cleaned}.zip')
                if with_split:
                    shutil.rmtree(f'{cleaned}_split')
                    os.remove(f'{cleaned}_split.mergefile')

            path = kd.download(i)

            if path != 'skipped':
                utils.edit_telegram_message(
                    self.__token,
                    self.__chat_id,
                    self.__status_message_id,
                    f"Running job_id_{self.__id}.\n"
                    f"creator_id: {creator_id},"
                    f"from: {provider}/{service}\n"
                    "Status: downloading\n"
                    f'Post {i+1}/{kd.get_post_count()}\n'
                    'Status: packing'
                )

                utils.pack(path)

                utils.edit_telegram_message(
                    self.__token,
                    self.__chat_id,
                    self.__status_message_id,
                    f"Running job_id_{self.__id}.\n\n"
                    f"creator_id: {creator_id},"
                    f"from: {provider}/{service}\n"
                    "Status: downloading\n"
                    f'Post {i+1}/{kd.get_post_count()}\n'
                    'Status: packed'
                )

                if os.path.getsize(path + ".zip") > config['CHUNK_SIZE']:
                    utils.edit_telegram_message(
                        self.__token,
                        self.__chat_id,
                        self.__status_message_id,
                        f"Running job_id_{self.__id}.\n"
                        f"creator_id: {creator_id},"
                        f"from: {provider}/{service}\n"
                        "Status: downloading\n"
                        f'Post {i+1}/{kd.get_post_count()}\n'
                        'Status: splitting'
                    )
                    utils.split(path, "zip", config['CHUNK_SIZE'])
                    utils.edit_telegram_message(
                        self.__token,
                        self.__chat_id,
                        self.__status_message_id,
                        f"Running job_id_{self.__id}.\n"
                        f"creator_id: {creator_id},"
                        f"from: {provider}/{service}\n"
                        "Status: downloading\n"
                        f'Post {i+1}/{kd.get_post_count()}\n'
                        'Status: split'
                    )
                    utils.edit_telegram_message(
                        self.__token,
                        self.__chat_id,
                        self.__status_message_id,
                        f"Running job_id_{self.__id}.\n"
                        f"creator_id: {creator_id},"
                        f"from: {provider}/{service}\n"
                        "Status: downloading\n"
                        f'Post {i+1}/{kd.get_post_count()}\n'
                        'Status: sending'
                    )
                    utils.dump_to_telegram(
                        self.__token,
                        self.__chat_id,
                        path + "_split",
                        True
                    )
                    utils.edit_telegram_message(
                        self.__token,
                        self.__chat_id,
                        self.__status_message_id,
                        f"Running job_id_{self.__id}.\n"
                        f"creator_id: {creator_id},"
                        f"from: {provider}/{service}\n"
                        "Status: downloading\n"
                        f'Post {i+1}/{kd.get_post_count()}\n'
                        'Status: sent'
                    )
                    utils.edit_telegram_message(
                        self.__token,
                        self.__chat_id,
                        self.__status_message_id,
                        f"Running job_id_{self.__id}.\n"
                        f"creator_id: {creator_id},"
                        f"from: {provider}/{service}\n"
                        "Status: downloading\n"
                        f'Post {i+1}/{kd.get_post_count()}\n'
                        'Status: cleaning cache'
                    )
                    clean_cache(path, True)
                else:
                    utils.edit_telegram_message(
                        self.__token,
                        self.__chat_id,
                        self.__status_message_id,
                        f"Running job_id_{self.__id}.\n"
                        f"creator_id: {creator_id},"
                        f"from: {provider}/{service}\n"
                        "Status: downloading\n"
                        f'Post {i+1}/{kd.get_post_count()}\n'
                        'Status: sending'
                    )
                    utils.dump_to_telegram(
                        self.__token,
                        self.__chat_id,
                        path + ".zip",
                        False
                    )
                    utils.edit_telegram_message(
                        self.__token,
                        self.__chat_id,
                        self.__status_message_id,
                        f"Running job_id_{self.__id}.\n"
                        f"creator_id: {creator_id},"
                        f"from: {provider}/{service}\n"
                        "Status: downloading\n"
                        f'Post {i+1}/{kd.get_post_count()}\n'
                        'Status: sent'
                    )
                    utils.edit_telegram_message(
                        self.__token,
                        self.__chat_id,
                        self.__status_message_id,
                        f"Running job_id_{self.__id}.\n"
                        f"creator_id: {creator_id},"
                        f"from: {provider}/{service}\n"
                        "Status: downloading\n"
                        f'Post {i+1}/{kd.get_post_count()}\n'
                        'Status: cleaning cache'
                    )
                    clean_cache(path, False)
            else:
                utils.edit_telegram_message(
                    self.__token,
                    self.__chat_id,
                    self.__status_message_id,
                    f"Running job_id_{self.__id}.\n"
                    f"creator_id: {creator_id},"
                    f"from: {provider}/{service}\n"
                    "Status: downloading\n"
                    f'Post {i+1}/{kd.get_post_count()}\n'
                    'Status: skipped'
                )

        utils.edit_telegram_message(
            self.__token,
            self.__chat_id,
            self.__status_message_id,
            f"Running job_id_{self.__id}.\n"
            f"creator_id: {creator_id},"
            f"from: {provider}/{service}\n"
            "Status: done"
        )
