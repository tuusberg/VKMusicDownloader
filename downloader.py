# coding=utf-8

import os
import requests
import utils
import settings

from argparse import ArgumentParser
from urllib import urlencode
from vkappauth import VKAppAuth
from click import progressbar


class Auth(object):
    def __init__(self, email, password, app_id, scope):
        self.email = email
        self.password = password
        self.app_id = app_id
        self.scope = scope

    def login(self):
        return VKAppAuth().auth(self.email, self.password, self.app_id, self.scope)


class VkMusic(object):
    def __init__(self, auth):
        self.auth = auth
        self.access_data = None

    def login(self):
        if self.access_data is None:
            self.access_data = self.auth.login()

    @property
    def audios(self):
        base_url = 'https://api.vkontakte.ru/method/audio.get?'
        url = base_url + urlencode(self.access_data)

        response = requests.get(url)
        return response.json()['response']

class Downloader(object):
    def __init__(self, outdir):
        self.outdir = outdir

    def download(self, filename, url, outdir=None):
        if outdir is None:
            outdir = self.outdir

        if not os.path.exists(outdir):
            os.makedirs(outdir)

        filename = utils.remove_invalid_chars(filename)
        filename = os.path.join(outdir, filename)

        response = requests.get(url, stream=True)

        if os.path.exists(filename):
            return filename

        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)

        return filename


def download_audios(outdir, audios):
    downloader = Downloader(outdir)
    number = len(audios)
    
    # haha 
    with progressbar(audios, fill_char='\b=э', bar_template='%(label)s [88%(bar)s] %(info)s') as bar:
        for idx, song in enumerate(bar):
            try:
                title = song['title'].encode('utf-8')
                artist = song['artist'].encode('utf-8')
                url = song['url']

                filename = '{} - {}.mp3'.format(artist, title)

                downloader.download(filename, url)

                bar.label = 'Downloading {}/{}'.format(idx + 1, number)
            except IOError:
                pass


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('--limit', '--l', nargs='?', type=int, default=None, help='')

    return parser.parse_args()


def main():
    args = parse_args()
    limit = args.limit

    print 'Authenticating ...'
    auth = Auth(settings.email, settings.password, settings.app_id, settings.scope)
    vkm = VkMusic(auth)
    vkm.login()

    outdir = os.path.dirname(os.path.abspath(__file__))
    audios = vkm.audios[:limit] if limit else vkm.audios

    download_audios(outdir, audios)


if __name__ == '__main__':
    main()






