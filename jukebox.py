import discord
import os
import random
import asyncio
import keyboard
from discord.ext import commands
from discord import FFmpegPCMAudio, PCMVolumeTransformer
import threading
import time
from dotenv import load_dotenv
from os import getenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
intents.guilds = True
vari = False

intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

CANAL_TEXTO_AUTORIZADO = 1354311386100011078
FFMPEG_PATH = "C:\\Users\\Thalita\\Downloads\\ffmpeg-7.1.1-essentials_build\\ffmpeg-7.1.1-essentials_build\\bin\\ffmpeg.exe"

voice_client_global = None
play_task = None
current_playlist = []
playlist_index = 0
paused = False
ligado = True
player = None
v = 0
timer_task = None
cond = None

async def tocar_proxima(ctx):

    with open("estadojuke\pause.txt", 'w') as fi:
        fi.write('False')
    
    print("⚠️ tocar_proxima foi chamada")
    
    
    global voice_client_global, current_playlist, playlist_index, paused, timer_task, vari, v, player, cond

    print('oi')
    if v > 0:
        v=0
        vari = True

    with open('estadojuke\\tempomusica.txt', 'w') as file:
        file.write(str(0))
    
    if not current_playlist:
        await ctx.send("A playlist está vazia.")
        if voice_client_global and voice_client_global.is_connected():
            await voice_client_global.disconnect()
        return

    if playlist_index >= len(current_playlist):
        playlist_index = 0  # Reinicia a playlist

    musica = current_playlist[playlist_index]
    caminho_completo = musica

    with open("musics.txt", "w") as file:

        if cond == True:
            return
        
        file.write(caminho_completo + '\n')
        file.write(os.path.basename(caminho_completo) + '\n')
    
    with open('estadojuke\\estadosom.txt', 'r') as file:
        volum = float(file.read())

    source = FFmpegPCMAudio(caminho_completo, executable=FFMPEG_PATH)
    source = PCMVolumeTransformer(source, volume=volum)

    player = source  # Atualiza o global player para o objeto atual que será tocado

    voice_client_global.play(player, after=lambda e: asyncio.run_coroutine_threadsafe(tocar_proxima(ctx), bot.loop))
    x = await ctx.send(f"Tocando agora: {os.path.basename(musica)}")
    playlist_index += 1
    v += 1
    #await ctx.message.delete()

async def iniciar_playlist(ctx, pasta):
    global current_playlist, playlist_index, paused, cond
    cond = False

    with open('estadojuke\\audiodiferente.txt', 'w') as file:
        file.write('False')

    # Verifique se a pasta existe
    if not os.path.exists(pasta):
        await ctx.send(f"❗ A pasta '{pasta}' não existe.")
        return

    arquivos = [f for f in os.listdir(pasta) if f.endswith((".mp3", ".m4a", ".wav"))]
    print(f"🎵 Arquivos encontrados na pasta '{pasta}': {arquivos}")

    if not arquivos:
        await ctx.send("❗ Nenhuma música encontrada na pasta.")
        return

    random.shuffle(arquivos)
    current_playlist = [os.path.join(pasta, musica) for musica in arquivos]
    playlist_index = 0
    paused = False

    await tocar_proxima(ctx)

@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}")

@bot.event
async def on_message(message):
    global voice_client_global, play_task, paused, playlist_index

    if message.author == bot.user:
        return

    if message.channel.id != CANAL_TEXTO_AUTORIZADO:
        return

    if message.content.startswith("!play"):
        if not message.author.voice:
            await message.channel.send("Você precisa estar em um canal de voz para usar este comando.")
            return

        # Se o bot já estiver conectado, parar e desconectar para "resetar" a voz
        if voice_client_global and voice_client_global.is_connected():
            voice_client_global.stop()
            await voice_client_global.disconnect()
            voice_client_global = None

        # Cancelar tarefa de play atual, se existir
        if play_task and not play_task.done():
            play_task.cancel()

        # Reconectar no canal do usuário
        canal = message.author.voice.channel
        voice_client_global = await canal.connect()
        with open('estadojuke\\jukeconect.txt', 'w') as f:
            f.write('False')

        # Escolher pasta baseado no comando
        pasta = None
        if message.content.startswith(getenv('PLAYLIST1')):
            pasta = 'jp_'
        elif message.content.startswith(getenv('PLAYLIST2')):
            pasta = 'ro_'
        elif message.content.startswith(getenv('PLAYLIST3')):
            pasta = 'a_'
        elif message.content.startswith(getenv('PLAYLIST4')):
            pasta = 'sy_'
        elif message.content.startswith(getenv('PLAYLIST5')):
            pasta = 'ch_'
        elif message.content.startswith(getenv('PLAYLIST6')):
            pasta = 'vi_'
        elif message.content.startswith(getenv('PLAYLIST7')):
            pasta = 'mp_'
        elif message.content.startswith(getenv('PLAYLIST8')):
            pasta = 'lo_'
        elif message.content.startswith(getenv('PLAYLIST9')):
            pasta = 'old_'


        if pasta:
            ctx = message.channel
            play_task = asyncio.create_task(iniciar_playlist(ctx, pasta))

            asyncio.create_task(atualiza_tempo(voice_client_global))
        else:
            await message.channel.send("Comando inválido.")

    elif message.content.startswith("!stop"):
        if voice_client_global:
            voice_client_global.stop()
            await voice_client_global.disconnect()
            voice_client_global = None
            await message.channel.send("Reprodução parada e desconectado.")
            with open('estadojuke\\jukeconect.txt', 'w') as f:
                f.write('True')

    elif message.content.startswith("!pause"):
        if voice_client_global and voice_client_global.is_playing():
            voice_client_global.pause()
            paused = True

            with open('estadojuke\pause.txt', 'w') as f:
                f.write('True')

            await message.channel.send("Música pausada.")

    elif message.content.startswith("!resume"):
        if voice_client_global and paused:
            with open("estadojuke\pause.txt", 'w') as fi:
                fi.write('False')
            
            with open("estadojuke\\tempomusica.txt", 'r') as fi:
                timer = int(fi.read())

            voice_client_global.resume()
            asyncio.create_task(atualiza_tempo(voice_client_global, timer))
            paused = False
            await message.channel.send("Música retomada.")

    elif message.content.startswith("!skip"):
        if voice_client_global and voice_client_global.is_playing():
            voice_client_global.stop()
            await message.channel.send("Pulando para a próxima música...")

    await bot.process_commands(message)

def escutar_teclas():
    canal = bot.get_channel(1354311386100011078)
    if canal is None:
        print("Erro: canal não encontrado!")
        return

    hook_container = [None]  # Lista para armazenar o hook_id

    def ao_apertar(event):
        print(f"Tecla pressionada: {event.name}")
        
        global player
        if player is None:
            print("Aviso: player está None no momento.")
            return

        if event.name == '-':
            print("Apertou -")
            player.volume = max(0.0, player.volume - 0.05)

            with open("estado\\estadomute.txt", "r") as file:
                estadomut = file.read().strip() == 'True'
            
            if estadomut:
                with open("estado\\estadomute.txt", "w") as file:
                    file.write("False")
            
            with open("estadojuke\\estadosom.txt", "w") as file:
                file.write(str(player.volume))

        elif event.name == '+':
            print("Apertou +")
            player.volume = min(1.0, player.volume + 0.05)  # Limita a 1.0 máximo
            

            with open("estado\\estadomute.txt", "r") as file:
                estadomut = file.read().strip() == 'True'

            
            if estadomut:
                with open("estado\\estadomute.txt", "w") as file:
                    file.write("False")

            with open("estadojuke\\estadosom.txt", "w") as file:
                file.write(str(player.volume))

        elif event.name == 'enter':
            print("Apertou enter - enviando mensagem e desregistrando hook")
            asyncio.run_coroutine_threadsafe(
                canal.send(f"Volume: {int(player.volume * 10)}"), bot.loop
            )
            keyboard.unhook(hook_container[0])  # Desregistra o hook
            return False  # Para o keyboard.wait

    hook_container[0] = keyboard.on_press(ao_apertar)
    print("Esperando tecla 'enter' para sair...")
    keyboard.wait("enter")
    print("Saiu do keyboard.wait")

    print(f"Volume salvo: {player.volume}")

@bot.command()
async def teste(ctx):
    await ctx.send(f"Comando funcionando no canal {ctx.channel.name} ({ctx.channel.id})!")

@bot.command()
async def volume(ctx):
    global player, ligado

    print(f"Comando chamado em canal: {ctx.channel.id}")
    print(f"Autor: {ctx.author}")
    print(f"Está em canal de voz? {ctx.author.voice is not None}")
    print(f"Bot está ligado? {ligado}")

    # IDs dos canais de texto permitidos
    canais_autorizados = {
        1354312920569221211,  # canal 2
        1354313052060909598,  # canal 3
        1354313099640963092,
        1354311386100011078   # canal 4
    }

    if ctx.channel.id not in canais_autorizados:
        await ctx.send("⚠️ Este canal não está autorizado a ajustar o volume.")
        return

    # Verifica se a pessoa está em algum canal de voz (opcional)
    if not ctx.author.voice:
        await ctx.send("⚠️ Você precisa estar em algum canal de voz.")
        return

    # Verifica se o bot está tocando algo
    if not ligado:
        await ctx.send("⚠️ A jukebox está desligada.")
        return

    from discord import PCMVolumeTransformer
    if not isinstance(player, PCMVolumeTransformer):
        await ctx.send("⚠️ O player atual não suporta ajuste de volume.")
        return

    await ctx.send("🎛️ Modo de ajuste de volume ativado. Envie mensagens com `+` para aumentar, `-` para diminuir, ou `enter` para sair.")

    def check(m):
        return (
            m.author == ctx.author and
            m.channel.id in canais_autorizados and
            ('+' in m.content or '-' in m.content or m.content.lower() == 'enter')
        )

    while True:
        try:
            msg = await bot.wait_for('message', timeout=60.0, check=check)

            if msg.content.lower() == 'enter':
                await ctx.send(f"✅ Ajuste finalizado com volume em {int(player.volume * 100)}%")
                break

            mais = msg.content.count('+')
            menos = msg.content.count('-')
            ajuste = (mais - menos) * 0.05

            player.volume = min(1.0, max(0.0, player.volume + ajuste))

            with open("estado\\estadomute.txt", "r", encoding="utf-8") as file:
                estadomut = file.read().strip() == 'True'

            if estadomut:
                with open("estado\\estadomute.txt", "w", encoding="utf-8") as file:
                    file.write("False")

            with open("estadojuke\\estadosom.txt", "w", encoding="utf-8") as file:
                file.write(str(player.volume))

            await ctx.send(f"🔊 Volume ajustado para {int(player.volume * 100)}%")

        except asyncio.TimeoutError:
            await ctx.send("⏳ Tempo esgotado. Saindo do modo de ajuste de volume.")
            break



async def atualiza_tempo(voice_client, tempo=None):
    global voice_client_global, vari, timer_task
    
    if voice_client == None:
        voice_client = voice_client_global
    
    if tempo == None:
        tempo_passado = 0
    else:
        tempo_passado = tempo

    while voice_client.is_connected() and voice_client.is_playing():
        print('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa', tempo_passado, type(tempo_passado))
        tempo_passado += 1  # ou calcule o tempo real
        with open("estadojuke\\tempomusica.txt", "w") as f:
            f.write(str(tempo_passado))
        await asyncio.sleep(1)
        print(vari)
        if vari:
            print('vari no if: ', vari)
            vari = False
            with open("estadojuke\\tempomusica.txt", "w") as f:
                f.write(str(0))
            global timer_task

    # Se já existe timer rodando, cancela ele
            if timer_task and not timer_task.done():
                timer_task.cancel()
            print('oie')

    # cria e inicia um novo timer para contar a música atual
            timer_task = asyncio.create_task(atualiza_tempo(voice_client_global))
            break

@bot.command()
async def fita123(ctx):
    
    if not ctx.author.voice or not ctx.guild.voice_client:
        #await ctx.send("❌ Você ou o bot não estão em um canal de voz.")
        return

    # Verifica se estão no MESMO canal
    if ctx.author.voice.channel != ctx.guild.voice_client.channel:
        #await ctx.send("⚠️ Você precisa estar no mesmo canal de voz que o bot para usar esse comando.")
        return
    global voice_client_global, play_task, paused, cond, player
    caminho = ''
    arq = ''

    for x in os.listdir('audios_secretos'):
        if x == '0Rádio Libertadora (Legenda) - Carlos Marighella.mp3':
            arq = x
            caminho = os.path.join('audios_secretos', x)

    #with open('estadojuke\\nome.txt', 'w') as file:
        #file.write(caminho)

    if not ctx.author.voice:
        await ctx.send("Você precisa estar em um canal de voz para usar esse comando.")
        return

    with open('estadojuke\\estadosom.txt', 'r') as file:
        volum = float(file.read())

    if voice_client_global and voice_client_global.is_connected():
        voice_client_global.stop()
        await voice_client_global.disconnect()
        voice_client_global = None

    canal = ctx.author.voice.channel
    voice_client_global = await canal.connect()
    with open('estadojuke\\jukeconect.txt', 'w') as f:
            f.write('False')

    if play_task and not play_task.done():
        play_task.cancel()

    paused = False
    cond = True

    with open('estadojuke\\audiodiferente.txt', 'w') as file:
        file.write('True')

    # Função para atualizar o cronômetro
    async def cronometro_loop():
        tempo = 0
        while True:
            with open("estadojuke\\cronometro.txt", "w") as f:
                f.write(str(tempo))
            await asyncio.sleep(1)
            tempo += 1

    # Inicia cronômetro paralelo
    cronometro_task = asyncio.create_task(cronometro_loop())

    # Reproduz os 3 áudios iniciais
    for i in range(3):
        if i != 2:
            source = FFmpegPCMAudio("tec_retro.mp3", executable=FFMPEG_PATH)
        else:
            source = FFmpegPCMAudio("long_beep_retro.mp3", executable=FFMPEG_PATH)

        player = PCMVolumeTransformer(source, volume=volum)

        if voice_client_global.is_playing():
            voice_client_global.stop()

        voice_client_global.play(player)

        

        while voice_client_global.is_playing():
            await asyncio.sleep(1)

    # Atualiza o estado para avisar que o áudio diferente terminou

    # Começa o áudio "chiado"
    source = FFmpegPCMAudio(caminho, executable=FFMPEG_PATH)
    player = PCMVolumeTransformer(source, volume=volum)
    voice_client_global.play(player)

    await ctx.send(f"Tocando áudio especial: chiado.mp3")
    with open('musics.txt', 'w') as file:
        file.write(caminho + '\n')
        file.write(os.path.basename(caminho) + '\n')

    # Espera o chiado terminar
    while voice_client_global.is_playing():
        await asyncio.sleep(1)

    # Para o cronômetro ao fim do áudio
    cronometro_task.cancel()
    with open("estadojuke\\cronometro.txt", "w") as f:
        f.write("0")  # reseta ao fim (opcional)
    #await ctx.message.delete()
    
bot.run(getenv('TOKKEN_JUKEBOX'))