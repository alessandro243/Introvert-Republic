import discord
from discord.ext import commands
from discord import FFmpegPCMAudio, PCMVolumeTransformer
import asyncio
import random
import datetime
from dotenv import load_dotenv
from os import getenv

load_dotenv()

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# IDs dos canais
TARGET_TEXT_CHANNEL_ID = 1365765011464523910  # <== troque para seu canal de texto
TARGET_VOICE_CHANNEL_ID = 1365765011464523910  # canal de voz

# Caminho para o executável do ffmpeg
FFMPEG_EXECUTABLE = "C:\\Users\\Thalita\\Downloads\\ffmpeg-7.1.1-essentials_build\\ffmpeg-7.1.1-essentials_build\\bin\\ffmpeg.exe"

# Estado global
dt_format = "%Y-%m-%d"
ja_choveu_hoje = False
fechado = False
estado_anterior = None
voice_client_global = None
player_global = None  # Armazena o player atual para controlar volume sem reiniciar

# Função que sorteia o intervalo diário

def randomizer():
    
    now = datetime.datetime.now()
    try:
        with open('estadosala\\hoje.txt', 'r') as f:
            hj = f.read().strip()
    except FileNotFoundError:
        hj = ''
    if hj != now.strftime(dt_format):
        with open('estadosala\\hoje.txt', 'w') as f:
            f.write(now.strftime(dt_format))
        bloco = random.randint(1, 3)  # 1=manhã,2=tarde,3=noite
        if bloco == 1:
            h = random.randint(0, 10)
            h2 = random.randint(h + 1, 11)  # garante que h2 > h
        elif bloco == 2:
            h = random.randint(12, 16)
            h2 = random.randint(h + 1, 17)
        else:
            h = random.randint(18, 22)
            h2 = random.randint(h + 1, 23)
        with open('estadosala\\horavaranda.txt', 'w') as f:
            f.write(f"{h}\n{h2}\n")
        cond = 'True' if random.choice([True, False]) else 'False'
        with open('estadosala\\numvaranda.txt', 'w') as f:
            f.write(cond)
        print(f"🎲 Novo intervalo: {h}h -> {h2}h, chuva={'sim' if cond=='True' else 'não'}")
    else:
        print('⏳ Mesmo dia: mantendo intervalo atual.')

# Coroutine que verifica o início da chuva periodicamente
async def verifica_chuva():
    chovendo = 0
    global ja_choveu_hoje
    while True:
        now = datetime.datetime.now()
        try:
            with open('estadosala\\hoje.txt', 'r') as f:
                hj = f.read().strip()
        except FileNotFoundError:
            hj = ''

        # Se é um novo dia, reseta flag e sorteia intervalo
        if hj != now.strftime(dt_format):
            ja_choveu_hoje = False
            # Atualiza data
            with open('estadosala\\hoje.txt', 'w') as f:
                f.write(now.strftime(dt_format))
            randomizer()

        try:
            with open('estadosala\\horavaranda.txt', 'r') as f:
                lines = f.readlines()
                h = int(lines[0].strip())
                h2 = int(lines[1].strip())
            with open('estadosala\\numvaranda.txt', 'r') as f:
                cond = f.read().strip() == 'True'
        except Exception:
            await asyncio.sleep(30)
            continue

        if cond and h <= now.hour <= h2 and not ja_choveu_hoje:
            if chovendo == 1:
                ...
            else:
                chovendo = 1
                message = f"🌧️ Começou a chover! Horário: {now.hour}h (intervalo {h}h-{h2}h)"
            print(message)
            target = bot.get_channel(TARGET_TEXT_CHANNEL_ID)
            if target:
                try:
                    await target.send(message)
                except discord.Forbidden:
                    print(f"❌ Sem permissão para enviar mensagem no canal {target.name} ({target.id})")
                except Exception as e:
                    print(f"❌ Erro ao enviar mensagem: {e}")
            ja_choveu_hoje = True

        await asyncio.sleep(30)

# Função para tocar áudio em loop de forma segura e controlando volume dinamicamente
async def tocar_em_loop(vc, volume_inicial):
    global player_global
    ultimo_audio = None

    while vc.is_connected():
        now = datetime.datetime.now()
        try:
            with open('estadosala\\horavaranda.txt', 'r') as f:
                lines = f.readlines()
                h = int(lines[0].strip())
                h2 = int(lines[1].strip())
            with open('estadosala\\numvaranda.txt', 'r') as f:
                cond = f.read().strip() == 'True'
        except Exception as e:
            print("⚠️ Erro na leitura de arquivos de chuva:", e)
            await asyncio.sleep(5)
            continue

        # Escolhe o áudio conforme a condição e horário
        AUDIO_FILE = 'chuva.mp3' if cond and h <= now.hour <= h2 else 'norain.mp3'

        # Se o áudio mudou em relação ao último, para o que está tocando para trocar
        if ultimo_audio != AUDIO_FILE and vc.is_playing():
            vc.stop()
            await asyncio.sleep(0.5)  # Dá um tempinho para parar antes de tocar outro

        # Prepara o áudio e o player
        source = FFmpegPCMAudio(AUDIO_FILE, executable=FFMPEG_EXECUTABLE)
        player = PCMVolumeTransformer(source, volume=volume_inicial)
        player_global = player  # pra controle externo

        # Se não estiver tocando, toca o áudio
        if not vc.is_playing():
            vc.play(player)
            print(f"[{now.strftime('%H:%M:%S')}] Tocando {AUDIO_FILE} com volume {player.volume}")

        ultimo_audio = AUDIO_FILE

        # Espera o áudio terminar para repetir o loop
        while vc.is_playing() and vc.is_connected():
            await asyncio.sleep(1)

@bot.event
async def on_ready():
    print(f"✅ Bot conectado como {bot.user}")
    randomizer()
    bot.loop.create_task(verifica_chuva())
    bot.loop.create_task(verifica_estado_da_porta())

@bot.event
async def on_voice_state_update(member, before, after):
    global voice_client_global
    if after.channel and after.channel.id == TARGET_VOICE_CHANNEL_ID:
        if not member.guild.voice_client:
            voice_client_global = await after.channel.connect()
            volume = 0.4 if fechado else 1.0
            bot.loop.create_task(tocar_em_loop(voice_client_global, volume))
    elif before.channel and before.channel.id == TARGET_VOICE_CHANNEL_ID:
        if len(before.channel.members) == 0 and before.channel.guild.voice_client:
            await before.channel.guild.voice_client.disconnect()
            voice_client_global = None

async def verifica_estado_da_porta():
    global estado_anterior, voice_client_global, player_global
    while True:
        await asyncio.sleep(1)
        if voice_client_global and voice_client_global.is_connected():
            if fechado != estado_anterior:
                estado_anterior = fechado
                novo_volume = 0.4 if fechado else 1.0
                print(f"🔊 Mudando volume para {novo_volume}")

                if player_global:
                    player_global.volume = novo_volume

@bot.command()
async def fecharvaranda(ctx):
    if not ctx.author.voice or not ctx.guild.voice_client:
        return

    if ctx.author.voice.channel != ctx.guild.voice_client.channel:
        return
    global fechado
    if ctx.author.voice and ctx.author.voice.channel and ctx.author.voice.channel.id == TARGET_VOICE_CHANNEL_ID:
        if fechado:
            await ctx.send("A vidraça da varanda já está fechada.")
        else:
            await ctx.send("Fechando a porta da varanda (volume baixo).")
            fechado = True

@bot.command()
async def abrirvaranda(ctx):
    if not ctx.author.voice or not ctx.guild.voice_client:
        return

    if ctx.author.voice.channel != ctx.guild.voice_client.channel:
        return
    global fechado
    if ctx.author.voice and ctx.author.voice.channel and ctx.author.voice.channel.id == TARGET_VOICE_CHANNEL_ID:
        if not fechado:
            await ctx.send("A vidraça da varanda já está aberta.")
        else:
            await ctx.send("Abrindo a vidraça da varanda (volume normal).")
            fechado = False

#função Di

@bot.command()
async def olhar(ctx):
    if not ctx.author.voice or not ctx.guild.voice_client:
        return

    if ctx.author.voice.channel != ctx.guild.voice_client.channel:
        return
    now = datetime.datetime.now()
    try:
        with open('estadosala\\horavaranda.txt', 'r') as f:
            lines = f.readlines()
            h = int(lines[0].strip())
            h2 = int(lines[1].strip())
        with open('estadosala\\numvaranda.txt', 'r') as f:
            cond = f.read().strip() == 'True'
    except Exception as e:
        await ctx.send("⚠️ Não consegui verificar o estado da varanda agora.")
        print("Erro ao ler arquivos para comando olhar:", e)
        return

    if cond and h <= now.hour <= h2:
        await ctx.send("🌧️ Você vê a noite chuvosa através da vidraça!")
    else:
        await ctx.send("Não está chovendo agora, é uma noite calma.")

#func test

# Novos comandos para controle manual da chuva e intervalo

@bot.command()
async def setchuva(ctx, estado: str):
    """Força o estado da chuva: use 'on' para chover e 'off' para parar a chuva"""
    global ja_choveu_hoje
    estado = estado.lower()
    if estado not in ['on', 'off']:
        await ctx.send("❌ Use `on` para ligar a chuva ou `off` para desligar.")
        return

    cond = 'True' if estado == 'on' else 'False'
    with open('estadosala\\numvaranda.txt', 'w') as f:
        f.write(cond)

    if estado == 'on':
        ja_choveu_hoje = True
    else:
        ja_choveu_hoje = False

    await ctx.send(f"🌧️ Estado da chuva atualizado para: {'chovendo' if cond == 'True' else 'sem chuva'}")

@bot.command()
async def setintervalo(ctx, inicio: int, fim: int):
    """Define manualmente o intervalo de chuva (horas inteiras de 0 a 23)"""
    if not (0 <= inicio < fim <= 23):
        await ctx.send("❌ Intervalo inválido. Use horas entre 0 e 23 e início < fim.")
        return

    with open('estadosala\\horavaranda.txt', 'w') as f:
        f.write

bot.run(getenv("TOKKEN_CHUVA_DA_SALA"))
