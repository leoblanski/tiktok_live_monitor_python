import random
from TikTokLive import TikTokLiveClient
from TikTokLive.types.events import *

import speech_recognition as sr
from gtts import gTTS
import os
import time
import playsound
from sounds import *  

# Instância a conexão com o @ do usuário
client: TikTokLiveClient = TikTokLiveClient(unique_id="@ojeevaan", **(
        {
            # Whether to process initial data (cached chats, etc.)
            "process_initial_data": True,

            # Connect info (viewers, stream status, etc.)
            "fetch_room_info_on_connect": True,

            # Whether to get extended gift info (Image URLs, etc.)
            "enable_extended_gift_info": True,

            # How frequently to poll Webcast API
            "polling_interval_ms": 1000,

            # Custom Client params
            "client_params": {},

            # Custom request headers
            "headers": {},

            # Custom timeout for Webcast API requests
            "timeout_ms": 1000,

            # Set the language for Webcast responses (Changes extended_gift's language)
            "lang": "pt-BR"
        }
    )
)

arrayLikes = {}

# Usado para fala da "alexa"
def notifier(text):
    print(text)
    tts = gTTS(text=text, lang='pt')
    filename = 'voice.mp3'
    tts.save(filename)
    playsound.playsound(filename)

# Usado para som
def mp3Sound(indexSound):
    #posição do caminho do som no array
    fileSoundName = sounds_array[indexSound]

   # print(fileSoundName)
    playsound.playsound(fileSoundName)


# Executa a conecção
@client.on("connect")
async def on_connect(_: ConnectEvent):
    print("Conectado com sucesso a live:", client.room_id)

# @client.on("join")
# async def on_join(event: JoinEvent):
#     notifier(f"{event.user.nickname} seja vem vindo a laive.")

# Monitoramento de likes

@client.on("like")
async def on_like(event: LikeEvent):
    if (event.user.nickname in arrayLikes) :
        arrayLikes[event.user.nickname] = arrayLikes[event.user.nickname] + event.likeCount
    else: 
        arrayLikes[event.user.nickname] = event.likeCount

    print(f"{event.user.nickname} já enviou {arrayLikes[event.user.nickname]} likes")

# Monitoramento de seguidores
@client.on("follow")
async def on_follow(event: FollowEvent):
    _random = random.randint(1,3)

    #transfer to swith case
    if (_random == 1):
        notifier(f"{event.user.nickname} valeu por seguir!")
    if (_random == 2):
        notifier(f"Obrigado {event.user.nickname} por me seguir.")
    if (_random == 3):
        notifier(f"Seguido por {event.user.nickname}.")

    f(_random)
    # mp3Sound(0)
 
# Monitoramento de presentes
@client.on("gift")
async def on_gift(event: GiftEvent):
    #Quantidade mínima para reproduzir a fala
    minimumQty = 5

    #Quantidade mínima para reproduzir o meme
    minimumQtyMeme = 10

    #Se irá disparar o evento da fala
    isImportant = event.gift.repeat_count >= minimumQty or event.gift.extended_gift.diamond_count >= minimumQty

    if event.gift.gift_type == 1:

        if event.gift.repeat_end == 1 and (isImportant):
            conector = "pelo"
            plural = ""
            qty = 0

            mustPlaySoundMeme = event.gift.repeat_count >= minimumQtyMeme or event.gift.extended_gift.diamond_count >= minimumQtyMeme
            
            if event.gift.extended_gift.name == "Rosa":
                conector = "pela"

            if event.gift.repeat_count >= minimumQty or event.gift.extended_gift.diamond_count >= minimumQty:
                plural = "s"
                qty = event.gift.repeat_count          
       
            notifier(f"{event.user.nickname} Obrigado {conector}{plural} {qty} {event.gift.extended_gift.name}{plural}!")
            
            #Diz se deve soltar o meme do luva de pedreiro
            if (mustPlaySoundMeme):
                mp3Sound(0)

    elif event.gift.gift_type != 1 and event.gift.extended_gift.diamond_count >= 10:
        notifier(f"{event.user.nickname} Obrigado pelo presente!")



if __name__ == '__main__':
    # Run the client and block the main thread
    # await client.start() to run non-blocking
    client.run()
