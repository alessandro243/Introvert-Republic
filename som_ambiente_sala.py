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

# IDs dos canais
ID_CANAL_DE_VOZ = 1365765011464523910
ID_CANAL_TEXTO = 1221650782364762164  # Canal para logs e comandos

# Caminho do ffmpeg
FFMPEG_PATH = r"C:\Users\Thalita\Downloads\ffmpeg-7.1.1-essentials_build\ffmpeg-7.1.1-essentials_build\bin\ffmpeg.exe"

voice_client_global = None
player = None

# Variáveis globais de estado
ultimo_volume = None
ultima_porta_fechada = None
ultima_musica_nome = None

async def tocar_musica_com_ajustes(voice_client, caminho, timer, volume_base, porta_fechada):
    global player, ultimo_volume, ultima_porta_fechada

    if porta_fechada:
        lowpass_freq = 1000   # som abafado
        volume_ajustado = volume_base / 2.5 / 2
    else:
        lowpass_freq = 1400  # som aberto
        volume_ajustado = (volume_base / 1.5)

    # Filtro simples lowpass (sem ruído)
    ffmpeg_options = f'-af lowpass=f={lowpass_freq}'

    if voice_client.is_playing():
        voice_client.stop()

    source = FFmpegPCMAudio(
        caminho,
        executable=FFMPEG_PATH,
        before_options=f'-ss {timer}',
        options=ffmpeg_options
    )

    player = PCMVolumeTransformer(source, volume=volume_ajustado)
    voice_client.play(player)

    ultimo_volume = volume_ajustado
    ultima_porta_fechada = porta_fechada

@bot.event
async def on_voice_state_update(member, before, after):
    global voice_client_global

    # Entrou no canal alvo
    if after.channel and after.channel.id == ID_CANAL_DE_VOZ and not member.bot:
        if not voice_client_global or not voice_client_global.is_connected():
            canal = after.channel
            voice_client_global = await canal.connect()
            print(f"🔊 Conectado ao canal {canal.name}")
            asyncio.create_task(loop_musica(voice_client_global))
            asyncio.create_task(verificar_volume_dinamico())

    # Saiu do canal alvo, verifica se vazio para desconectar
    if before.channel and before.channel.id == ID_CANAL_DE_VOZ:
        canal = before.channel
        if len([m for m in canal.members if not m.bot]) == 0:
            if voice_client_global and voice_client_global.is_connected():
                await voice_client_global.disconnect()
                print("👋 Desconectado do canal (vazio)")

async def loop_musica(voice_client):
    global ultima_musica_nome

    print("▶️ Loop de música iniciado")

    while voice_client.is_connected():
        try:
            # Checa se a jukebox está online
            if os.path.exists("estadojuke/online.txt"):
                with open("estadojuke/online.txt", "r") as f:
                    online = f.read().strip() == "True"
            else:
                online = False

            if not online:
                print("🛑 Jukebox offline — parando reprodução.")
                if voice_client.is_playing():
                    voice_client.stop()
                await asyncio.sleep(5)
                continue

            if not os.path.exists("musics.txt"):
                print("Arquivo musics.txt não encontrado, aguardando...")
                await asyncio.sleep(3)
                continue

            with open("musics.txt", "r") as file:
                linhas = file.readlines()
                if len(linhas) < 1:
                    print("Arquivo musics.txt vazio, aguardando...")
                    await asyncio.sleep(3)
                    continue

                caminho = linhas[0].strip()
                nome = linhas[1].strip() if len(linhas) > 1 else os.path.basename(caminho)

            if nome != ultima_musica_nome:
                print(f"Nova música detectada: {nome}")
                ultima_musica_nome = nome

            with open("estadojuke\\tempomusica.txt", "r") as file:
                timer = int(file.read())

            with open('estadojuke\\estadosom.txt', 'r') as file:
                volume_base = float(file.read())

            with open('estadoambiente\\portasala.txt', 'r') as file:
                porta_fechada = file.read().strip() == 'True'

            await tocar_musica_com_ajustes(voice_client, caminho, timer, volume_base, porta_fechada)

            await asyncio.sleep(10)

        except Exception as e:
            import traceback
            print(f"❗Erro no loop de música: {e}")
            traceback.print_exc()
            await asyncio.sleep(5)

async def verificar_volume_dinamico():
    global player, voice_client_global, ultimo_volume, ultima_porta_fechada

    while True:
        await asyncio.sleep(1)

        if voice_client_global is None or player is None or not voice_client_global.is_connected():
            continue

        try:
            with open("estadojuke\\estadosom.txt", "r") as file:
                volume_base = float(file.read())

            with open('estadoambiente\\portasala.txt', 'r') as file:
                porta_fechada = file.read().strip() == 'True'

            novo_volume = (volume_base / 2.5) / 2 if porta_fechada else (volume_base / 2.5) * 2

            # Reinicia a música só se o estado da porta (filtro) mudou
            if porta_fechada != ultima_porta_fechada:
                with open("musics.txt", "r") as file:
                    linhas = file.readlines()
                    caminho = linhas[0].strip()

                with open("estadojuke\\tempomusica.txt", "r") as file:
                    timer = int(file.read())

                print(f"♻️ Porta {'fechada' if porta_fechada else 'aberta'} detectada, reiniciando música com filtro.")
                await tocar_musica_com_ajustes(voice_client_global, caminho, timer, volume_base, porta_fechada)
                ultima_porta_fechada = porta_fechada
                ultimo_volume = novo_volume

            # Atualiza só o volume no player, sem reiniciar a música
            elif abs(novo_volume - ultimo_volume) > 0.01:
                player.volume = novo_volume
                print(f"🔊 Volume atualizado para {novo_volume:.2f}")
                ultimo_volume = novo_volume

        except Exception as e:
            print(f"⚠️ Erro ao atualizar volume dinamicamente: {e}")

@bot.command()
async def fechar(ctx):
    if ctx.author.voice and ctx.author.voice.channel and ctx.author.voice.channel.id == ID_CANAL_DE_VOZ:
        with open('estadoambiente\\portasala.txt', 'r') as file:
            cond = file.read().strip() == "True"

        if cond:
            await ctx.send("🚪 Porta da sala já está fechada.")
        else:
            await ctx.send("🚪 Fechando porta da sala.")

        with open('estadoambiente\\portasala.txt', 'w') as file:
            file.write("True")
    else:
        ...

@bot.command()
async def abrir(ctx):
    if ctx.author.voice and ctx.author.voice.channel and ctx.author.voice.channel.id == ID_CANAL_DE_VOZ:
        with open('estadoambiente\\portasala.txt', 'r') as file:
            cond = file.read().strip() == "True"

        if not cond:
            await ctx.send("🚪 Porta da sala já está aberta.")
        else:
            await ctx.send("🚪 Abrindo porta da sala.")

        with open('estadoambiente\\portasala.txt', 'w') as file:
            file.write("False")
    else:
        ...

bot.run(os.getenv('TOKKEN_SOM_SALA'))