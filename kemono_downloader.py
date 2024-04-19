from config import config
from pathlib import Path

import requests
import urllib.request
import urllib.error
import utils
import time


class KemonoDownloader:

    def __init__(self, provider: str, service: str, user_id: int, update_data: dict):
        self.__provider = provider
        self.__service = service
        self.__user_id = user_id
        self.__posts_data = []
        self.__post_count = 0
        self.__update_data = update_data
        self.__fetch_data()

    def __fetch_data(self):

        utils.edit_telegram_message(
            self.__update_data['token'],
            self.__update_data['chat_id'],
            self.__update_data['update_message'],
            f"Running job_id_{self.__update_data['update_message']}."
            f"creator_id: {self.__update_data['creator_id']},"
            f"from: {self.__update_data['provider']}/{self.__update_data['service']}\n"
            f'Status: fetching posts'
        )

        page = 0

        while True:

            response = requests.get(
                f'https://{self.__provider}.su/api/v1/{self.__service}/user/{self.__user_id}'
                f'?o={page * config["KEMONO_OFFSET"]}'
            )

            posts = None

            if response:
                posts = response.json()

            if posts is None or len(posts) == 0:
                break

            for post in posts:
                self.__posts_data.append(
                    {
                        'id': post['id'],
                        'title': post['title'],
                        'date': post['published'],
                        'files': post['attachments']
                    }
                )

            page += 1

        utils.edit_telegram_message(
            self.__update_data['token'],
            self.__update_data['chat_id'],
            self.__update_data['update_message'],
            f"Running job_id_{self.__update_data['update_message']}."
            f"creator_id: {self.__update_data['creator_id']},"
            f"from: {self.__update_data['provider']}/{self.__update_data['service']}\n"
            "Status: collected"
            f'Collected {len(self.__posts_data)} posts'
        )

    def get_post_count(self):
        return len(self.__posts_data)

    def download(self, post_idx: int) -> str:
        post = self.__posts_data[post_idx]

        if len(post['files']) == 0:
            return 'skipped'
        else:
            path = f"{post['id']}-{post['title']}".replace("/", "---")

            Path(path).mkdir(parents=True, exist_ok=True)

            for i in range(len(post['files'])):
                att = 0
                while True:

                    try:
                        urllib.request.urlretrieve(
                            f"https://{self.__provider}.su/{post['files'][i]['path']}",
                            f"{path}/{post['id']}-{i}-{post['files'][i]['name']}"
                        )
                        break
                    except urllib.error.HTTPError:
                        time.sleep(30)
                        att += 1
                        if att > 15:
                            print("I fucking can't")
                            break

            return path



