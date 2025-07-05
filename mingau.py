import discord
import random
import time
from dotenv import load_dotenv
from os import getenv
from discord.ext import commands
from mingau_docs.mingaufrases import frases_mingau_chao, frases_mingau_mesa, frases_mingau_sofa, frases_mingau_varanda, frases_mingau_balcao, frases_mingau_mesa1, frases_mingau_mesa2, frases_mingau_mesa3, frases_mingau_ex_degrais, frases_chao_banheiro, frases_chao_corredor, frases_degrais_escadas, frases_mingau_ex_calcada, frases_mingau_ex_gramado
from utils_ids import CANAL_AUDIO_BANHEIRO, CANAL_AUDIO_CORREDOR, CANAL_AUDIO_ESCADARIA, CANAL_AUDIO_EXTERIOR, CANAL_AUDIO_JUKEBOX, CANAL_TELEVISAO, CANAL_TEXTO_BALCAO, CANAL_TEXTO_BANHEIRO, CANAL_TEXTO_CORREDOR, CANAL_TEXTO_ESCADARIA, CANAL_TEXTO_EXTERIOR, CANAL_TEXTO_MESA_1, CANAL_TEXTO_MESA_2, CANAL_TEXTO_MESA_3, CANAL_TEXTO_SALA, ID_SERVIDOR 

load_dotenv()

with open('mingau_docs/ultimocomodo.txt', 'r') as file:
        lis = [x.strip() for x in file.readlines()]
        comodo_antigo = int(lis[0])

mingau_inte = 0
locais = []
local_mingau = None

locais1 = ['mesa', 'chão', 'sofá', 'varanda']
locais2 = ['balcão']
locais3 = ['chão do banheiro']
locais4 = ['chão do corredor']
locais5 = ['degrais da escada da entrada', 'calçada', 'gramado']
locais6 = ['degrais da escada do bar']
locais7 = ['mesa 1']
locais8 = ['mesa 2']
locais9 = ['mesa 3']

FFMPEG_PATH = "C:\\Users\\Thalita\\Desktop\\Alessandro\\ffmpeg-7.1.1-essentials_build\\ffmpeg-7.1.1-essentials_build\\bin\\ffmpeg.exe"

LOCAIS = [CANAL_TEXTO_SALA, CANAL_TELEVISAO, CANAL_AUDIO_JUKEBOX, CANAL_TEXTO_BALCAO, CANAL_TEXTO_MESA_1, CANAL_TEXTO_MESA_2, CANAL_TEXTO_MESA_3,
CANAL_AUDIO_BANHEIRO, CANAL_TEXTO_BANHEIRO, CANAL_AUDIO_CORREDOR, CANAL_TEXTO_CORREDOR, CANAL_AUDIO_EXTERIOR, CANAL_TEXTO_EXTERIOR,
CANAL_AUDIO_ESCADARIA, CANAL_TEXTO_ESCADARIA
]

SALA = [CANAL_TEXTO_SALA, CANAL_TELEVISAO]
BAR = [CANAL_AUDIO_JUKEBOX, CANAL_TEXTO_BALCAO]
BANHEIRO = [CANAL_AUDIO_BANHEIRO, CANAL_TEXTO_BANHEIRO]
CORREDOR = [CANAL_AUDIO_CORREDOR, CANAL_TEXTO_CORREDOR]
EXTERIOR = [CANAL_AUDIO_EXTERIOR, CANAL_TEXTO_EXTERIOR]
ESCADA = [CANAL_AUDIO_ESCADARIA, CANAL_TEXTO_ESCADARIA]
MESA1 = [CANAL_TEXTO_MESA_1]
MESA2 = [CANAL_TEXTO_MESA_2]
MESA3 = [CANAL_TEXTO_MESA_3]

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True  # <- necessário para detectar entrada/saída de canais de voz

bot = commands.Bot(command_prefix='!', intents=intents)
# Substitua pelo ID do seu canal de texto

async def swtchcom(canal):
    global mingau_inte
    mingau_inte = 0
    novo_comodo_id = str(random.choice(LOCAIS))
    novo_comodo = bot.get_channel(int(novo_comodo_id))
    comodo_antigo = canal.name

    with open('mingau_docs/ultimocomodo.txt', 'w') as file:
        file.write('')

    with open('mingau_docs/ultimocomodo.txt', 'a') as file1:
        file1.write(str(novo_comodo_id)+'\n')
        file1.write(str(1365624579967680522)+'\n')

    await canal.send(f"Mingau saiu do seu cômodo e foi para {novo_comodo.name}")
    await novo_comodo.send(f"Mingau entrou em {novo_comodo.name}")

async def swtchLoc(local, canal):
    global local_mingau
    global mingau_inte
    local_mingau = random.choice(locais)
    await canal.send(f"Mingau saiu de {local}")
    #await canal.send(f"Mingau foi para {local_mingau}")
    mingau_inte = 0

@bot.command()
async def sala(ctx):
    
    with open('mingau_docs/ultimocomodo.txt', 'w') as file:
        file.write('')

    with open('mingau_docs/ultimocomodo.txt', 'a') as file1:
        file1.write(str(CANAL_TELEVISAO)+'\n')
        file1.write(str(1365624579967680522)+'\n')

@bot.command()
async def bar(ctx):

    with open('mingau_docs/ultimocomodo.txt', 'w') as file:
        file.write('')

    with open('mingau_docs/ultimocomodo.txt', 'a') as file2:
        file2.write(str(CANAL_AUDIO_JUKEBOX)+'\n')
        file2.write(str(1365624579967680522)+'\n')

@bot.command()
async def banheiro(ctx):
    
    with open('mingau_docs/ultimocomodo.txt', 'w') as file:
        file.write('')

    with open('mingau_docs/ultimocomodo.txt', 'a') as file1:
        file1.write(str(CANAL_AUDIO_BANHEIRO)+'\n')
        file1.write(str(1365624579967680522)+'\n')

@bot.command()
async def corredor(ctx):

    with open('mingau_docs/ultimocomodo.txt', 'w') as file:
        file.write('')

    with open('mingau_docs/ultimocomodo.txt', 'a') as file2:
        file2.write(str(CANAL_AUDIO_CORREDOR)+'\n')
        file2.write(str(1365624579967680522)+'\n')

@bot.command()
async def escada(ctx):
    
    with open('mingau_docs/ultimocomodo.txt', 'w') as file:
        file.write('')

    with open('mingau_docs/ultimocomodo.txt', 'a') as file1:
        file1.write(str(CANAL_AUDIO_ESCADARIA)+'\n')
        file1.write(str(1365624579967680522)+'\n')

@bot.command()
async def exterior(ctx):

    with open('mingau_docs/ultimocomodo.txt', 'w') as file:
        file.write('')

    with open('mingau_docs/ultimocomodo.txt', 'a') as file2:
        file2.write(str(CANAL_AUDIO_EXTERIOR)+'\n')
        file2.write(str(1365624579967680522)+'\n')

@bot.event
async def on_ready():
    print(f'Mingau está online como {bot.user}')

async def func(x=None):
    
    if x is None:
        return
    
    async def inter():
        return random.choice(x)
    return inter

@bot.event
async def on_message(message):
    global local_mingau
    global mingau_inte
    canal = message.channel

    with open('mingau_docs/ultimocomodo.txt', 'r') as file:
        listaa = [x.strip() for x in file.readlines()]
        CANAL_MINGAL_ID = int(listaa[0])
    
    if message.channel.id != CANAL_MINGAL_ID:
        await bot.process_commands(message)
        return

    locais.clear()
    
    if CANAL_MINGAL_ID in SALA:
        locais.extend(locais1)
    elif CANAL_MINGAL_ID in BAR:
        locais.extend(locais2)
    elif CANAL_MINGAL_ID in BANHEIRO:
        locais.extend(locais3)
    elif CANAL_MINGAL_ID in CORREDOR:
        locais.extend(locais4)
    elif CANAL_MINGAL_ID in EXTERIOR:
        locais.extend(locais5)
    elif CANAL_MINGAL_ID in ESCADA:
        locais.extend(locais6)
    elif CANAL_MINGAL_ID in MESA1:
        locais.extend(locais7)
    elif CANAL_MINGAL_ID in MESA2:
        locais.extend(locais8)
    elif CANAL_MINGAL_ID in MESA3:
        locais.extend(locais9)

    if not locais:
        await bot.process_commands(message)
        return

    if local_mingau not in locais:
        local_mingau = random.choice(locais)

    antigo_local = local_mingau

    if message.author == bot.user:
        return

    if message.content.lower() == getenv('SECRET_MINGAU'):
        await message.delete()
        if message.author.guild_permissions.manage_messages:
            quantidade = int(message.content.split()[1]) if len(message.content.split()) > 1 else 100
            await message.channel.send("Você ativou o poder oculto do Mingau...")
            await message.channel.send("Seus olhos começam a brilhar... todos perdem a memória de tudo o que já foi dito nessa sala")
            time.sleep(2)
            await message.channel.purge(limit=quantidade)
        else:
            await message.channel.send("Você não tem permissão para limpar as mensagens!", delete_after=5)

    if mingau_inte > 2 and random.randint(0, 1) == 1:
        await swtchLoc(antigo_local, canal)
        localiza_mingau = f"Mingau saiu de {antigo_local} para {local_mingau}" if antigo_local != local_mingau else "Mingau repentinamente olhou para a vidraça..."
        await message.channel.send(localiza_mingau)

    if message.content.lower() == getenv('COMANDO_MIAU'):
        await message.delete()
        mingau_inte += 1

        localpossies = {
            "mesa": await func(frases_mingau_mesa),
            "chão": await func(frases_mingau_chao),
            "sofá": await func(frases_mingau_sofa),
            "varanda": await func(frases_mingau_varanda),
            "balcão": await func(frases_mingau_balcao),
            "mesa 1": await func(frases_mingau_mesa1),
            "mesa 2": await func(frases_mingau_mesa2),
            "mesa 3": await func(frases_mingau_mesa3),
            "chão do banheiro": await func(frases_chao_banheiro),
            "chão do corredor": await func(frases_chao_corredor),
            "degrais da escada da entrada": await func(frases_mingau_ex_degrais),
            "calçada": await func(frases_mingau_ex_calcada),
            "gramado": await func(frases_mingau_ex_gramado),
            "degrais da escada do bar": await func(frases_degrais_escadas),
            "": await func(),
        }
        
        resposta_func = localpossies.get(local_mingau, await func())
        resposta = await resposta_func()

        if "miou" in resposta.lower():
            await message.channel.send(file=discord.File("mingau_miando.mp3"))

        await message.channel.send(resposta)
        
        if random.randint(0, random.randint(0, 9)) == 0:
            await swtchcom(canal)

    await bot.process_commands(message)

    

@bot.event
async def on_voice_state_update(member, before, after):
    if member.bot:
        return

    with open('mingau_docs/ultimocomodo.txt', 'r') as file:
        como = int(file.readline().strip())  # usa apenas a primeira linha, já limpa

    # Verifica se a mudança envolve o canal monitorado
    if not (before.channel and before.channel.id == como) and not (after.channel and after.channel.id == como):
        return

    canal_voz = after.channel or before.channel
    guild = member.guild

    # Se a pessoa entrou no canal monitorado
    if after.channel and after.channel.id == como and (not before.channel or before.channel.id != como):
        voice_client = guild.voice_client

        if not voice_client or not voice_client.is_connected():
            try:
                vc = await canal_voz.connect()
                print(f"Mingau entrou no canal de voz: {canal_voz.name}")

                # Toca som do mingau miando
                vc.play(discord.FFmpegPCMAudio("mingau_miando.mp3", executable=FFMPEG_PATH))
                
                # Envia texto no canal de texto
                canal_texto = discord.utils.get(guild.text_channels, id=CANAL_MINGAL_ID)
                if canal_texto:
                    await canal_texto.send("🐾 Mingau pulou no canal de voz quando alguém chegou!")
            except Exception as e:
                print(f"Erro ao conectar o Mingau: {e}")

    # Se Mingau está sozinho no canal
    voice_client = guild.voice_client
    if voice_client and voice_client.channel.id == como and len(voice_client.channel.members) == 1:
        await voice_client.disconnect()
        print("Mingau saiu do canal porque ficou sozinho.")

# Inicia o bot
TOKEN = getenv('TOKKEN_MINGAU')
bot.run(TOKEN)