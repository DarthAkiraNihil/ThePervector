from pathlib import Path
from filesplit.split import Split

import os
import zipfile
import shutil
import requests


def pack(packed_file: str):
    def zipdir(path, zip_handle):
        for root, dirs, files in os.walk(path):
            for file in files:
                zip_handle.write(os.path.join(root, file),
                                 os.path.relpath(os.path.join(root, file),
                                                 os.path.join(path, '..')))

    with zipfile.ZipFile(f'{packed_file}.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipdir(f'{packed_file}/', zipf)


def split(path: str, extension: str, chunk_size: int):
    def write_mergefile(for_dir: str):
        with open(f"{for_dir}.mergefile", "w+", encoding='utf8') as mergefile:
            files = os.listdir(for_dir)
            for f in files:
                if f != 'manifest':
                    mergefile.write(f + '\n')

    out_dir = f"{path}_split"
    Path(out_dir).mkdir(parents=True, exist_ok=True)

    Split(f"{path}.{extension}", out_dir).bysize(chunk_size)

    write_mergefile(out_dir)

    return out_dir


def merge(mergefile: str):
    files = []
    with open(mergefile, "r", encoding='utf8') as mergefile:
        files += list(map(str.rstrip, mergefile.readlines()[:-1]))
    with open("merged_file.zip", "wb+") as outfile:
        for file in files:
            with open(file, "rb") as infile:
                shutil.copyfileobj(infile, outfile)


def merge_all(mergefiles_dir: str = '.'):
    for f in os.listdir(mergefiles_dir):
        if f.endswith(".mergefile"):
            merge(f)


def send_telegram_message(
        token: str,
        chat_id: str,
        text: str
):
    url_request_template = f'https://api.telegram.org/bot{token}'

    return requests.post(
        f'{url_request_template}/sendMessage',
        data={
            'chat_id': chat_id,
            'text': text
        }
    ).json()['result']['message_id']


def edit_telegram_message(
        token: str,
        chat_id: str,
        message_id: int,
        text: str
):
    url_request_template = f'https://api.telegram.org/bot{token}'

    requests.post(
        f'{url_request_template}/editMessageText',
        data={
            'chat_id': chat_id,
            'message_id': message_id,
            'text': text
        }
    )

def dump_to_telegram(
        token: str,
        chat_id: str,
        path: str,
        is_dir: bool,
        begin_message: str = 'A new package has arrived',
):

    url_request_template = f'https://api.telegram.org/bot{token}'

    def send_file(file_path):
        return requests.post(
            f'{url_request_template}/sendDocument',
            data={
                'chat_id': chat_id
            },
            files={
                'document': open(file_path, 'rb')
            },
            stream=True
        ).status_code

    print(requests.post(
        f'{url_request_template}/sendMessage',
        data={
            'chat_id': chat_id,
            'text': begin_message
        }
    ).status_code)

    if is_dir:
        for f in os.listdir(path):
            if f != 'manifest':
                print(send_file(f'{path}/{f}'))
        send_file(f'{path}.mergefile')
    else:
        print(send_file(path))
