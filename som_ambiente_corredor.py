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

# IDs
ID_CANAL_DE_VOZ = 1376065935235874948  # Corredor
ID_CANAL_TEXTO = 1221647823052906607   # Canal de texto do corredor

FFMPEG_PATH = (
    "C:\\Users\\Thalita\\Downloads\\ffmpeg-7.1.1-essentials_build"
    "\\ffmpeg-7.1.1-essentials_build\\bin\\ffmpeg.exe"
)

voice_client_global = None
player = None

@bot.event
async def on_ready():
    print(f"✅ Bot online como {bot.user}")

@bot.event
async def on_voice_state_update(member, before, after):
    global voice_client_global

    # Se alguém (não-bot) entrar no canal de voz do corredor, conecta e inicia loop
    if after.channel and after.channel.id == ID_CANAL_DE_VOZ and not member.bot:
        if not voice_client_global or not voice_client_global.is_connected():
            canal = after.channel
            voice_client_global = await canal.connect()
            print(f"🔊 Conectado a {canal.name}")
            asyncio.create_task(loop_musica(voice_client_global))
            asyncio.create_task(monitorar_volume())

    # Se o canal tiver ficado vazio de humanos, desconecta
    if before.channel and before.channel.id == ID_CANAL_DE_VOZ:
        canal = before.channel
        if len([m for m in canal.members if not m.bot]) == 0:
            if voice_client_global and voice_client_global.is_connected():
                await voice_client_global.disconnect()
                print("👋 Desconectado (canal vazio)")

async def loop_musica(voice_client):
    """
    Loop principal que verifica:
    1) Se a jukebox está online (online.txt == "True").
       - Se estiver offline, para a música (se estiver tocando) e mantém o bot conectado.
    2) Se há um arquivo musics.txt válido, lê caminho/nome.
    3) Toca o arquivo a partir de tempomusica.txt, com filtro lowpass e volume ajustado.
    4) Aguarda 2 segundos antes de repetir.
    """

    global player
    ultima_musica = ""

    while voice_client.is_connected():
        try:
            # 1) Verifica se a jukebox está online
            if os.path.exists("estadojuke/online.txt"):
                with open("estadojuke/online.txt", "r") as f:
                    onl = f.read().strip().lower() == "true"
            else:
                # Se não existir o arquivo, considera jukebox offline
                onl = False

            if not onl:
                # Se a jukebox estiver offline, apenas para o áudio (se estiver tocando)
                if voice_client.is_playing():
                    voice_client.stop()
                    print("🛑 Jukebox offline – parando reprodução.")
                await asyncio.sleep(1)
                continue

            # 2) Lê musics.txt
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

            # 3) Se houver mudança de música, reinicia
            if nome != ultima_musica:
                ultima_musica = nome

                # Para o áudio atual (se estiver tocando)
                if voice_client.is_playing():
                    voice_client.stop()

                # Lê o ponto de início salvo em tempomusica.txt (se existir)
                timer = 0
                try:
                    with open("estadojuke/tempomusica.txt", "r") as file:
                        timer = int(file.read().strip())
                except Exception:
                    # Se não conseguir ler, mantém timer=0
                    pass

                # 3.1) Decide filtro lowpass dependendo da porta do corredor
                estado_porta = "False"
                caminho_porta = "estadoambiente/porta_corredor.txt"
                if os.path.exists(caminho_porta):
                    with open(caminho_porta, "r") as file:
                        estado_porta = file.read().strip()

                if estado_porta == "True":
                    filtro = "-af lowpass=f=800,volume=1.2"   # porta fechada
                else:
                    filtro = "-af lowpass=f=18000,volume=1.2" # porta aberta

                # 3.2) Lê volume base em estadosom.txt
                volume = 0.2
                try:
                    with open("estadojuke/estadosom.txt", "r") as file:
                        volume = float(file.read())
                except Exception:
                    # Se não conseguir ler, mantém volume padrão 0.2
                    pass

                # Cria fonte FFmpeg com filtro e posição inicial
                source = FFmpegPCMAudio(
                    caminho,
                    executable=FFMPEG_PATH,
                    options=filtro,
                    before_options=f"-ss {timer}"
                )

                # Ajusta volume com base no valor lido e fator 1/2.8
                player = PCMVolumeTransformer(source, volume=volume / 2.8)
                voice_client.play(player)

                print(
                    f"▶️ Tocando '{nome}' ─ "
                    f"Volume {(volume / 2.8):.2f} ─ "
                    f"Filtro: {filtro} ─ "
                    f"Ponto inicial: {timer}s"
                )

            # 4) Espera 2 segundos antes de checar novamente
            await asyncio.sleep(2)

        except Exception as e:
            print(f"❗ Erro no loop de música: {e}")
            await asyncio.sleep(5)

async def verificar_volume_dinamico():
    """
    Task separada que roda em paralelo:
    - A cada segundo, lê estadosom.txt e porta_corredor.txt
    - Ajusta player.volume em tempo real (sem reiniciar música),
      multiplicando/dividindo conforme porta aberta/fechada.
    """
    global player, volume_atual

    caminho_volume = "estadojuke/estadosom.txt"
    caminho_porta  = "estadoambiente/porta_corredor.txt"

    while True:
        await asyncio.sleep(1)

        if player is None:
            continue

        try:
            # Lê volume base
            with open(caminho_volume, "r") as file:
                base_volume = float(file.read().strip())

            # Lê estado da porta
            porta_fechada = False
            if os.path.exists(caminho_porta):
                with open(caminho_porta, "r") as file:
                    porta_fechada = (file.read().strip() == "True")

            # Ajusta volume conforme porta
            if porta_fechada:
                novo_volume = (base_volume / 2) / 2.8
            else:
                novo_volume = (base_volume * 2) / 2.8

            # Se for diferente do atual, aplica
            if player.volume != novo_volume:
                player.volume = novo_volume
                print(f"🔊 Volume atualizado (corredor): {novo_volume:.2f}")

        except Exception as e:
            print(f"⚠️ Erro ao atualizar volume: {e}")

# ⬇️ Coloque seu token real aqui
bot.run(os.getenv('TOKKEN_SOM_CORREDOR'))
