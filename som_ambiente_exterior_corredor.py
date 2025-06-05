import discord
import asyncio
import os

from discord.ext import commands
from discord import FFmpegPCMAudio, PCMVolumeTransformer

intents = discord.Intents.default()
intents.voice_states = True
intents.guilds = True
intents.members = True
intents.message_content = True

from dotenv import load_dotenv
load_dotenv()

bot = commands.Bot(command_prefix="!", intents=intents)

ID_CANAL_DE_VOZ = 1366035560249954315  # canal de voz corredor
FFMPEG_PATH = "C:\\Users\\Thalita\\Downloads\\ffmpeg-7.1.1-essentials_build\\ffmpeg-7.1.1-essentials_build\\bin\\ffmpeg.exe"

voice_client_global = None
player = None
volume_atual = None

@bot.event
async def on_ready():
    print(f"✅ Bot online como {bot.user}")
    # Inicia monitoramento do volume
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
    global player, volume_atual
    ultima_musica = ""

    while voice_client.is_connected():
        try:
            # Verifica se jukebox está ativa
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
                # Para a música, mas mantém conectado
                if voice_client.is_playing():
                    voice_client.stop()
                await asyncio.sleep(2)
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

                with open("estadojuke/tempomusica.txt", "r") as file:
                    timer = int(file.read())

                # Ler estado da porta
                estado_porta = "False"  # padrão aberta
                caminho_porta = "estadoambiente/porta_corredor.txt"
                if os.path.exists(caminho_porta):
                    with open(caminho_porta, "r") as file:
                        estado_porta = file.read().strip()

                # Define filtro ffmpeg com base na porta
                if estado_porta == "True":
                    filtro = "-af lowpass=f=800,volume=1.2"
                else:
                    filtro = "-af lowpass=f=18000,volume=1.2"

                # Ler volume base
                if os.path.exists("estadojuke/estadosom.txt"):
                    with open("estadojuke/estadosom.txt", "r") as file:
                        volume_atual = float(file.read())
                else:
                    volume_atual = 0.2

                source_ffmpeg = FFmpegPCMAudio(
                    caminho,
                    executable=FFMPEG_PATH,
                    options=filtro,
                    before_options=f'-ss {timer}'
                )

                player = PCMVolumeTransformer(source_ffmpeg, volume=volume_atual / 2.8)
                voice_client.play(player)

            await asyncio.sleep(2)

        except Exception as e:
            print(f"❗Erro no loop de música: {e}")
            await asyncio.sleep(5)

async def monitorar_volume():
    global player, volume_atual
    caminho_volume = "estadojuke/estadosom.txt"
    caminho_porta = "estadoambiente/porta_corredor.txt"

    while True:
        try:
            if os.path.exists(caminho_volume):
                with open(caminho_volume, "r") as file:
                    base_volume = float(file.read().strip())

                porta_fechada = False
                if os.path.exists(caminho_porta):
                    with open(caminho_porta, "r") as file:
                        porta_fechada = file.read().strip() == "True"

                # Ajuste do volume conforme porta
                novo_volume = base_volume / 2 if porta_fechada else base_volume * 2

                if novo_volume != volume_atual:
                    volume_atual = novo_volume
                    if player:
                        player.volume = volume_atual / 2.8
                        print(f"[Volume atualizado] Novo volume: {player.volume}")

        except Exception as e:
            print(f"Erro ao monitorar volume: {e}")

        await asyncio.sleep(1)

# Comandos para abrir/fechar porta
@bot.command()
async def fechar(ctx):
    if not ctx.author.voice or ctx.author.voice.channel is None:
        return
    if ctx.author.voice.channel.id != ID_CANAL_DE_VOZ:
        return

    caminho_porta = "estadoambiente/porta_corredor.txt"

    if os.path.exists(caminho_porta):
        with open(caminho_porta, "r") as file:
            cond = file.read().strip() == "True"

        if cond:
            await ctx.send("🚪 Porta para o corredor já está fechada.")
            return

    with open(caminho_porta, "w") as file:
        file.write("True")
    await ctx.send("🚪 Fechando porta do corredor.")

@bot.command()
async def abrir(ctx):
    if not ctx.author.voice or ctx.author.voice.channel is None:
        return
    if ctx.author.voice.channel.id != ID_CANAL_DE_VOZ:
        return

    caminho_porta = "estadoambiente/porta_corredor.txt"

    if os.path.exists(caminho_porta):
        with open(caminho_porta, "r") as file:
            cond = file.read().strip() == "True"

        if not cond:
            await ctx.send("🚪 Porta para o corredor já está aberta.")
            return

    with open(caminho_porta, "w") as file:
        file.write("False")
    await ctx.send("🚪 Abrindo porta para o corredor.")

# 🔒 Token real aqui
bot.run(os.getenv('TOKKEN_SOM_CORREDOR_EXTERIOR'))