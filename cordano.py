import discord
import asyncio
from discord.ext import commands
import datetime
import os
import random
import json
import unicodedata
import string
import dotenv

dotenv.load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

memoria = []
images2 = ['cordanoia/1.png', 'cordanoia/2.png', 'cordanoia/3.png']

usuarios_path = 'cordanoia/usuarios.json'
data_path = 'cordanoia/data.txt'
i = 0

if not os.path.exists(usuarios_path):
    with open(usuarios_path, 'w') as f:
        json.dump({}, f)

def setday(data=None):
    if data is None:
        data = datetime.datetime.now().date()
    with open(data_path, 'w') as f:
        f.write(str(data))

def readday():
    hoje = datetime.datetime.now().date()
    ultima_data = None
    if os.path.exists(data_path):
        with open(data_path, 'r') as f:
            dat = f.read().strip()
            try:
                ultima_data = datetime.datetime.strptime(dat, '%Y-%m-%d').date()
            except ValueError:
                ultima_data = None
    if ultima_data != hoje:
        with open(usuarios_path, 'r') as f:
            dados = json.load(f)
        for user in dados.values():
            user["visitou_hoje"] = False
        with open(usuarios_path, 'w') as f:
            json.dump(dados, f, indent=2)
        setday(hoje)

@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user}')

def normaliza(texto):
    texto = ''.join(c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn')
    texto = texto.translate(str.maketrans('', '', string.punctuation))
    return texto.lower()

async def imge(canal):
    with open(random.choice(images2), "rb") as f:
        imagem = discord.File(f)
        return await canal.send(file=imagem)

async def faloUsers(dicionario, message, canal):
    x = random.randint(1, 3)
    with open('cordanoia/ultimocomodo.txt', 'r') as file:
        localmilka = file.read().strip()
    conteudo = normaliza(message.content)
    for palavras_chave, resposta in dicionario.items():
        palavras_norm = [normaliza(p) for p in palavras_chave]
        if all(palavra in conteudo for palavra in palavras_norm):
            await asyncio.sleep(x)
            await imge(canal)
            await message.channel.send(resposta)
            return

@bot.event
async def on_message(message):
    global i
    if message.channel.id != 1354312727388225617:
        return

    raw_content = message.content
    conteudo_msg = normaliza(message.content)
    autor = message.author.display_name

    conversausers = {
        ('eae cordano', 'finalmente consegui', 'me da uma vodka'): 'Tranquilo, camarada. Parece cansada, você tá pra lá e pra cá o dia todo.',
        ('acabou', 'city pop', 'serra'): 'Boa, sempre gosto de te acompanhar nessa. Muder disse que passará aqui, falei com ela pela transmissão de rádio',
        ('e como estao as', 'coisas por la'): 'Parece que a federação está planejando subir a serra em uma nova operação. A Dama já está articulando a guerrilha.',
        ('ela deve vir', 'falar sobre', 'vir sozinha'): 'Não sei... você tá preocupada com alguém?',
        ('com quem nos preocuparmos', 'tentar uma comunicacao', 'organizacoes urbanas'): 'Na verdade tenho que contatá-los, se ver o Terega por aí fale que Muder está por vir.',
    }

    await faloUsers(conversausers, message, message.channel)

    async def musica():
        global i
        with open('musics.txt', 'r') as f:
            musi = f.read()
        if 'Sweet Love' in musi.strip() and i < 1:
            i += 1
            return 'Essa música me lembra você... por que teve que ir embora?... Ah! Aí está você.'
        return '_'

    readday()

    with open('cordanoia/memoriageral', 'a', encoding='utf-8') as f:
        f.write(f'{autor} disse: {message.content}\n')

    async def doing(bruh, image='', message=None):
        if message is None:
            return
        if image:
            with open(image, "rb") as f:
                imagem = discord.File(f)
                await message.channel.send(file=imagem)
        await message.channel.send(bruh)

    frases = [
        "Olha só... o rádio só faz chiar. Fraga disse faria a transmição essa noite. Não vi nada sobre a serra na TV... Eu odeio não ter norícias.",
        "Você viu o Berto por aí? preciso que ele leve uma mensagem pra Dama.",
        "Ele sabe os caminhos mais seguros evitando as tropas da federação. Ainda não vi ele por aqui."
    ]
    poses = images2

    with open(usuarios_path, 'r') as f:
        dados = json.load(f)

    user_data = dados.get(autor, {
        "visitou_hoje": False,
        "visitas_total": 0,
        "ultima_data": str(datetime.datetime.now().date()),
        "iteracoes": 0,
        "itens": {}
    })

    # 👇 Resposta imediata quando digita só "cordano"
    if conteudo_msg.strip() == "cordano":
        user_data["iteracoes"] = 0
        dados[autor] = user_data
        with open(usuarios_path, 'w', encoding='utf-8') as f:
            json.dump(dados, f, indent=2)
        texto = frases[user_data["iteracoes"]]
        user_data["iteracoes"] = (user_data["iteracoes"] + 1) % len(frases)
        dados[autor] = user_data
        with open(usuarios_path, 'w', encoding='utf-8') as f:
            json.dump(dados, f, indent=2)
        await doing(texto, random.choice(poses), message)
        await asyncio.sleep(1)
        await doing("[>c] para seguir", message=message)
        return

    if not user_data["visitou_hoje"] and "cordano" in conteudo_msg:
        user_data["visitou_hoje"] = True
        user_data["visitas_total"] += 1
        user_data["ultima_data"] = str(datetime.datetime.now().date())
        user_data["iteracoes"] = 0
        user_data["itens"] = {}
        dados[autor] = user_data
        with open(usuarios_path, 'w', encoding='utf-8') as f:
            json.dump(dados, f, indent=2)

        cumprimentos = [
            f'🎵🎵kasanetemiru no Aah, konna ni mo kagayaite-mieru machi🎶🎶!!! hey, olha só você, {autor}!' if i > 0 else f'{autor}? com essa luz quase não te vejo',
            f'Hey, {autor}, abaixo a federação',
            f'Vi que resolveu se juntar a nós. Bom ter você aqui hoje.',
            f'{autor}? com essa luz quase não te vejo'
        ]

        await doing(await musica(), random.choice(poses), message)
        await doing(random.choice(cumprimentos), message=message)
        await doing('[>c] para seguir.', message=message)
        return

    elif user_data["visitou_hoje"] and raw_content.startswith(">c") and "cordano" in user_data["itens"].get("fita123", []):
        fita = user_data["itens"]["fita123"]
        if "cordano" in fita:
            fita.remove("cordano")
            dados[autor] = user_data
            with open(usuarios_path, 'w', encoding='utf-8') as f:
                json.dump(dados, f, indent=2)
        texto = 'Vejo que você tem uma fita com voce. Você pode tocar fitas como essa na jukebox, use seu nome como comando na jukebox.'
        await doing(texto, random.choice(poses), message)
        return

    elif 'cordano' in conteudo_msg and "voce sabe" in conteudo_msg and "segredo" in conteudo_msg:
        await doing('Não sei do que você tá falando, mas nem todos canais de TV são janelas pro passado', random.choice(poses), message)
        return

    elif 'cordano' in conteudo_msg and "ano" in conteudo_msg and "estamos" in conteudo_msg:
        await doing('Tá bom, chega de bebida pra você.', random.choice(poses), message)
        await doing('Os desenhos de séculos antigos têm confundido sua cabeça?', message=message)
        return

    elif raw_content.startswith(">c"):
        texto = frases[user_data["iteracoes"]]
        user_data["iteracoes"] = (user_data["iteracoes"] + 1) % len(frases)
        dados[autor] = user_data
        with open(usuarios_path, 'w', encoding='utf-8') as f:
            json.dump(dados, f, indent=2)
        await doing(texto, random.choice(poses), message)
        await asyncio.sleep(1)
        await doing("[>c] para seguir", message=message)
        return

    await bot.process_commands(message)
TOKKEN = os.getenv("TOKKEN_CORDANO")
bot.run(TOKKEN)