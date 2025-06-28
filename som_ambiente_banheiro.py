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
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

ID_CANAL_DE_VOZ = 1376116149472727111  # ID do canal de voz do corredor
FFMPEG_PATH = "C:\\Users\\Usuario\\Desktop\\ffmpeg-7.1.1-essentials_build\\ffmpeg-7.1.1-essentials_build\\bin\\ffmpeg.exe"

voice_client_global = None
player = None
volume_atual = None

@bot.event
async def on_ready():
    print(f"✅ Bot online como {bot.user}")
    asyncio.create_task(monitorar_volume())

@bot.event
async def on_voice_state_update(member, before, after):
    global voice_client_global

    if after.channel and after.channel.id == ID_CANAL_DE_VOZ and not member.bot:
        if not voice_client_global or not voice_client_global.is_connected():
            canal = after.channel
            voice_client_global = await canal.connect()
            print(f"🔊 Conectado a {canal.name}")
            asyncio.create_task(loop_musica(voice_client_global))

    if before.channel and before.channel.id == ID_CANAL_DE_VOZ:
        canal = before.channel
        if len([m for m in canal.members if not m.bot]) == 0:
            if voice_client_global and voice_client_global.is_connected():
                await voice_client_global.disconnect()
                print("👋 Desconectado (canal vazio)")

async def loop_musica(voice_client):
    global player, volume_atual, voice_client_global
    ultima_musica = ""

    while voice_client.is_connected():
        try:
            # Verificar online.txt ANTES de tocar qualquer coisa
            if os.path.exists("estadojuke\\online.txt"):
                with open("estadojuke\\online.txt", "r") as f:
                    online = f.read().strip()

                with open("estadojuke\pause.txt", 'r') as fi:
                    pausado = fi.read().strip()

                if pausado == 'True':
                    voice_client_global.pause()
                else:
                    voice_client_global.resume()

                if online != "True":
                    print('entrei')
                    if voice_client.is_playing():
                        voice_client.stop()
                        print("🛑 Parando reprodução (jukebox offline).")
                    await asyncio.sleep(1)
                    continue
            else:
                await asyncio.sleep(1)
                continue

            if not os.path.exists("musics.txt"):
                print("❌ musics.txt não encontrado.")
                await asyncio.sleep(2)
                continue

            with open("musics.txt", "r") as file:
                linhas = file.readlines()
                if len(linhas) < 1:
                    print("⚠️ musics.txt está vazio.")
                    await asyncio.sleep(2)
                    continue

                caminho = linhas[0].strip()
                nome = linhas[1].strip() if len(linhas) > 1 else os.path.basename(caminho)

            if nome != ultima_musica:
                print(f"🎵 Trocando para: {nome}")
                ultima_musica = nome

                if voice_client.is_playing():
                    voice_client.stop()

                with open("estadojuke\\tempomusica.txt", "r") as file:
                    timer = int(file.read())

                # Ler estado da porta
                estado_porta = "False"
                caminho_porta = "estadoambiente\\portabanheiro.txt"
                if os.path.exists(caminho_porta):
                    with open(caminho_porta, "r") as file:
                        estado_porta = file.read().strip()

                # Filtro lowpass conforme porta
                if estado_porta == "True":
                    filtro = "-af lowpass=f=400,volume=1.2"
                else:
                    filtro = "-af lowpass=f=800,volume=1.2"

                # Volume
                if os.path.exists('estadojuke\\estadosom.txt'):
                    with open('estadojuke\\estadosom.txt', 'r') as file:
                        volume_atual = float(file.read())
                else:
                    volume_atual = 0.2

                source_ffmpeg = FFmpegPCMAudio(
                    caminho,
                    executable=FFMPEG_PATH,
                    options=filtro,
                    before_options=f'-ss {timer}'
                )

                if estado_porta == "True":
                    volume_com_ajuste = (volume_atual / 2) / 2.8
                else:
                    volume_com_ajuste = (volume_atual * 2) / 2.8

                player = PCMVolumeTransformer(source_ffmpeg, volume=volume_com_ajuste)
                voice_client.play(player)

            await asyncio.sleep(1)

        except Exception as e:
            print(f"❗Erro no loop de música: {e}")
            await asyncio.sleep(5)

async def monitorar_volume():
    global player, volume_atual
    caminho_arquivo = 'estadojuke\\estadosom.txt'
    caminho_porta = "estadoambiente\\portabanheiro.txt"

    while True:
        try:
            if os.path.exists(caminho_arquivo):
                with open(caminho_arquivo, 'r') as f:
                    novo_volume = float(f.read().strip())

                estado_porta = "False"
                if os.path.exists(caminho_porta):
                    with open(caminho_porta, 'r') as file:
                        estado_porta = file.read().strip()

                if estado_porta == "True":
                    volume_com_ajuste = (novo_volume / 2) / 2.8
                else:
                    volume_com_ajuste = (novo_volume * 2) / 2.8

                if volume_com_ajuste != volume_atual:
                    volume_atual = volume_com_ajuste
                    if player:
                        player.volume = volume_atual
                        print(f"[Volume atualizado] Novo volume: {player.volume}")

            else:
                print(f"Arquivo {caminho_arquivo} não encontrado.")

        except Exception as e:
            print(f"Erro ao monitorar volume: {e}")

        await asyncio.sleep(1)

@bot.command()
async def fechar(ctx):
    if not ctx.author.voice or ctx.author.voice.channel.id != ID_CANAL_DE_VOZ:
        return

    with open('estadoambiente\\portabanheiro.txt', 'r') as file:
        cond = file.read().strip() == "True"

    if cond:
        await ctx.send("🚪 Porta do banheiro já está fechada.")
    else:
        await ctx.send("🚪 Fechando porta do banheiro.")

    with open('estadoambiente\\portabanheiro.txt', 'w') as file:
        file.write("True")

@bot.command()
async def abrir(ctx):
    if not ctx.author.voice or ctx.author.voice.channel.id != ID_CANAL_DE_VOZ:
        return

    with open('estadoambiente\\portabanheiro.txt', 'r') as file:
        cond = file.read().strip() == "True"

    if not cond:
        await ctx.send("🚪 Porta do banheiro já está aberta.")
    else:
        await ctx.send("🚪 Abrindo porta para o banheiro.")

    with open('estadoambiente\\portabanheiro.txt', 'w') as file:
        file.write("False")

# ⬇️ Coloque seu token real aqui
bot.run(os.getenv('TOKKEN_SOM_BANHEIRO'))
