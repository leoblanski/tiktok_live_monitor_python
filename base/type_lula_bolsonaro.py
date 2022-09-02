import random
import os
from TikTokLive import TikTokLiveClient
from TikTokLive.types.events import *

import speech_recognition as sr
from gtts import gTTS
import os
import time
import playsound
import requests
from http.client import HTTPConnection  # py3
import logging
from sounds import * 
import json

# Instantiate the client with the user's username
client: TikTokLiveClient = TikTokLiveClient(unique_id="@daniielbn2")

apiUrl = "http://localhost:8989/api"

typeLike = 1
typeGift = 2
typeVote = 3

voteLula = 1
voteBolsonaro = 2

arrayLikes = {}

#utilizado para logs
def logPrint():
    log = logging.getLogger('urllib3')
    log.setLevel(logging.DEBUG)

    # logging from urllib3 to console
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    log.addHandler(ch)


# print statements from `http.client.HTTPConnection` to console/stdout
HTTPConnection.debuglevel = 0

#Utilizado para enviar a informação para API
def saveMoviment(params, type):
    response = requests.post(apiUrl + "/saveMoviment", json=params)

    print(response.text)
    print('Registrado movimentação na API =>> Tipo: ' + type)


#Utilizado falar texto
def playSound(text):
    tts = gTTS(text=text, lang='pt')
    filename = 'voice.mp3'
    tts.save(filename)
    playsound.playsound(filename)

def playThanksSound(event):
    _random = random.randint(1,3)

    if (_random == 1):
        playSound(f"{event.user.nickname} obrigado pelo presente!")
    if (_random == 2):
        playSound(f"Obrigado {event.user.nickname} por patrocinar a live!.")
    if (_random == 3):
        playSound(f"Obrigado pelos presentes  {event.user.nickname}.")

# Usado para som do meme
def mp3Sound():
    _random = random.randint(1,4)

   # print(fileSoundName)
    playsound.playsound(f"sound_{_random}.mp3")

@client.on("comment")
async def on_comment(event: CommentEvent):
    params = {
        'user': event.user.uniqueId,
        'qty': 1,
        'profile_picture': event.user.profilePicture.urls[0],
        'name': event.user.nickname,
        'type': typeVote,
    }

    if event.comment.find("/lula"):
        params['vote'] = voteLula
    
    if event.comment.find("/bolsonaro"):
        params['vote'] = voteBolsonaro

    if params['vote'] != '':
        saveMoviment(params, 'Vote')
        
    print(f"{event.user.nickname}: {event.comment}\n")

    params = {}

# Executa a conecção
@client.on("connect")
async def on_connect(_: ConnectEvent):
    os.system("clear")
    print("Conectado com sucesso a live:", client.room_id)

# Monitoramento de likes
@client.on("like")
async def on_like(event: LikeEvent):

    params = {
        'user': event.user.uniqueId,
        'qty': 1,
        'profile_picture': event.user.profilePicture.urls[0],
        'name': event.user.nickname,
        'type': typeLike,
    }

    saveMoviment(params, 'Likes')

    if (event.user.nickname in arrayLikes) :
        arrayLikes[event.user.nickname] = arrayLikes[event.user.nickname] + event.likeCount
    else: 
        arrayLikes[event.user.nickname] = event.likeCount
    
    print(f"{event.user.nickname} já enviou {arrayLikes[event.user.nickname]} likes\n")
    params = {}

# Monitoramento de seguidores
@client.on("follow")
async def on_follow(event: FollowEvent):
    _random = random.randint(1,3)

    if (_random == 1):
        playSound(f"{event.user.nickname} valeu por seguir!")
    if (_random == 2):
        playSound(f"Obrigado {event.user.nickname} por me seguir.")
    if (_random == 3):
        playSound(f"Seguido por {event.user.nickname}.")

 
# Monitoramento de presentes
@client.on("gift")
async def on_gift(event: GiftEvent):
    params = {
        'user': event.user.uniqueId,
        'name': event.user.nickname,
        'qty': 1,
        'amount': event.gift.extended_gift.diamond_count,
        'profile_picture': event.user.profilePicture.urls[0],
        'name': event.user.nickname,
        'type': typeGift,
    }

    saveMoviment(params, 'Gift')
    params = {}
    
    if event.gift.gift_type == 1:
        if event.gift.repeat_end == 1:
            if event.gift.repeat_count >= 5:
                playThanksSound(event)

    print(f"{event.user.nickname} enviou {event.gift.repeat_count}x {event.gift.extended_gift.name}")

# Define handling an event via "callback"
client.add_listener("comment", on_comment)
client.add_listener("like", on_like)
client.add_listener("follow", on_follow)
client.add_listener("gift", on_gift)

@client.on("error")
async def on_connect(error: Exception):
    # Handle the error
    if isinstance(error, Exception):
        print("Notificando telespectadores")
        print(error)
        return

    # Otherwise, log the error
    client._log_error(error)

if __name__ == '__main__':
    # Run the client and block the main thread
    # await client.start() to run non-blocking
    client.run()
