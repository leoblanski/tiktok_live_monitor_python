import random
import os
from TikTokLive import TikTokLiveClient
from TikTokLive.types.events import *

import speech_recognition as sr
from gtts import gTTS
import os
import time
import playsound
from sounds import *  



# Instância a conexão com o @ do usuário
client: TikTokLiveClient = TikTokLiveClient(unique_id="@leoblanskii", **(
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

#Quantidade mínima para reproduzir a fala
minimumQty = 5

#Quantidade mínima para reproduzir o meme
minimumQtyMeme = 10

#Quantidade mínima para reproduzir dizer para seguir
minimumSayFollow = 20


arrayLikes = {}

# Usado para fala da "alexa"
def notifier(text, qty):
    if (qty >= minimumQty):
        print(f"""
╭💜💜💜💜💜💜💜💜💜💜💜💜💜💜💜💜💜💜💜💜╮
 {text}
╰💜💜💜💜💜💜💜💜💜💜💜💜💜💜💜💜💜💜💜💜╯
        """)
        playsound.playsound("moedas.mp3")
    else:
        print(f"{text}\n")

    tts = gTTS(text=text, lang='pt')
    filename = 'voice.mp3'
    tts.save(filename)
    playsound.playsound(filename)


# Usado para som do meme
def mp3Sound():
    _random = random.randint(1,4)

   # print(fileSoundName)
    playsound.playsound(f"sound_{_random}.mp3")

@client.on("comment")
async def on_connect(event: CommentEvent):
    print(f"{event.user.nickname}: {event.comment}\n")


# Executa a conecção
@client.on("connect")
async def on_connect(_: ConnectEvent):
    os.system("clear")
    print("Conectado com sucesso a live:", client.room_id)

# Monitoramento de likes
@client.on("like")
async def on_like(event: LikeEvent):
    if (event.user.nickname in arrayLikes) :
        arrayLikes[event.user.nickname] = arrayLikes[event.user.nickname] + event.likeCount
    else: 
        arrayLikes[event.user.nickname] = event.likeCount
    
    print(f"{event.user.nickname} já enviou {arrayLikes[event.user.nickname]} likes\n")

# Monitoramento de seguidores
@client.on("follow")
async def on_follow(event: FollowEvent):
    _random = random.randint(1,3)

    #transfer to swith case
    if (_random == 1):
        notifier(f"{event.user.nickname} valeu por seguir!", 0)
    if (_random == 2):
        notifier(f"Obrigado {event.user.nickname} por me seguir.", 0)
    if (_random == 3):
        notifier(f"Seguido por {event.user.nickname}.", 0)

    # mp3Sound(0)
 
# Monitoramento de presentes
@client.on("gift")
async def on_gift(event: GiftEvent):
    #Se irá disparar o evento da fala
    isImportant = event.gift.repeat_count >= minimumQty or event.gift.extended_gift.diamond_count >= minimumQty

    if event.gift.gift_type == 1:

        if event.gift.repeat_end == 1 and (isImportant):
            conector = "pelo"
            plural = ""
            qty = 0

            mustPlaySoundMeme = event.gift.repeat_count >= minimumQtyMeme or event.gift.extended_gift.diamond_count >= minimumQtyMeme and event.gift.repeat_count < minimumSayFollow 
            mustFollow = event.gift.repeat_count >= minimumSayFollow 

            if event.gift.extended_gift.name == "Rosa":
                conector = "pela"

            if event.gift.repeat_count >= minimumQty or event.gift.extended_gift.diamond_count >= minimumQty:
                plural = "s"
                qty = event.gift.repeat_count          
       
            notifier(f"{event.user.nickname} Obrigado {conector}{plural} {qty} {event.gift.extended_gift.name}{plural}!", qty)
            
            #Se deve falar o meme
            if (mustPlaySoundMeme):
                mp3Sound()

            #Se deve falar para seguir
            if (mustFollow):
                notifier(f"Vamos seguir o {event.user.nickname}!", qty)

        if event.gift.repeat_end == 1 and event.gift.repeat_count < minimumQty:
            print(f"""
╭💜💜💜💜💜💜💜💜💜💜💜💜💜💜💜💜💜💜💜💜╮
 {event.user.nickname} enviou {event.gift.repeat_count}x {event.gift.extended_gift.name}!
╰💜💜💜💜💜💜💜💜💜💜💜💜💜💜💜💜💜💜💜💜╯\n
""")

    elif event.gift.gift_type != 1 and event.gift.extended_gift.diamond_count >= 10:
        notifier(f"{event.user.nickname} Obrigado pelo presente!", event.gift.extended_gift.diamond_count)


@client.on("error")
async def on_connect(error: Exception):
    # Handle the error
    if isinstance(error, Exception):
        print("Notificando telespectadores")
        return

    # Otherwise, log the error
    client._log_error(error)

if __name__ == '__main__':
    # Run the client and block the main thread
    # await client.start() to run non-blocking
    client.run()
