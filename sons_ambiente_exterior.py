import discord
from discord.ext import commands
from dotenv import load_dotenv
from os import getenv

load_dotenv()

intents = discord.Intents.default()
intents.members = True  # Necessário para capturar eventos de membros
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Substitua com o ID do canal que você deseja monitorar
TARGET_CHANNEL_ID = 1366035560249954315  # ID do seu canal de voz
AUDIO_FILE = "chuva.mp3"  # Caminho do arquivo de áudio que você quer tocar
FFMPEG_EXECUTABLE = "C:\\Users\\Thalita\\Downloads\\ffmpeg-7.1.1-essentials_build\\ffmpeg-7.1.1-essentials_build\\bin\\ffmpeg.exe"

@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}")

@bot.event
async def on_voice_state_update(member, before, after):
    if after.channel is not None:
        print(f"{member.name} entrou no canal {after.channel.name}")

        if after.channel.id == TARGET_CHANNEL_ID:
            # Se o bot não está conectado, ele se conecta
            if member.guild.voice_client is None:
                channel = after.channel
                voice_client = await channel.connect()

                # Função para tocar o áudio em loop
                def play_audio_loop(error=None):
                    if not voice_client.is_connected():
                        return
                    source = discord.FFmpegPCMAudio(AUDIO_FILE, executable=FFMPEG_EXECUTABLE)
                    voice_client.play(source, after=play_audio_loop)

                # Começar a tocar o áudio
                if not voice_client.is_playing():
                    play_audio_loop()
                    print(f"Tocando áudio {AUDIO_FILE} em loop")

    elif before.channel is not None:
        # Se o canal ficou vazio, desconecta o bot
        if len(before.channel.members) == 0 and before.channel.guild.voice_client:
            print(f"O canal {before.channel.name} está vazio, desconectando o bot.")
            await before.channel.guild.voice_client.disconnect()

bot.run(getenv('TOKKEN_SOM_EXTERIOR'))