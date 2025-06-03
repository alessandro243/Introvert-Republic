import discord
import random
import time
from dotenv import load_dotenv
from os import getenv

load_dotenv()

mingau_inte = 0
locais = ["mesa", "chão", "varanda", "sofá"]
local_mingau = locais[random.randint(0, 3)]

def swtchLoc(local):
    global local_mingau
    global mingau_inte
    local_mingau = locais[random.randint(0, 1)]
    print("Mingau saiu de ", local)
    print("Mingau foi para ", local_mingau)
    mingau_inte = 0

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True  # <- necessário para detectar entrada/saída de canais de voz

client = discord.Client(intents=intents)

CANAL_MINGAL_ID = 1365765011464523910  # Substitua pelo ID do seu canal de texto

frases_mingau_mesa = [
    "Mingau está a ronronar...",
    "Mingau derrubou alguma coisa da mesa e está olhando pra você, aparentemente foi de propósito.",
    "Mingau deitou e está olhando pra você.",
    "Mingau está caçando um inseto nas flores do vaso.",
    "Mingau está olhando através do vidro.",
    "Mingau está afiando as unhas na mesa.",
    "Mingau miou."
]

frases_mingau_chao = [
    "Mingau está no chão.",
    "Mingau está rolando no chão.",
    "Mingau está brincando com um joystick.",
    "Mingau miou.",
    "Mingau está olhando para você.",
    "Mingau inalou fumaça e espirrou."
]

frases_mingau_sofa = [
    "Mingau deitou no sofá.",
    "Mingau está rolando e exibindo a barriga.",
    "Mingau se esfregou em você.",
    "Mingau atacou seu braço.",
    "Mingau subiu no encosto do sofá.",
    "Mingau cheirou você.",
    "Mingau miou."
]

frases_mingau_varanda = [
    "Mingau está olhando para o estacionamento lá embaixo.",
    "Mingau está chateado porque caiu chuva nele.",
    "Mingau está correndo atrás de uma mosca na varanda.",
    "Mingau está escalando o apoio da varanda.",
    "Mingau miou."
]

@client.event
async def on_ready():
    print(f'Mingau está online como {client.user}')

@client.event
async def on_message(message):
    antigo_local = local_mingau
    global mingau_inte

    if message.author == client.user:
        return  # Ignora as próprias mensagens do bot

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
        swtchLoc(antigo_local)
        localiza_mingau = f"Mingau saiu de {antigo_local} para {local_mingau}" if antigo_local != local_mingau else "Mingau repentinamente olhou para a vidraça..."
        await message.channel.send(localiza_mingau)

    if message.content.lower() == getenv('COMANDO_MIAU'):
        await message.delete()
        if message.channel.id == CANAL_MINGAL_ID:
            mingau_inte += 1
            if local_mingau == "mesa":
                resposta = random.choice(frases_mingau_mesa)
            elif local_mingau == "chão":
                resposta = random.choice(frases_mingau_chao)
            elif local_mingau == "sofá":
                resposta = random.choice(frases_mingau_sofa)
            elif local_mingau == "varanda":
                resposta = random.choice(frases_mingau_varanda)

            if "Mingau miou." in resposta:
                await message.channel.send(file=discord.File("mingau_miando.mp3"))
            await message.channel.send(resposta)

@client.event
async def on_voice_state_update(member, before, after):
    # Ignora se for bot
    if member.bot:
        return

    canal_voz = after.channel
    guild = member.guild

    # Se a pessoa entrou em um canal de voz
    if canal_voz and before.channel != canal_voz:
        voice_client = guild.voice_client

        if not voice_client or not voice_client.is_connected():
            try:
                vc = await canal_voz.connect()
                print(f"Mingau entrou no canal de voz: {canal_voz.name}")

                # Toca som do mingau miando
                vc.play(discord.FFmpegPCMAudio("mingau_miando.mp3"))
                
                # Envia texto no canal de texto
                canal_texto = discord.utils.get(guild.text_channels, id=CANAL_MINGAL_ID)
                if canal_texto:
                    await canal_texto.send("🐾 Mingau pulou no canal de voz quando alguém chegou!")
            except Exception as e:
                print(f"Erro ao conectar o Mingau: {e}")

    # Se Mingau está sozinho no canal, ele sai
    voice_client = guild.voice_client
    if voice_client and voice_client.channel and len(voice_client.channel.members) == 1:
        await voice_client.disconnect()
        print("Mingau saiu do canal porque ficou sozinho.")

# Inicia o bot
TOKEN = getenv('TOKKEN_MINGAU')
client.run(TOKEN)
