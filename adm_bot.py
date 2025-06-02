import discord
from discord.ext import commands
from collections import defaultdict
from dotenv import load_dotenv
from os import getenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# IDs do servidor e canais
ID_SERVIDOR = 1354266715785134160

CANAL_TEXTO_SALA = 1354275870956851384
CANAL_TELEVISAO = 1365765011464523910

CANAL_TEXTO_CORREDOR = 1354333089781780490
CANAL_AUDIO_CORREDOR = 1376065935235874948

CANAL_TEXTO_ESCADARIA = 1354316192042455080
CANAL_AUDIO_ESCADARIA = 1377161141469315132

CANAL_TEXTO_EXTERIOR = 1354333283483390032
CANAL_AUDIO_EXTERIOR = 1366035560249954315

CANAL_TEXTO_BANHEIRO = 1354316992764711012
CANAL_AUDIO_BANHEIRO = 1376116149472727111

CANAL_TEXTO_BALCAO = 1354312727388225617
CANAL_TEXTO_MESA_1 = 1354312920569221211
CANAL_TEXTO_MESA_2 = 1354313052060909598
CANAL_TEXTO_MESA_3 = 1354313099640963092
CANAL_AUDIO_JUKEBOX = 1354311386100011078

# Contador de mensagens por usuário e por canal de texto
mensagens_por_usuario = defaultdict(int)

@bot.event
async def on_ready():
    print(f"✅ Bot online como {bot.user}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    user_id = message.author.id

    def deve_enviar(canal_texto, canal_audio_esperado):
        return (
            message.channel.id == canal_texto and
            not (message.author.voice and message.author.voice.channel and message.author.voice.channel.id == canal_audio_esperado)
        )

    # CORREDOR
    if deve_enviar(CANAL_TEXTO_CORREDOR, CANAL_AUDIO_CORREDOR):
        mensagens_por_usuario[(user_id, CANAL_TEXTO_CORREDOR)] += 1
        count = mensagens_por_usuario[(user_id, CANAL_TEXTO_CORREDOR)]
        if count % 20 == 0 or count == 1:
            embed = discord.Embed(
                title="🌆 Corredor",
                description=f"{message.author.name}, perceba ao fundo... de longe você ouve a música que vem do bar enquanto está no corredor banhado pelo neon vermelho.",
                color=0xFF3C3C
            )
            embed.set_image(url="https://i.pinimg.com/736x/53/4e/0b/534e0b642a92c6bd5fe2a12929d899c8.jpg")
            embed.add_field(
                name="🎧 Entrar no canal de áudio",
                value=f"[Clique aqui para entrar](https://discord.com/channels/{ID_SERVIDOR}/{CANAL_AUDIO_CORREDOR})",
                inline=False
            )
            await message.channel.send(embed=embed)

    # EXTERIOR
    elif deve_enviar(CANAL_TEXTO_EXTERIOR, CANAL_AUDIO_EXTERIOR):
        mensagens_por_usuario[(user_id, CANAL_TEXTO_EXTERIOR)] += 1
        count = mensagens_por_usuario[(user_id, CANAL_TEXTO_EXTERIOR)]
        if count % 20 == 0 or count == 1:
            embed = discord.Embed(
                title="🌧️ Exterior",
                description=f"{message.author.name}, ouça o som da noite... daqui das escadas você pode parar para apreciar a chuva e pássaros cantando.",
                color=0x00BFFF
            )
            embed.set_image(url="https://i.pinimg.com/736x/d4/32/49/d432499aa3a0c6d7bf7315caf4263e21.jpg")
            embed.add_field(
                name="🎧 Entrar no canal de áudio",
                value=f"[Clique aqui para entrar](https://discord.com/channels/{ID_SERVIDOR}/{CANAL_AUDIO_EXTERIOR})",
                inline=False
            )
            await message.channel.send(embed=embed)
    
    #ESCADARIA
    elif deve_enviar(CANAL_TEXTO_ESCADARIA, CANAL_AUDIO_ESCADARIA):
        mensagens_por_usuario[(user_id, CANAL_TEXTO_ESCADARIA)] += 1
        count = mensagens_por_usuario[(user_id, CANAL_TEXTO_ESCADARIA)]
        if count % 20 == 0 or count == 1:
            embed = discord.Embed(
                title="🌧️ Exterior",
                description=f"{message.author.name}, ouça o som da noite... daqui das escadas você pode parar para apreciar a chuva e pássaros cantando.",
                color=0x00BFFF
            )
            embed.set_image(url="https://i.pinimg.com/736x/17/06/23/170623e163253b2d45666438ffc4e034.jpg")
            embed.add_field(
                name="🎧 Entrar no canal de áudio",
                value=f"[Clique aqui para entrar](https://discord.com/channels/{ID_SERVIDOR}/{CANAL_AUDIO_ESCADARIA})",
                inline=False
            )
            await message.channel.send(embed=embed)

    # BANHEIRO
    elif deve_enviar(CANAL_TEXTO_BANHEIRO, CANAL_AUDIO_BANHEIRO):
        mensagens_por_usuario[(user_id, CANAL_TEXTO_BANHEIRO)] += 1
        count = mensagens_por_usuario[(user_id, CANAL_TEXTO_BANHEIRO)]
        if count % 20 == 0 or count == 1:
            embed = discord.Embed(
                title="🚽 Banheiro",
                description=f"{message.author.name}, está aproveitando a solidão do banheiro? Você pode curtir ainda mais ativando o som ambiente:",
                color=0xAAAAAA
            )
            embed.set_image(url="https://i.pinimg.com/736x/28/7a/97/287a97445a31f65b973b14614d88816c.jpg")
            embed.add_field(
                name="🎧 Entrar no canal de áudio",
                value=f"[Clique aqui para entrar](https://discord.com/channels/{ID_SERVIDOR}/{CANAL_AUDIO_BANHEIRO})",
                inline=False
            )
            await message.channel.send(embed=embed)
    
    elif deve_enviar(CANAL_TEXTO_SALA, CANAL_TELEVISAO):
        mensagens_por_usuario[(user_id, CANAL_TEXTO_SALA)] += 1
        count = mensagens_por_usuario[(user_id, CANAL_TEXTO_SALA)]
        if count % 20 == 0 or count == 1:
            embed = discord.Embed(
                title=" Sala pricipal",
                description=f"{message.author.name}, Ligue a TV, talvez para ver um dos canais ou para ter um som de fundo diferente enquanto conversa.",
                color=0x00BFFF
            )
            embed.set_image(url="https://i.pinimg.com/736x/f7/88/eb/f788eb666869d349cc04690acdd6307d.jpg")
            embed.add_field(
                name="🎧 Entrar no canal de áudio",
                value=f"[Clique aqui para entrar](https://discord.com/channels/{ID_SERVIDOR}/{CANAL_TELEVISAO})",
                inline=False
            )
            await message.channel.send(embed=embed)

    # MESAS E BALCÃO (compartilham canal de áudio do bar)
    elif message.channel.id in [CANAL_TEXTO_BALCAO, CANAL_TEXTO_MESA_1, CANAL_TEXTO_MESA_2, CANAL_TEXTO_MESA_3] and not (
        message.author.voice and message.author.voice.channel and message.author.voice.channel.id == CANAL_AUDIO_JUKEBOX
    ):
        mensagens_por_usuario[(user_id, message.channel.id)] += 1
        count = mensagens_por_usuario[(user_id, message.channel.id)]
        if count % 20 == 0 or count == 1:
            embed = discord.Embed(
                title="🎵 Jukebox do Bar",
                description=f"{message.author.name}, aproveite a ambientação completa. A música está rolando no bar — junte-se ao som!",
                color=0xFFD700
            )
            embed.set_image(url="https://i.pinimg.com/736x/c4/f5/d2/c4f5d20824551a5fcf52f60f6b6dfbb7.jpg")
            embed.add_field(
                name="🎧 Entrar no canal de áudio",
                value=f"[Clique aqui para entrar](https://discord.com/channels/{ID_SERVIDOR}/{CANAL_AUDIO_JUKEBOX})",
                inline=False
            )
            await message.channel.send(embed=embed)

    await bot.process_commands(message)

# Coloque seu token aqui
bot.run(getenv("TOKKEN_ADM_BOT"))