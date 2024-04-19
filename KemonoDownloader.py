from config import config

import requests
import urllib.request
import urllib.error
from pathlib import Path
import time


class KemonoDownloader:

    def __init__(self, provider: str, service: str, user_id: int):
        self.__provider = provider
        self.__service = service
        self.__user_id = user_id
        self.__posts_data = []
        self.__post_count = 0
        self.__fetch_data()

    def __fetch_data(self):

        page = 0

        while True:

            response = requests.get(
                f'https://{self.__provider}.su/api/v1/{self.__service}/user/{self.__user_id}'
                f'?o={page * config["KEMONO_OFFSET"]}'
            )

            posts = None

            if not response:
                print('fuck')
                print(response.status_code)
                print(response.headers['Retry-After'])
            else:
                posts = response.json()

            if len(posts) == 0:
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

        print(f"collected {len(self.__posts_data)} posts")

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



