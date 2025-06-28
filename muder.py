import discord
import random
import asyncio
from  discord.ext import commands
from falas_muder import falas_bot

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.command()
async def sala(ctx):
    with open('muder/ultimocomodo.txt', 'a') as file:
        canal = ctx.channel
        await canal.send('No sala')
        file.write(str(1354275870956851384))

@bot.command()
async def banheiro(ctx):
    with open('muder/ultimocomodo.txt', 'a') as file:
        canal = ctx.channel
        await canal.send('No banheiro')
        file.write(str(1354316992764711012))

@bot.command()
async def balcao(ctx):
    with open('muder/ultimocomodo.txt', 'a') as file:
        canal = ctx.channel
        await canal.send('No balcao')
        file.write(str(1354312727388225617)+'\n')
        file.write(str(1384988346706821160)+'\n')

@bot.command()
async def corredor(ctx):
    with open('muder/ultimocomodo.txt', 'a') as file:
        canal = ctx.channel
        await canal.send('No corredor')
        file.write(str(1354333089781780490))

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    if message.content == "Chamando Muder" and message.author.display_name:
        await asyncio.sleep(2)
        await message.reply(falas_bot.get("Milka")[0])
    
    elif message.content == "Resposta 1 para muder":
        await asyncio.sleep(2)
        await message.reply(falas_bot.get("Milka")[1])
    
    elif message.content == "Resposta dois para muder":
        await asyncio.sleep(2)
        await message.reply(falas_bot.get("Milka")[2])


    await bot.process_commands(message)
    

bot.run('MTM4NDk4ODM0NjcwNjgyMTE2MA.GvIL6Y.o8t6xpe4sE1XjV2C3RJzUFJW7uTRVrnXoF1Duo')