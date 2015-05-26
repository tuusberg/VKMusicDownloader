__author__ = 'Matthew Tuusberg'

import os
import requests
import logging
from vkappauth import VKAppAuth
import json


def remove_invalid_chars(filename):
    return "".join(i for i in filename if i not in r'\/:*?"<>|')


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
        if index != 314: continue
        artist = song['artist']
        title  = song['title']
        url    = song['url']

        print("Downloading %d / %d: %s - %s" % (index + 1, number, artist, title))

        filename = "%s - %s.mp3" % (song['artist'], song['title'])
        filename = remove_invalid_chars(filename)
        filename = os.path.join(folder, filename)

        if not os.path.exists(filename):
           # try:
                with open(filename, "wb") as out:
                    response = requests.get(song['url'].split('?')[0])
                    out.write(response.content)
           # except IOError:
           #     pass
           # except:
           #    raise


# credentials
email    = ""
password = ""
app_id   = "4856994"
scope    = "audio"

print "Authentication"
access_data = authenticate(email, password, app_id, scope)
print "Done!"

print 'Connecting to VKAPI'
audio_list = get_audio_list(access_data)
print "Done!"

print "Downloading"
folder = "d:\VKAudioDownloader"
download_audios(folder, audio_list)
print "Done!"


