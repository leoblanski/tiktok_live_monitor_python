from TikTokLive import TikTokLiveClient
from TikTokLive.types.events import *

import speech_recognition as sr
from gtts import gTTS
import os
import time
import playsound

# Instância a conexão com o @ do usuário
client: TikTokLiveClient = TikTokLiveClient(unique_id="@leoblanskii")

# Usado para fala
def notifier(text):
    print(text)
    tts = gTTS(text=text, lang='pt')
    filename = 'voice.mp3'
    tts.save(filename)
    playsound.playsound(filename)


# Executa a conecção
@client.on("connect")
async def on_connect(_: ConnectEvent):
    print("Conectado com sucesso a live:", client.room_id)

# @client.on("join")
# async def on_join(event: JoinEvent):
#     notifier(f"{event.user.nickname} seja vem vindo a laive.")

# Monitoramento de likes

# @client.on("like")
# async def on_like(event: LikeEvent):
#    print(f"{event.user.nickname} - {event.like.likeCount}!")

@client.on("follow")
async def on_follow(event: FollowEvent):
    notifier(f"{event.user.nickname} Seguiu o anfitrião.")


# Monitoramento de 
@client.on("gift")
async def on_gift(event: GiftEvent):
    # If it's type 1 and the streak is over
    if event.gift.gift_type == 1:
        if event.gift.repeat_end == 1:
            if event.gift.repeat_count == 1 :
                notifier(f"{event.user.nickname} Obrigado pelos presentes!")
            else: 
                notifier(f"{event.user.nickname} Obrigadoo pelos presentes, esssssssssquece!!")
    # It's not type 1, which means it can't have a streak & is automatically over
    elif event.gift.gift_type != 1:
        notifier(f"{event.user.nickname} Obrigado pelo presente!")


if __name__ == '__main__':
    # Run the client and block the main thread
    # await client.start() to run non-blocking
    client.run()
