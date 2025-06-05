import discord
from discord.ext import commands, tasks
import os
import asyncio
import random
import keyboard
import threading
import datetime
from discord import PCMVolumeTransformer
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKKEN_TELEVISAO')

FFMPEG_PATH = "C:\\Users\\Thalita\\Downloads\\ffmpeg-7.1.1-essentials_build\\ffmpeg-7.1.1-essentials_build\\bin\\ffmpeg.exe"

PASTAS = ['canal 01', 'canal 05', 'canal 92', 'canal 153', 'canal 223', 'canal 450']
ESTADO_DIR = 'estado'

DESCANSO_SEGUNDOS = 60  # tempo para desligar se ficar sozinho
ID_CANAL_VOZ_PERMITIDO = 1365765011464523910


intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Estado atual do bot
bot.estado_tocado = False
bot.canal_atual = None
bot.voice_client = None
bot.tarefa_tocando = None
bot.descanso_task = None
bot.descanso_contador = 0
player = None
ligado = False


def setup_arquivos_estado():
    os.makedirs(ESTADO_DIR, exist_ok=True)
    for pasta in PASTAS:
        caminho = os.path.join(ESTADO_DIR, f"{pasta}.txt")
        if not os.path.exists(caminho):
            with open(caminho, 'w', encoding='utf-8') as f:
                pass
    ultima_pasta_path = os.path.join(ESTADO_DIR, 'ultima_pasta.txt')
    if not os.path.exists(ultima_pasta_path):
        with open(ultima_pasta_path, 'w', encoding='utf-8') as f:
            pass

def get_estado_path(pasta):
    return os.path.join(ESTADO_DIR, f"{pasta}.txt")

def salvar_ultimo_arquivo(pasta, arquivo):
    with open(get_estado_path(pasta), 'w', encoding='utf-8') as f:
        f.write(arquivo)

def carregar_ultimo_arquivo(pasta):
    try:
        with open(get_estado_path(pasta), 'r', encoding='utf-8') as f:
            return f.read().strip()
    except FileNotFoundError:
        return None

def salvar_ultima_pasta(pasta):
    with open(os.path.join(ESTADO_DIR, "ultima_pasta.txt"), 'w', encoding='utf-8') as f:
        f.write(pasta)

def carregar_ultima_pasta():
    try:
        with open(os.path.join(ESTADO_DIR, "ultima_pasta.txt"), 'r', encoding='utf-8') as f:
            return f.read().strip()
    except FileNotFoundError:
        return None
    
async def toca_canal(canal_nome, ctx=None, canal_voz=None):
    global player

    if canal_nome not in PASTAS:
        
        if ctx:
            
            await ctx.send("Canal inválido!")
            
        return

    if not canal_voz and ctx:
        if not ctx.author.voice or not ctx.author.voice.channel:
            print('aqui2')
            await ctx.send("Você precisa estar em um canal de voz para eu entrar.")
            return
        canal_voz = ctx.author.voice.channel

    # Se já estiver em outro canal, desconecta para trocar
    if bot.voice_client and bot.voice_client.is_connected():
        print('aqui3')
        await bot.voice_client.disconnect()
    # Conecta no canal de voz novo
    try:
        ...
        bot.voice_client = await canal_voz.connect()
    except Exception as e:
        print('aqu4')        
        if ctx:
            print('aqui5')
            await ctx.send(f"Erro ao conectar no canal de voz: {e}")
        return
    
    filtro_tv = (
    "acompressor=threshold=-25dB:ratio=3:attack=100:release=800,"  # compressor mais suave e rápido
    "aphaser=in_gain=0.5:out_gain=0.8:delay=4,"                    # phaser mais perceptível
    "asetrate=44100*0.92,"                                        # menos pitch shift pra ficar menos distorcido
    "aresample=44100,"                                            # resample normal
    "adelay=0|15,"                                                # delay maior no canal direito, pra criar mais espaço
    "volume=1.3,"                                                 # volume um pouco mais baixo pra evitar clipping
    "bandreject=f=1200:w=250,"                                   # notch em 1200 Hz, faixa um pouco maior pra interferência
    "acrusher=bits=10:mode=log"                                  # menos crusher pra manter clareza
)  
    
    if canal_nome == 'canal 05':
        bot.estado_tocado = True
        bot.canal_atual = canal_nome
        salvar_ultima_pasta(canal_nome)

        arquivos = [f for f in os.listdir(canal_nome) if f.endswith('.mp3')]
        arquivos.sort()

        ultimo = carregar_ultimo_arquivo(canal_nome)

        # Loop para tocar arquivos em sequência e repetir depois que acabar tudo
        while bot.estado_tocado and bot.canal_atual == canal_nome:
            horario = canal06()
            if horario == 1:
                print('no if', arquivos[0])
                caminho = os.path.join(canal_nome, arquivos[0])
            else:
                print('no else', arquivos[1])
                caminho = os.path.join(canal_nome, arquivos[1])

            source = discord.FFmpegPCMAudio(
            caminho,
            executable=FFMPEG_PATH,
            options=f'-af "{filtro_tv}"'
    )
            player = PCMVolumeTransformer(source, 1)
            with open("estado\\estadomute.txt", "r") as file:
                mut = file.read().strip() == "True"

                if not mut:
                    with open("estado\\estadovolume.txt", "r") as file:
                        player.volume = float(file.read())
                else:
                    player.volume = 0
            
            bot.voice_client.play(
                player
)
            while bot.voice_client.is_playing():
                await asyncio.sleep(1)
                # Se a TV foi desligada ou canal mudou, para de tocar
                if not bot.estado_tocado or bot.canal_atual != canal_nome:
                    bot.voice_client.stop()
                    return

    else:
        bot.estado_tocado = True
    bot.canal_atual = canal_nome
    salvar_ultima_pasta(canal_nome)

    arquivos = [f for f in os.listdir(canal_nome) if f.endswith('.mp3')]
    arquivos.sort()

    ultimo = carregar_ultimo_arquivo(canal_nome)
    start_index = arquivos.index(ultimo) + 1 if ultimo in arquivos else 0

    # Loop para tocar arquivos em sequência e repetir depois que acabar tudo
    while bot.estado_tocado and bot.canal_atual == canal_nome:
        for i in range(start_index, len(arquivos)):
            arquivo = arquivos[i]
            caminho = os.path.join(canal_nome, arquivo)
            salvar_ultimo_arquivo(canal_nome, arquivo)
            
            arquiv = os.listdir("comerciais")
            vari = random.randint(0,2)
            p = random.choice(arquiv)
            mut = None
            source = discord.FFmpegPCMAudio(
                os.path.join("comerciais", p),
                executable=FFMPEG_PATH,
                options=f'-af "{filtro_tv}"'
    )
            
            player = PCMVolumeTransformer(source, 1)
            with open("estado\\estadomute.txt", "r") as file:
                mut = file.read().strip() == "True"

                if not mut:
                    with open("estado\\estadovolume.txt", "r") as file:
                        player.volume = float(file.read())
                else:
                    player.volume = 0

            if vari == 1:
                bot.voice_client.play(
                player
)   
            while bot.voice_client.is_playing():
                await asyncio.sleep(1)
                # Se a TV foi desligada ou canal mudou, para de tocar
                if not bot.estado_tocado or bot.canal_atual != canal_nome:
                    bot.voice_client.stop()
                    return

            source2 = discord.FFmpegPCMAudio(
            caminho,
            executable=FFMPEG_PATH,
            options=f'-af "{filtro_tv}"'
    )
            player = PCMVolumeTransformer(source2, 1)
            with open("estado\\estadomute.txt", "r") as file:
                mut = file.read().strip() == "True"

                if not mut:
                    with open("estado\\estadovolume.txt", "r") as file:
                        player.volume = float(file.read())
                else:
                    player.volume = 0
            
            bot.voice_client.play(
                player
)
            while bot.voice_client.is_playing():
                await asyncio.sleep(1)
                # Se a TV foi desligada ou canal mudou, para de tocar
                if not bot.estado_tocado or bot.canal_atual != canal_nome:
                    bot.voice_client.stop()
                    return
        start_index = 0  # reinicia do começo após acabar a lista

def escutar_teclas():
    canal = bot.get_channel(1365765011464523910)
    hook_container = [None]  # Lista para armazenar o hook_id

    def ao_apertar(event):
        
        if event.name == '-':
            print("Apertou -")
            player.volume = max(0.0, player.volume - 0.1)

            with open("estado\\estadomute.txt", "r") as file:
                estadomut = file.read().strip() == 'True'
            
            if estadomut:
                with open("estado\\estadomute.txt", "w") as file:
                    file.write("False")

        elif event.name == '+':
            print("Apertou +")
            player.volume = max(0.0, player.volume + 0.1)

            with open("estado\\estadomute.txt", "r") as file:
                estadomut = file.read().strip() == 'True'
            
            if estadomut:
                with open("estado\\estadomute.txt", "w") as file:
                    file.write("False")

        elif event.name == 'enter':
            asyncio.run_coroutine_threadsafe(
                canal.send(f"Volume: {int(player.volume * 10)}"), bot.loop
            )
            keyboard.unhook(hook_container[0])  # Usa o hook armazenado
            return False

    hook_container[0] = keyboard.on_press(ao_apertar)
    keyboard.wait("enter")

    with open("estado\\estadovolume.txt", "w") as file:
        if player.volume <10:
            file.write(str(player.volume))
        
        else:
            file.write(str(player.volume))

# Dentro do seu bot, em algum momento:
@bot.command()
async def mute(ctx):
    if not ctx.author.voice or not ctx.guild.voice_client:
        #await ctx.send("❌ Você ou o bot não estão em um canal de voz.")
        return

    # Verifica se estão no MESMO canal
    if ctx.author.voice.channel != ctx.guild.voice_client.channel:
        #await ctx.send("⚠️ Você precisa estar no mesmo canal de voz que o bot para usar esse comando.")
        return
    global player

    # Lê estado atual de mute
    with open("estado\\estadomute.txt", "r") as file:
        estadomute = file.read().strip() == 'True'

    # Se estava mutado → DESMUTAR
    if estadomute:
        # Lê volume salvo
        with open("estado\\estadovolume.txt", "r") as file:
            estadovol = float(file.read())

        player.volume = estadovol
        with open("estado\\estadomute.txt", "w") as file:
            file.write("False")

    # Se não estava mutado → MUTAR
    else:
        # Salva o volume atual antes de mutar
        with open("estado\\estadovolume.txt", "w") as file:
            file.write(str(player.volume))

        player.volume = 0
        with open("estado\\estadomute.txt", "w") as file:
            file.write("True")

    await ctx.send(f'Volume: {int(player.volume * 10)}')
    print(player.volume)


@bot.command()
async def volume(ctx):
    global player, ligado

    # IDs dos canais de texto permitidos para comando
    canais_autorizados = {
        1365765011464523910   # canal 4
    }

    if ctx.channel.id not in canais_autorizados:
        #await ctx.send("⚠️ Este canal não está autorizado a ajustar o volume.")
        return

    # Verifica se o autor está em canal de voz
    if not ctx.author.voice:
        #await ctx.send("⚠️ Você precisa estar em algum canal de voz.")
        return

    # Verifica se o bot está tocando algo
    if not ligado:
        #await ctx.send("⚠️ A jukebox está desligada.")
        return

    if not player or not isinstance(player, PCMVolumeTransformer):
        await ctx.send("⚠️ O player atual não suporta ajuste de volume.")
        return

    await ctx.send("🎛️ Modo de ajuste de volume ativado. Envie mensagens com + para aumentar, - para diminuir, ou enter para sair.")

    def check(m):
        return (
            m.author == ctx.author and
            m.channel.id == ctx.channel.id and
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
            ajuste = (mais - menos) * 0.05  # Ajusta 5% por + ou -

            player.volume = min(1.0, max(0.0, player.volume + ajuste))

            with open("estado\\estadomute.txt", "r", encoding="utf-8") as file:
                estadomut = file.read().strip() == 'True'

            if estadomut:
                with open("estado\\estadomute.txt", "w", encoding="utf-8") as file:
                    file.write("False")

            with open("estado\\estadovolume.txt", "w", encoding="utf-8") as file:
                file.write(str(player.volume))

            await ctx.send(f"🔊 Volume ajustado para {int(player.volume * 100)}%")

        except asyncio.TimeoutError:
            await ctx.send("⏳ Tempo esgotado. Saindo do modo de ajuste de volume.")
            break

@bot.command()
async def ligar(ctx):
    print(123)

    canal_permitido_id = 1365765011464523910

    # Verifica se o usuário está em um canal de voz
    if not ctx.author.voice:
        print(1234)
        await ctx.send("❌ Você precisa estar em um canal de voz para ligar a TV.")
        return

    canal_usuario = ctx.author.voice.channel

    # Verifica se o canal do usuário é o canal permitido
    if canal_usuario.id != canal_permitido_id:
        print(12345)
        await ctx.send("⚠️ Você precisa estar conectado no canal de voz correto para ligar a TV.")
        return

    # Se o bot ainda não está conectado, conecta ao canal do usuário
    if not ctx.guild.voice_client:
        print('ooooooo')
        #await canal_usuario.connect()
        

    global ligado
    ligado = True

    # Se a TV já estiver ligada
    if bot.estado_tocado:
        await ctx.send("A TV já está ligada.")
        return

    # Carrega o último canal
    canal = carregar_ultima_pasta()
    if canal not in PASTAS:
        canal = 'canal 01'

    await ctx.send(f"Ligando TV.")
    bot.tarefa_tocando = asyncio.create_task(toca_canal(canal, ctx))
    bot.estado_tocado = True
    bot.canal_atual = canal

@bot.command()
async def desligar(ctx):
    if not ctx.author.voice or not ctx.guild.voice_client:
        print('aqui')
        #await ctx.send("❌ Você ou o bot não estão em um canal de voz.")
        return

    # Verifica se estão no MESMO canal
    if ctx.author.voice.channel != ctx.guild.voice_client.channel:
        print('aqui')
        #await ctx.send("⚠️ Você precisa estar no mesmo canal de voz que o bot para usar esse comando.")
        return
    canal_permitido = bot.get_channel(1365765011464523910)
    
    global ligado
    ligado = False

    if not ctx.author.voice or ctx.author.voice.channel != canal_permitido:
        await ctx.send("Você precisa estar conectado no canal de voz correto para desligar a TV.")
        return
    
    if not bot.estado_tocado:
        await ctx.send("A TV já está desligada.")
        return

    bot.estado_tocado = False
    if bot.voice_client and bot.voice_client.is_connected():
        await bot.voice_client.disconnect()
        bot.voice_client = None

    if bot.tarefa_tocando:
        bot.tarefa_tocando.cancel()
        bot.tarefa_tocando = None

    await ctx.send("TV desligada.")

@bot.command()
async def trocar(ctx, *, canal_nome: str):
    await ctx.message.delete()

    canal_nome = canal_nome.lower().strip()
    if not ctx.author.voice or not ctx.guild.voice_client:
        #await ctx.send("❌ Você ou o bot não estão em um canal de voz.")
        return

    # Verifica se estão no MESMO canal
    if ctx.author.voice.channel != ctx.guild.voice_client.channel:
        #await ctx.send("⚠️ Você precisa estar no mesmo canal de voz que o bot para usar esse comando.")
        return
    # Ajuste para aceitar "canal01", "canal 01", "canal_01" etc
    for p in PASTAS:
        if canal_nome.replace(" ", "") == p.replace(" ", ""):
            canal_nome = p
            break

    if canal_nome not in PASTAS:
        await ctx.send(f"Canal inválido.")
        return

    if not bot.estado_tocado:
        await ctx.send("A TV está desligada. Use !ligar para ligar.")
        return

    if not ctx.author.voice or not ctx.author.voice.channel:
        await ctx.send("Você precisa estar em um canal de voz para trocar o canal.")
        return

    bot.estado_tocado = False  # para a reprodução atual
    if bot.tarefa_tocando:
        bot.tarefa_tocando.cancel()

    await asyncio.sleep(1)  # deixa a tarefa parar

    # Liga no novo canal
    bot.tarefa_tocando = asyncio.create_task(toca_canal(canal_nome, ctx, ctx.author.voice.channel))
    bot.estado_tocado = True
    bot.canal_atual = canal_nome
    await ctx.send(f"Trocando para o {canal_nome}...")
    
    mensagens = [msg async for msg in ctx.channel.history(limit=1)]
    for msg in mensagens:
        try:
            await msg.delete()
        except:
            pass

@bot.event
async def on_voice_state_update(member, before, after):
    # Ignora eventos do bot
    if member == bot.user:
        return

    if not bot.voice_client or not bot.voice_client.is_connected():
        return

    # Se o bot está em canal e ficou sozinho, começa a contar descanso
    vc = bot.voice_client
    canal = vc.channel

    # Verifica se o bot está sozinho no canal de voz
    if len(canal.members) == 1 and canal.members[0] == bot.user:
        # Começa contador se não estiver ativo
        if not bot.descanso_task or bot.descanso_task.done():
            bot.descanso_contador = 0
            bot.descanso_task = asyncio.create_task(contar_descanso())
    else:
        # Se tiver alguém, cancela o descanso
        if bot.descanso_task and not bot.descanso_task.done():
            bot.descanso_task.cancel()

async def contar_descanso():
    try:
        while bot.descanso_contador < DESCANSO_SEGUNDOS:
            await asyncio.sleep(1)
            bot.descanso_contador += 1
        # Tempo esgotado, desliga TV
        if bot.estado_tocado:
            canal = bot.canal_atual
            bot.estado_tocado = False
            if bot.voice_client and bot.voice_client.is_connected():
                await bot.voice_client.disconnect()
                bot.voice_client = None
            if bot.tarefa_tocando:
                bot.tarefa_tocando.cancel()
                bot.tarefa_tocando = None
            print(f"TV desligada automaticamente por ficar sozinha no canal ({canal}).")
    except asyncio.CancelledError:
        pass

@bot.event
async def on_ready():
    setup_arquivos_estado()
    print(f"Bot conectado como {bot.user}")

def canal06():
    agora = datetime.datetime.now()
    
    if agora.hour == 8 and 2 <= agora.minute <= 3:
        return 1
    
    return 0

bot.run(TOKEN)
