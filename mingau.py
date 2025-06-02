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
    print("Mingal saiu de ", local)
    print("Mingal foi para ", local_mingau)
    mingau_inte = 0


intents = discord.Intents.default()
intents.message_content = True  # MUITO IMPORTANTE para ler o conteúdo das mensagens
client = discord.Client(intents=intents)

# ID do canal onde o Mingal vive
CANAL_MINGAL_ID = 1365765011464523910  # <- você vai colocar o ID do seu canal aqui

# Frases que Mingal pode responder

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

    print(mingau_inte)

    # Comando para limpar mensagens
    if message.content.lower() == getenv('SECRET_MINGAU'):
        #if message.channel.id == CANAL_MINGAL_ID:
            if message.author.guild_permissions.manage_messages:  # Verifica se o autor da mensagem tem permissão
                quantidade = int(message.content.split()[1]) if len(message.content.split()) > 1 else 100  # Quantas mensagens limpar
                await message.channel.send("Você ativou o poder oculto do Mingau...")
                await message.channel.send("Seus olhos começam a brilhar... todos perdem a memória de tudo o que já foi dito nessa sala")
                time.sleep(2)
                await message.channel.purge(limit=quantidade)
            else:
                await message.channel.send("Você não tem permissão para limpar as mensagens!", delete_after=5)

    # Lógica do Mingau
    if mingau_inte > 2 and random.randint(0, 1) == 1:
        swtchLoc(antigo_local)
        localiza_mingau = f"Mingau saiu de {antigo_local} para {local_mingau}" if antigo_local != local_mingau else "Mingau repentinamente olhou para a vidraça..."
        await message.channel.send(localiza_mingau)

    if message.author == client.user:
        return  # Ignora as próprias mensagens do bot

    if message.content.lower() == getenv('COMANDO_MIAU'):
        if message.channel.id == CANAL_MINGAL_ID:
            if local_mingau == "mesa":
                mingau_inte += 1
                resposta = random.choice(frases_mingau_mesa)

            elif local_mingau == "chão":
                mingau_inte += 1
                resposta = random.choice(frases_mingau_chao)

            elif local_mingau == "sofá":
                mingau_inte += 1
                resposta = random.choice(frases_mingau_sofa)

            elif local_mingau == "varanda":
                mingau_inte += 1
                resposta = random.choice(frases_mingau_varanda)

            if "Mingau miou." in resposta:
                await message.channel.send(file=discord.File("mingau_miando.mp3"))
            await message.channel.send(resposta)
        else:
            ...

TOKEN = getenv('TOKKEN_MINGAU')
client.run(TOKEN)