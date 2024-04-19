from KemonoDownloader import KemonoDownloader
from config import config

import utils
import shutil
import os


class ThePervector:

    def __init__(self):
        self.__kd = None

    def download_and_send(self, provider: str, service: str, creator_id: int):

        self.__kd = KemonoDownloader(provider, service, creator_id)

        for i in range(self.__kd.get_post_count()):

            def clean_cache(cleaned: str, with_split: bool):
                shutil.rmtree(cleaned)
                os.remove(f'{cleaned}.zip')
                if with_split:
                    shutil.rmtree(f'{cleaned}_split')
                    os.remove(f'{cleaned}_split.mergefile')

            path = self.__kd.download(i)

            if path != 'skipped':
                print(path)

                utils.pack(path)

                print('packed')

                if os.path.getsize(path + ".zip") > config['CHUNK_SIZE']:
                    utils.split(path, "zip", config['CHUNK_SIZE'])
                    print('split')
                    utils.dump_to_telegram(
                        config['TOKEN'],
                        config['CHAT_ID'],
                        path + "_split",
                        True
                    )
                    clean_cache(path, True)
                    print('sent')
                else:
                    utils.dump_to_telegram(
                        config['TOKEN'],
                        config['CHAT_ID'],
                        path + ".zip",
                        False
                    )
                    print('sent')
                    clean_cache(path, False)


