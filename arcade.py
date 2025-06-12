import discord
import asyncio
import random
import psutil
from discord import PCMVolumeTransformer
from dotenv import load_dotenv
from os import getenv
import os
import datetime
load_dotenv()

# ================== CONFIGURAÇÕES ==================
TOKEN = getenv('TOKKEN_ARCADE')
ID_CANAL_VOZ = 1354311386100011078
NOME_BOT = 'Jukebox'
FMPEG = "C:\\Users\\Thalita\\Downloads\\ffmpeg-7.1.1-essentials_build\\ffmpeg-7.1.1-essentials_build\\bin\\ffmpeg.exe"
# ====================================================

intents = discord.Intents.default()
intents.voice_states = True
intents.guilds = True
intents.members = True

client = discord.Client(intents=intents)
playing_task = None

def nightdom():
    agora = datetime.datetime.now()
    dom = datetime.datetime.now()
    nome_dia = dom.strftime("%A")  # Nome do dia em inglês, ex: 'Wednesday'
    
    if nome_dia in ['Sunday', 'sunday'] and 18 <= agora.hour <= 23:
        print('no if')
        caminho = 'arcadesons\\issunday\\1talk.mp3'
        audi = [f"arcadesons\\issunday\\som{i}.mp3" for i in range(1, 5)]
        #print(caminho, audi)
        return caminho, audi
    
    caminho = 'arcadesons\\notsunday\\silencio.mp3'
    audi = [f"arcadesons\\notsunday\\som{i}.mp3" for i in range(1, 5)]
    #print(caminho, audi)
    return caminho, audi

def jukebox_esta_rodando():
    for proc in psutil.process_iter(['cmdline']):
        try:
            cmdline = proc.info['cmdline']
            if cmdline and any('jukebox.py' in part for part in cmdline):
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return False

async def bot_esta_no_canal():
    guilds = client.guilds
    for guild in guilds:
        voice_client = guild.voice_client
        if voice_client and voice_client.channel:
            nomes_membros = [m.name for m in voice_client.channel.members]
            if NOME_BOT in nomes_membros:
                if voice_client.channel.id == ID_CANAL_VOZ:
                    return True
    return False

async def checar_status_completo():
    rodando = jukebox_esta_rodando()
    no_canal = await bot_esta_no_canal()
    if rodando and no_canal:
        return True
    else:
        return False

@client.event
async def on_ready():
    print(f'✅ Bot conectado como {client.user}')

@client.event
async def on_voice_state_update(member, before, after):
    if member.bot:
        return

    canal = after.channel or before.channel
    if not canal:
        return

    print(f"[DEBUG] Canal: {canal.name} | Membros: {[m.name for m in canal.members]}")

    nomes_membros = [m.name for m in canal.members]
    if NOME_BOT not in nomes_membros:
        print(f"⚠️ Aviso: O bot '{NOME_BOT}' NÃO está presente no canal {canal.name}")
    else:
        print(f"✅ Bot '{NOME_BOT}' detectado no canal {canal.name}")

    if canal.id == ID_CANAL_VOZ and not canal.guild.voice_client:
        await conectar_e_tocar_loop(canal)

async def checar_jukebox_enquanto_toca(voice_client):
    while voice_client.is_connected() and voice_client.is_playing():
        status_completo = await checar_status_completo()
        if status_completo:
            print("[STATUS] Jukebox ONLINE (script rodando e bot no canal)")
            with open("estadojuke\online.txt", "w") as f:
                f.write('True')
        else:
            print("[STATUS] Jukebox OFFLINE (script ou bot não estão OK)")
            with open("estadojuke\online.txt", "w") as f:
                f.write('False')
        await asyncio.sleep(1)

async def conectar_e_tocar_loop(canal):
    global playing_task

    voice_client = await canal.connect()
    print(f"🔊 Conectado ao canal: {canal.name}")

    async def loop_audio():
        while voice_client.is_connected():
            canal_atual = await voice_client.channel.guild.fetch_channel(voice_client.channel.id)
            nomes_membros = [m.name for m in canal_atual.members]

            caminho, audi = nightdom()

            if NOME_BOT not in nomes_membros:
                print(f"⚠️ [loop] O bot '{NOME_BOT}' NÃO está presente no canal {canal_atual.name}")
            else:
                print(f"✅ [loop] Bot '{NOME_BOT}' detectado no canal {canal_atual.name}")

            # Toca silêncio
            source = discord.FFmpegPCMAudio(
                caminho,
                executable=FMPEG,
                options='-af "acompressor=threshold=0.1:ratio=20:attack=5:release=50,highpass=f=800,lowpass=f=1500,aresample=22050"'
            )
            source = PCMVolumeTransformer(source, volume=0.6)
            voice_client.play(source)

            # Checa status enquanto toca
            await asyncio.gather(
                checar_jukebox_enquanto_toca(voice_client)
            )

            await asyncio.sleep(10)

            if random.randint(1, 4) == 1:
                audios = audi
                som_escolhido = random.choice(audios)
                print('aaaaaaaaaaaaaaaa', som_escolhido)
                print(f"🎵 Tocando áudio aleatório: {som_escolhido}")
                source = discord.FFmpegPCMAudio(
                    som_escolhido,
                    executable=FMPEG,
                    options='-af "acompressor,highpass=f=300,lowpass=f=3000"'
                )
                voice_client.play(source)

                # Checa status enquanto toca
                await asyncio.gather(
                    checar_jukebox_enquanto_toca(voice_client)
                )

    if not playing_task or playing_task.done():
        playing_task = asyncio.create_task(loop_audio())

client.run(TOKEN)
