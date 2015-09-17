__author__ = 'Matthew Tuusberg'

import os
import requests
import json
import settings

from vkappauth import VKAppAuth


def authenticate(email, password, app_id, scope):
    return VKAppAuth().auth(email, password, app_id, scope)


def get_audio_list(access_data):
    url = "https://api.vkontakte.ru/method/" \
          "audio.get?uid=" + access_data['user_id'] + \
          "&access_token=" + access_data['access_token']

    response = requests.get(url)
    return json.loads(response.text)['response']


def download_audios(folder, audio_list):
    if not os.path.exists(folder):
        os.makedirs(folder)

    number = len(audio_list)

    for index, song in enumerate(audio_list):
        artist = song['artist']
        title = song['title']
        url = song['url']

        print("Downloading %d / %d: %s - %s" % (index + 1, number, artist, title))

        filename = "%s - %s.mp3" % (song['artist'], song['title'])
        filename = remove_invalid_chars(filename)
        filename = os.path.join(folder, filename)

        if not os.path.exists(filename):
            try:
                with open(filename, "wb") as out:
                    response = requests.get(song['url'].split('?')[0])
                    out.write(response.content)
            except IOError:
                pass
            except:
                raise


def remove_invalid_chars(filename):
    return "".join(i for i in filename if i not in r'\/:*?"<>|')


def main():
    print
    "Authentication..."
    access_data = authenticate(settings.email, settings.password, settings.app_id, settings.scope)
    print
    'Done!'

    print
    'Connecting to VKAPI...'
    audio_list = get_audio_list(access_data)
    print
    "Done!"

    print
    'Downloading...'
    download_audios(settings.output_folder, audio_list)
    print
    'Done!'


if __name__ == '__main__':
    main()



