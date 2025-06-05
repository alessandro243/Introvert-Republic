import discord
import asyncio
import os

from discord.ext import commands
from discord import FFmpegPCMAudio, PCMVolumeTransformer
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.voice_states = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

ID_CANAL_DE_VOZ = 1377161141469315132
ID_CANAL_TEXTO = 1221650782364762164  # Canal de texto da escadaria

FFMPEG_PATH = "C:\\Users\\Thalita\\Downloads\\ffmpeg-7.1.1-essentials_build\\ffmpeg-7.1.1-essentials_build\\bin\\ffmpeg.exe"

voice_client_global = None
player = None
volume_atual = None

@bot.event
async def on_ready():
    print(f"✅ Bot online como {bot.user}")

@bot.event
async def on_voice_state_update(member, before, after):
    global voice_client_global

    if after.channel and after.channel.id == ID_CANAL_DE_VOZ and not member.bot:
        if not voice_client_global or not voice_client_global.is_connected():
            canal = after.channel
            voice_client_global = await canal.connect()
            print(f"🔊 Conectado a {canal.name}")
            asyncio.create_task(loop_musica(voice_client_global))
            asyncio.create_task(verificar_volume_dinamico())

    if before.channel and before.channel.id == ID_CANAL_DE_VOZ:
        canal = before.channel
        if len([m for m in canal.members if not m.bot]) == 0:
            if voice_client_global and voice_client_global.is_connected():
                await voice_client_global.disconnect()
                print("👋 Desconectado (canal vazio)")

async def loop_musica(voice_client):
    global player, volume_atual
    ultima_musica = ""

    while voice_client.is_connected():
        try:
            # Verificar se jukebox está ativa
            jukebox_ativa = True
            if os.path.exists("estadojuke/online.txt"):
                with open("estadojuke/online.txt", "r") as f:
                    status = f.read().strip().lower()
                    jukebox_ativa = status == "true"
            
            with open("estadojuke\pause.txt", 'r') as fi:
                pausado = fi.read().strip()

                if pausado == 'True':
                    voice_client_global.pause()
                else:
                    voice_client_global.resume()

            if not jukebox_ativa:
                if voice_client.is_playing():
                    voice_client.stop()
                await asyncio.sleep(2)
                continue

            if not os.path.exists("musics.txt"):
                await asyncio.sleep(2)
                continue

            with open("musics.txt", "r") as file:
                linhas = file.readlines()
                if len(linhas) < 1:
                    await asyncio.sleep(2)
                    continue

                caminho = linhas[0].strip()
                nome = linhas[1].strip() if len(linhas) > 1 else os.path.basename(caminho)

            if nome != ultima_musica:
                ultima_musica = nome

                if voice_client.is_playing():
                    voice_client.stop()

                with open("estadojuke/tempomusica.txt", "r") as file:
                    timer = int(file.read())

                source = FFmpegPCMAudio(caminho, executable=FFMPEG_PATH, before_options=f'-ss {timer}')

                if os.path.exists("estadojuke/estadosom.txt"):
                    with open("estadojuke/estadosom.txt", "r") as file:
                        volume_atual = float(file.read())
                else:
                    volume_atual = 0.2

                player = PCMVolumeTransformer(source, volume=volume_atual / 2.8)
                voice_client.play(player)

            await asyncio.sleep(2)

        except Exception as e:
            print(f"❗Erro no loop de música: {e}")
            await asyncio.sleep(5)

async def verificar_volume_dinamico():
    global player, volume_atual
    caminho_volume = "estadojuke/estadosom.txt"

    while True:
        try:
            if os.path.exists(caminho_volume):
                with open(caminho_volume, "r") as file:
                    novo_volume = float(file.read().strip())

                if novo_volume != volume_atual:
                    volume_atual = novo_volume
                    if player:
                        player.volume = volume_atual / 2.8
                        print(f"🔊 Volume atualizado: {round(player.volume, 2)}")
        except Exception as e:
            print(f"⚠️ Erro ao atualizar volume: {e}")

        await asyncio.sleep(1)

# ⬇️ Coloque seu token real aqui

bot.run(os.getenv('TOKKEN_SOM_ESCADA'))
