import discord
from discord.ext import commands
from collections import defaultdict
from dotenv import load_dotenv
from os import getenv
from db_files.milka_db_utils import insertUser, verifyUser, insertPendent, deleteUser, selectMilka, updtMilka, insertAsked, verifyaskeds, truncTable, verifyterms, selectTalks, insertInventario, selectInventario, deletarCDsDoInventario
import os
import asyncio
import random
import datetime
from milka_docs.falas import falas_pendent, fala_padrao, fala_bots, falas_chat_comum
#import mysql.connector
load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
intents.guilds = True
intents.members = True
intents.presences = True
bot = commands.Bot(command_prefix="!", intents=intents)
images2 = ['imagens/Milka_3.png']

ii = 0
i5 = 0

CANALCADASTRO = 1383461556993527980
ROLEINIT = 1383461909646278656
MEMBER_ROLE = 1386002510736658432
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

async def dellDesk(task_name):
    for task in asyncio.all_tasks():
        if task.get_name() == task_name:
            task.cancel()
            await task

async def verifico_id_lista(id, doc):
    with open(doc, 'r') as file:
        arquivo = [linha.strip() for linha in file.readlines() if linha.strip()]
        if id not in arquivo:
            with open(doc, 'a') as file:
                file.write(id +'\n')
                
async def isOn(member, canal):
    while True:
        guild = bot.get_guild(1354266715785134160)
        lista = [x.name for x in guild.members]
        if member.name not in lista:
            await canal.delete()
            await dellDesk("on_server")
        await asyncio.sleep(10)  # Diminui a frequência pra evitar ser rate-limited

@bot.command()
async def found(ctx):
    canal_user = ctx.channel.id
    variavel = ''
    bots_on_channel = []
    bots = {
        'milka': 'milka_docs/ultimocomodo.txt',
        'mingau': 'mingau_docs/ultimocomodo.txt',
        'muder': 'muder/ultimocomodo.txt',
        'cordano': 'cordanoia/ultimocomodo.txt'
    }

    LUGARES = {
        'BAR': [CANAL_AUDIO_JUKEBOX, CANAL_TEXTO_BALCAO, CANAL_TEXTO_MESA_1, CANAL_TEXTO_MESA_2, CANAL_TEXTO_MESA_3],
        'SALA': [CANAL_TELEVISAO, CANAL_TEXTO_SALA],
        'BANHEIRO': [CANAL_AUDIO_BANHEIRO, CANAL_TEXTO_BANHEIRO],
        'CORREDOR': [CANAL_AUDIO_CORREDOR, CANAL_TEXTO_CORREDOR],
        'ESCADA': [CANAL_AUDIO_ESCADARIA, CANAL_TEXTO_ESCADARIA],
        'EXTERIOR': [CANAL_AUDIO_EXTERIOR, CANAL_TEXTO_EXTERIOR],
    }

    for nome_bot, path in bots.items():
        with open(path, 'r') as file:
            canal_id_bot = int(file.readline().strip())

        for lugar, canais in LUGARES.items():
            if canal_id_bot in canais and canal_user in canais:
                bots_on_channel.append(nome_bot)
                break  # evita checar outros lugares depois que achou um

    if not bots_on_channel:
        await ctx.reply("O cômodo está vazio")
        return

    for nome_bot in bots_on_channel:
        with open(bots[nome_bot], 'r') as file:
            canal_id = int(file.readline().strip())
        canal = bot.get_channel(canal_id)
        canal_nome = canal.name if canal else "Canal desconhecido"
        variavel += f'{nome_bot} está no cômodo, em {canal_nome}\n'

    await ctx.reply(variavel)

async def verif():
    guild = bot.get_guild(1354266715785134160)  # Use o ID fixo do servidor
    if not guild:
        print("Guild não encontrada!")
        return

    membros = guild.members
    arquivo = await verifyUser('users') # Tira o '\n'
    arquivo2 = await verifyUser('pendents')
    ids_registrados = {linha[0] for linha in arquivo}
    ids_pendentes = {linha[0] for linha in arquivo2}

    for membro in membros:
        if membro.bot:
            continue  # Ignora bots

        if membro.id not in ids_registrados:
            print(f"O usuário {membro.display_name} ({membro.id}) não está registrado")

            if membro.id not in ids_pendentes:
                await insertPendent(membro.id, membro.display_name)

async def achoBot_id(lista1, lista2, milka, *bots):
    for x in bots:
        with open(milka, 'r') as loc:
            localmilka = loc.read()

        with open(x, 'r') as file:
            listaa = file.readlines()
            localbot = listaa[0].strip()
            idbot = listaa[1].strip()

            if localbot == localmilka:
                lista2.append(idbot)
                lista1.append(localbot)

async def faco(x, y, a):
    async def inter():
        agora = datetime.datetime.now()
        retorno = await selectMilka("ULT_COM_")
        comodo = [comodo[0] for comodo in retorno]
        comodo_antigo = comodo[0]
        
        if agora.hour == x:
            await updtMilka("ULT_COM_", "NAME", int(y), "Milka")
            
        retorno = await selectMilka("ULT_COM_")
        comodo = [comodo[0] for comodo in retorno]
        comodo_atual = comodo[0]

        if comodo_antigo != comodo_atual:
            canal = bot.get_channel(int(comodo_antigo))
            await canal.send(f"Milka saiu de {canal.name}")
            print(f"Milka saiu de {canal.name}")

    return inter

async def calltask():
    global i5

    target_hour = 13
    rando = True  # Horário fixo da checagem
    #envio = 2   
    mesas = [CANAL_TEXTO_MESA_1, CANAL_TEXTO_MESA_2, CANAL_TEXTO_MESA_3]
    hora_milka_coversation, hora_milka_coversation2 = random.sample(range(24), 2)
    minute_milka_conversation, minute_milka_conversation2 = random.sample(range(60), 2)
    hora_milka_corredor, hora_milka_balcao, hora_milka_sala, hora_milka_exterior, hora_milka_mesa = random.sample(range(24), 5)
    #print('hora1: ', hora_milka_coversation, 'hora2: ', hora_milka_coversation2)
    #print('minute1: ', minute_milka_conversation, 'minute2: ', minute_milka_conversation2)
    #minuterange_milka_conversation = random.randint(minute_milka_conversation, 59)
    print("hora milka coversation: ", hora_milka_coversation, "hora milka coversation2: ", hora_milka_coversation2)
    print("minutes milka coversation: ", minute_milka_conversation, "minutes milka coversation2: ", minute_milka_conversation2)
    print('corredor: ', hora_milka_corredor, 'bar: ', hora_milka_balcao, 'sala: ', hora_milka_sala, 'mesa: ', hora_milka_mesa, 'exterior: ', hora_milka_exterior)

    possibles = {
            str(hora_milka_balcao): await faco(hora_milka_balcao, CANAL_TEXTO_BALCAO, i5),
            str(hora_milka_sala): await faco(hora_milka_sala, CANAL_TEXTO_SALA, i5),
            str(hora_milka_exterior): await faco(hora_milka_exterior, CANAL_TEXTO_EXTERIOR, i5),
            str(hora_milka_corredor): await faco(hora_milka_corredor, CANAL_TEXTO_CORREDOR, i5),
            str(hora_milka_mesa): await faco(hora_milka_mesa, random.choice(mesas), i5)
}

    while True:
        comodos_dos_bots = []
        bots_no_canal = []
        agora = datetime.datetime.now()
        hoje = agora.day
        hora_atual = agora.hour
        bot_choiced = ''
        local_choiced = ''

        for x, y in possibles.items():
            if str(agora.hour) == x and rando:
                await y()
        
        await achoBot_id(comodos_dos_bots ,bots_no_canal, 'milka_docs/ultimocomodo.txt', 'muder/ultimocomodo.txt', 'mingau_docs/ultimocomodo.txt', 'cordanoia/ultimocomodo.txt')
        with open('milka_docs/ultimocomodo.txt', 'r') as file:
            localMilka = file.read()

        n = 1 if len(bots_no_canal) > 0 else 0

        #if envio > 0:
        i = random.randint(0, len(bots_no_canal) - n)
        for x, y in enumerate(bots_no_canal):
            if x == i:
                bot_choiced = bots_no_canal[x]
                local_choiced = comodos_dos_bots[x]
                    #print('canal do bot: ', comodos_dos_bots[x], 'id do bot: ', bots_no_canal[x])
        
        if local_choiced == localMilka and bot_choiced != '' and local_choiced != ''and rando\
            and agora.hour in [hora_milka_coversation, hora_milka_coversation2] and agora.minute in [minute_milka_conversation, minute_milka_conversation2]:
            canal = bot.get_channel(int(localMilka))
            await canal.send(fala_bots.get(bot.get_user(int(bot_choiced)).display_name)()[0])
            await asyncio.sleep(60)

        # Garante que o arquivo de controle existe
        returno = await selectMilka("HOJE")
        days = [day[0] for day in returno]
        
        if days[0] is None:
            await updtMilka("HOJE", "NAME", 0, 'Milka')

        # Lê o último dia que a Milka disparou
        returno = await selectMilka("HOJE")
        days = [day[0] for day in returno]
        content = days[0]

        try:
            dia_executado = int(content)
        except ValueError:
            dia_executado = 0  # Caso o arquivo esteja corrompido
    
        # Se for o horário alvo e ainda não executou hoje
        if hora_atual == target_hour and dia_executado != hoje:
            await truncTable('askeds')
            #envio = 2
            hora_milka_coversation, hora_milka_coversation2 = random.sample(range(24), 2)
            minute_milka_conversation, minute_milka_conversation2 = random.sample(range(60), 2)
            # ✅ Faz a verificação de pendentes ANTES de disparar as mensagens
            await verif()

            guild = bot.get_guild(1354266715785134160)
            if guild:
                try:
                    
                    pends = await verifyUser('pendents')
                    pendentes = [pendente[0] for pendente in pends]

                    for user_id in pendentes:
                        membro = guild.get_member(int(user_id))
                        if membro:
                            try:
                                await membro.send(f"{membro.display_name}, preciso falar com você")
                                await membro.send(f"Não sei como você passou por mim sem se registrar. Então, não me faça perder tempo e venha falar comigo!")
                            except Exception as e:
                                print(f"Erro ao tentar mandar mensagem para {membro.display_name}: {e}")

                    # Atualiza o dia de execução para hoje
                    await updtMilka("HOJE", "NAME", hoje, "Milka")
                    print(f"Milka disparou as mensagens do dia {hoje}.")

                except Exception as e:
                    print(f"Erro durante o envio das mensagens: {e}")

        # Dorme 60 segundos antes de verificar de novo
        await asyncio.sleep(5)

async def escrevoHumor(x):
    await updtMilka("HUMOR", "NAME", x, "Milka")

async def vejoHumor():
    estreseReturn = await selectMilka("HUMOR")
    estrese = [x[0] for x in estreseReturn][0]
    retorno = await selectMilka("HUMOR")
    dados = [x[0] for x in retorno]
    humor = dados[0]

    return humor

async def func(member, pedente=False):
    global extress    
    i = 0
    i2 = 0
    i3 = 0
    apresentacoesReturn = await selectTalks(cond="init")
    apresentacoes = [x[0] for x in apresentacoesReturn]
    apresentacoesReturn2 = await selectTalks(cond="init2")
    apresentacoes2 = [x[0] for x in apresentacoesReturn2]
    #apresentacoes2 = ['Ah... é você, você ficou de me passar algumas informações.', 'Resolveu aparecer pra fazer o registro? Eu tava te procurando.']
    images = ['imagens/Milka_1.png']

    estreseReturn = await selectMilka("HUMOR")
    estrese = [x[0] for x in estreseReturn][0]
    pends = await verifyUser('pendents')
    arquivo2 = [pendente[0] for pendente in pends]

    name = member.display_name
    primeiro_nome = name.split()[0] if len(name.split()) > 1 else name
    estilo_musical = ''
    como_chegou = ''

    # Criar canal privado para o membro com permissões exclusivas
    overwrites = {
            member.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            member: discord.PermissionOverwrite(read_messages=True),
            bot.user: discord.PermissionOverwrite(read_messages=True)
    }
    canal = await member.guild.create_text_channel(f'cadastro-{primeiro_nome}', overwrites=overwrites)
    
    role_inicial = member.guild.get_role(ROLEINIT)

    validReturns = await verifyterms()
    validlist = [term[0] for term in validReturns]
    forgetReturns = await verifyterms("unk")
    forget = [forg[0] for forg in forgetReturns]
    envtReturns = await verifyterms("env")
    envtme = [envt[0] for envt in envtReturns]
    convidado = forget + envtme

    c0Return = await selectTalks(cond="c0")
    c0 = [x[0] for x in c0Return]
    c1Return = await selectTalks(cond="c1")
    c1 = [x[0] for x in c1Return]
    c2Return = await selectTalks(cond="c2")
    c2 = [x[0] for x in c2Return]
    
    perguntas = [
    c0[0].format(member_display_name=member.display_name),
    c1[0].format(member_display_name=member.display_name),
    c2[0].format(member_display_name=member.display_name).replace("\\n", "\n"),                                                           
]
    
    task1 = asyncio.create_task(isOn(member, canal))
    task1.set_name("on_server")
    if role_inicial:
    # Remove todas as roles, exceto @everyone
        roles_a_remover = [r for r in member.roles if r.name != "@everyone"]
        if roles_a_remover:
            await member.remove_roles(*roles_a_remover)

    # Adiciona a nova role
        await member.add_roles(role_inicial)

    # Envia mensagem de boas-vindas, se não for pendente
        if not pedente:
            await canal.send(
                random.choice(apresentacoes if str(member.id) not in arquivo2 else apresentacoes2)
            )

        async def imge():
            with open(random.choice(images), "rb") as f:
                imagem = discord.File(f)
                return await canal.send(file=imagem)

        async def msge(x=False):
            if not x:
                return '-'
            await imge()
            return await canal.send(perguntas[i])
        
        async def milk(name, eu, st):
            envter = await selectTalks(cond='cnvm')
            envte = [en[0] for en in envter]
            unkr = await selectTalks(cond='unk')
            unk = [en[0] for en in unkr]

            if eu.lower() == 'milka':
                await canal.send(envte[0])
                await asyncio.sleep(1)
                eu = f'{name} alegou que foi convidado por min.'
                return eu
            
            elif any(x in eu.lower() for x in forget):
                await canal.send(unk[0])
                await asyncio.sleep(1)
                eu = f'{name} não lembra ou não sabe quem lhe deu o convite, suspeito! Fiquem de olho!'
                return eu
            
            else:
                st = f' convidou.'
                eu = eu + st
                return eu
        estreseReturn = await selectMilka("HUMOR")
        estrese = [x[0] for x in estreseReturn][0]
        estreseReturn = await selectMilka("HUMOR")
        extress = [x[0] for x in estreseReturn][0]

        async def ender(nome, convite, estilo, cd, comando):
            estreseReturn = await selectMilka("CTRL_HUMOR")
            extress = [x[0] for x in estreseReturn][0]
            end0R = await selectTalks(0, 'end0')
            ends0 = [x[0] for x in end0R]
            end1R = await selectTalks(1, 'end1')
            ends1 = [x[0] for x in end1R]
            end2R = await selectTalks(2, 'end2')
            ends2 = [x[0] for x in end2R]
            
            if extress < 3:
                await escrevoHumor(0)

            elif 5 > extress >= 3:
                await escrevoHumor(1)
            
            elif extress >= 5:
                await escrevoHumor(2)

            extress_ = await vejoHumor()

            async def endier(lista):
                for x in lista:
                    try:
                        x = x.format(nome=primeiro_nome, estilo=cd, comando=comando)
                    except KeyError:
                        pass  # Ignora placeholders que não existem na string
                    await canal.send(x)
                    await asyncio.sleep(1)

            if extress_ == 0:
                await endier(ends0)
                
            elif extress_ == 1:
                await endier(ends1)

            elif extress_ == 2:
                await endier(ends2)
        
        retR = await selectTalks(cond="ret")
        rets = [r[0] for r in retR]
        user = await verifyUser("users", member.id)
            
        if len(user) > 0 and int(member.id) == int(user[0][0]):
            try:
                await canal.send(rets[0].format(member_display_name=member.display_name))
                await asyncio.sleep(1) 
                await canal.send(rets[1].format(member_display_name=member.display_name))
                await asyncio.sleep(1) 
                await canal.send(rets[2].format(member_display_name=member.display_name))
                await canal.send(rets[3].format(member_display_name=member.display_name))
                alguem2 = await bot.wait_for('message', check=lambda m: m.channel == canal, timeout=20)

                if alguem2.content:
                    
                    role_membro = member.guild.get_role(MEMBER_ROLE)
                    await member.remove_roles(role_inicial)
                    if role_membro:
                        await member.add_roles(role_membro)
                
                    await canal.delete()
                    await dellDesk('on_server')
                    estreseReturn = await selectMilka("CTRL_HUMOR")
                    extress = [x[0] for x in estreseReturn][0] - 1
                    if extress < 0:
                        extress = 0
                    await updtMilka("CTRL_HUMOR", 'NAME', extress, 'Milka')
                    return
                
            except asyncio.TimeoutError:
                role_membro = member.guild.get_role(MEMBER_ROLE)
                await member.remove_roles(role_inicial)
                if role_membro:
                    await member.add_roles(role_membro)

            # Apagar o canal de cadastro
                await canal.delete()
                await verifico_id_lista(str(member.id), 'milka_docs/ids.txt')
                await dellDesk("on_server")

        def check(m):
            return m.author == member and m.channel == canal

        try:
            x = True
            r = False
            while i < len(perguntas):
                await msge(x)
                msg = await bot.wait_for('message', check=check, timeout=120)

                if '?' in msg.content:
                    await canal.send('Eu faço as perguntas, aqui! Pare de fugir e me fala...')
                    x = False
                    continue

                if i == 0 and msg.content.lower() in validlist:
                    positiveReturn = await verifyterms("pos")
                    positiva = [x[0] for x in positiveReturn]
                    negativeReturn = await verifyterms("neg")
                    negativa = [x[0] for x in negativeReturn]

                    if msg.content.lower() in positiva:
                        await canal.send('...')
                        i += 1
                        x = True
                        continue

                    elif msg.content.lower() in negativa:
                        if i2 < 1:
                            await canal.send(c0[1])
                            i2 += 1
                            x = False
                            await asyncio.sleep(1)
                            continue

                        elif i2 == 1:
                            i2 += 1
                            await imge()
                            await canal.send(c0[2])
                            await asyncio.sleep(2)
                            await canal.send(c0[3].format(primeiro_nome=primeiro_nome))
                            x = False
                            estreseReturn = await selectMilka("CTRL_HUMOR")
                            extress = [x[0] for x in estreseReturn][0] + 1
                            
                            if extress > 7:
                                extress = 7

                            await updtMilka("CTRL_HUMOR", 'NAME', extress, 'Milka')
                            await asyncio.sleep(1)
                            continue

                        else:
                            await imge()
                            await canal.send(c0[4].format(member_display_name=member.display_name))
                            await asyncio.sleep(2)
                            await canal.send(c0[5])
                            await asyncio.sleep(2)
                            await canal.send(c0[6].format(member_display_name=member.display_name))
                            resp = member.display_name
                            i2 = 0
                            i += 1
                            x = True
                            estreseReturn = await selectMilka("CTRL_HUMOR")
                            extress = [x[0] for x in estreseReturn][0] + 2
                            
                            if extress > 7:
                                extress = 7

                            await updtMilka("CTRL_HUMOR", 'NAME', extress, 'Milka')
                            continue

                elif i == 0 and msg.content.lower() not in validlist:
                    if i3 < 1:
                        await canal.send(c0[7])
                        await asyncio.sleep(1)
                        await canal.send(c0[8].format(primeiro_nome=primeiro_nome))
                        i3 += 1
                        x = False
                        estreseReturn = await selectMilka("CTRL_HUMOR")
                        extress = [x[0] for x in estreseReturn][0] + 1
                            
                        if extress > 7:
                            extress = 7

                        await updtMilka("CTRL_HUMOR", 'NAME', extress, 'Milka')
                        continue

                    elif i3 == 1:
                        await imge()
                        await canal.send(c0[9])
                        await asyncio.sleep(2)
                        await canal.send(c0[10].format(primeiro_nome=primeiro_nome))
                        i3 += 1
                        x = False
                        estreseReturn = await selectMilka("CTRL_HUMOR")
                        extress = [x[0] for x in estreseReturn][0] + 1
                            
                        if extress > 7:
                            extress = 7

                        await updtMilka("CTRL_HUMOR", 'NAME', extress, 'Milka')
                        continue
                    
                    else:
                        await imge()
                        await canal.send(c0[11])
                        resp = member.display_name
                        i3 = 0
                        i += 1
                        x = True
                        estreseReturn = await selectMilka("CTRL_HUMOR")
                        extress = [x[0] for x in estreseReturn][0] + 2
                            
                        if extress > 7:
                            extress = 7

                        await updtMilka("CTRL_HUMOR", 'NAME', extress, 'Milka')
                        continue
                    
                xi = 'QR code'
                
                if i == 1 and xi.lower() in msg.content.lower():
                    como_chegou = msg.content
                    i += 1
                    x = True
                    await canal.send(c1[1])
                    await asyncio.sleep(2)
                    await canal.send(c1[2])
                    await asyncio.sleep(2)
                    continue

                elif i == 1 and any(x in msg.content.lower() for x in convidado):
                    
                    humorret = await selectMilka('CTRL_HUMOR')
                    humor = int([x[0] for x in humorret][0])
                    
                    if humor < 3:
                        await escrevoHumor(0)

                    elif 5 > humor >= 3:
                        await escrevoHumor(1)
            
                    elif humor >= 5:
                        await escrevoHumor(2)

                    alguem = ''
                    st = f''

                    await canal.send(c1[3])
                    alguem = await bot.wait_for('message', check=check, timeout=60)
                    alguem.content = await milk(primeiro_nome, alguem.content, st)
                    guild_ = bot.guilds[0]
                    members = [x.display_name.split()[0].lower() if ' ' in x.display_name else x.display_name.lower() for x in guild_.members]
                    primeiro_nome_alg = alguem.content.split()[0].lower() if ' ' in alguem.content else alguem.content.lower()
                    
                    if primeiro_nome_alg.lower() not in members:
                        humorret = await selectMilka('HUMOR')
                        humor = int([x[0] for x in humorret][0])
                        unk0Return = await selectTalks(cond='unk2', humor=0)
                        unk1Return = await selectTalks(cond='unk2', humor=1)
                        unk2Return = await selectTalks(cond='unk2', humor=2)
                        unk0 = [x[0].format(primeiro_nome_alg=primeiro_nome_alg) for x in unk0Return][0]
                        unk1 = [x[0].format(primeiro_nome_alg=primeiro_nome_alg) for x in unk1Return][0]
                        unk2 = [x[0].format(primeiro_nome_alg=primeiro_nome_alg) for x in unk2Return][0]
                        unks =[unk0, unk1, unk2]
                        possi = [x for x in members if x[0:3] == primeiro_nome_alg[0:3]]
                        x = True
                        await canal.send(unks[humor])
                        
                        if int(humor) == 2:
                            r = True
                        
                        if len(possi) > 0:
                            await canal.send(f"Você quis dizer {possi[0].capitalize()}?")
                            resp = await bot.wait_for('message', check=check, timeout=60)
                            positiveReturn = await verifyterms("pos")
                            positiva = [x[0] for x in positiveReturn]
                            unkReturn = await verifyterms("unk")
                            unk = [x[0] for x in positiveReturn]
                            negReturn = await verifyterms("neg")
                            negativa = [x[0] for x in negReturn]
                            
                            if resp.content.lower() in positiva:
                                como_chegou = f'{possi[0].capitalize()} convidou.'
                                i += 1
                                x = True
                                await asyncio.sleep(1)
                                continue
                            
                            elif resp.content.lower() in negativa:
                                x = True
                                estreseReturn = await selectMilka("CTRL_HUMOR")
                                extress = [x[0] for x in estreseReturn][0] + 1
                                if extress > 7:
                                    extress = 7
                                await updtMilka("CTRL_HUMOR", 'NAME', extress, 'Milka')
                                if r:
                                    i += 1
                                    como_chegou = f'Não sabe o nome de quem convidou.'
                                    await asyncio.sleep(1)
                                continue
                            
                            if resp.content.lower() in unk:
             
                                como_chegou = f'Não sabe o nome de quem convidou.'
                                i += 1
                                x = True
                                await asyncio.sleep(1)
                                continue

                        como_chegou = f'{alguem.content} convidou.'
                        await asyncio.sleep(1)
                        continue

                    como_chegou = alguem.content
                    i += 1
                    x = True
                    await asyncio.sleep(1)
                    continue

                elif i == 1:
                    if len(msg.content) < 3:
                        await canal.send(f"{msg.content}? O que?")
                        x = False
                        continue

                    i += 1
                    x = True
                    como_chegou = msg.content
                    await asyncio.sleep(1)
                    continue
                
                estreseReturn = await selectMilka("HUMOR")
                extress = [x[0] for x in estreseReturn][0]
                cd_n = ''
                conds = {
                    '1':['city pop', '!playjpop'],
                    '2':['rock', '!playrock'],
                    '3':['synth pop', '!playpop'],
                    '4':['oldrock', '!playoldrock'],
                    '5':['músicas de vinil', '!playvinil'],
                    '6':['música alternativa', '!playalternative'],
                    '7':['mpb', '!playMPB'],
                    '8':['lo-fi', '!playlofi'],
                    '9':['chilled hip hop', '!playchill']
                }

                if str(msg.content) not in conds.keys():
                    await canal.send(f"Escolha inválida! Escolha um dos discos disponíveis.")
                    x = False
                    await asyncio.sleep(1)
                    continue

                for x, y in conds.items(): 
                    if x in msg.content and i == 2:
                        cd_n = y
                        estilo_musical = x
                        print('entrei, e o estilo musical é: ', estilo_musical)
                        await ender(name, '', estilo_musical, cd_n[0], cd_n[1])                                                         
        
                i += 1

            await insertUser(
                member.id ,name, como_chegou, int(estilo_musical)
                )

            regsR = await selectInventario(int(estilo_musical), member.id)
            print('regs', regsR,'estilo', estilo_musical, 'idmembro', member.id)

            if len(regsR) > 0:
                await deletarCDsDoInventario(member.id)

            await insertInventario(member.id, int(estilo_musical), 1)
            await canal.send(c2[1].format(member_mention=member.mention))
            await canal.send(c2[2])

            try:
                alguem = await bot.wait_for('message', check=check, timeout=20)
            # Troca de role: remove a role de verificação e dá a de membro
                if alguem.content:
                    role_membro = member.guild.get_role(MEMBER_ROLE)
                    await member.remove_roles(role_inicial)
                    if role_membro:
                        await member.add_roles(role_membro)
                    
                    estreseReturn = await selectMilka("CTRL_HUMOR")
                    extress = [x[0] for x in estreseReturn][0] - 2
                    if extress < 0:
                        extress = 0
                    await updtMilka("CTRL_HUMOR", 'NAME', extress, 'Milka')

            # Apagar o canal de cadastro
                    await verifico_id_lista(str(member.id), 'milka_docs/ids.txt')
                    await canal.delete()
                    if member.id in arquivo2:
                        await deleteUser('pendents', member.id)  # Removendo da lista carregada
            
            except asyncio.TimeoutError:
                role_membro = member.guild.get_role(MEMBER_ROLE)
                await member.remove_roles(role_inicial)
                if role_membro:
                    await member.add_roles(role_membro)

            # Apagar o canal de cadastro
                await canal.delete()
                await verifico_id_lista(str(member.id), 'milka_docs/ids.txt')
                await dellDesk("on_server")

        except asyncio.TimeoutError:
            await canal.send(f"{member.mention}, você demorou muito pra responder. Tente novamente mais tarde.")
            if str(member.id) not in arquivo2:
                await member.kick()
                await canal.delete()
            
            else:
                await canal.delete()
                role_membro = member.guild.get_role(MEMBER_ROLE)
                await member.remove_roles(role_inicial)
                if role_membro:
                    await member.add_roles(role_membro)

        #await verifico_id_lista(str(member.id), 'milka_docs/ids.txt')
        await dellDesk("on_server")
    
@bot.event
async def on_ready():
    asyncio.create_task(calltask())
    print(f'Bot {bot.user} está online!')

@bot.event
async def on_member_join(member):
    await func(member)

async def envio(y, message, i):
    async def inter():
        await asyncio.sleep(2)
        await message.reply(fala_bots.get(y)[i])
    return inter

async def executofala(z, message):
    for x, y in z.items():
        if x == message.content:
            await y()

async def imge(canal):
    with open(random.choice(images2), "rb") as f:
        imagem = discord.File(f)
        return await canal.send(file=imagem)

async def faloUsers(dicionario, message, canal):
    x = random.randint(1,3)

    retorno = await selectMilka("ULT_COM_")
    comodos = [com[0] for com in retorno]
    localmilka = comodos[0]

    conteudo = message.content.lower()

    for palavras_chave, resposta in dicionario.items():
        if all(palavra in conteudo for palavra in palavras_chave) and message.channel.id == localmilka:
            await asyncio.sleep(x)
            await imge(canal)
            await message.channel.send(resposta)
            return  # Garante que só responda uma vez

@bot.event
async def on_message(message):
    global on_channel
    canal = message.channel
    user_id = message.author.id
    user = message.author
    bote = bot.user.display_name.lower()
    # Usando banco de dados você pode trazer todas as informações do usuário aqui para usar nas frases.

    if message.author == bot.user:
        return
    
    conversamuder = {
        f'respondendo Milka.': envio("muder", message, 1),
        "Segunda resposta para Milka.": envio("muder", message, 2),
        "": envio("muder", message, 1),
        "": envio("muder", message, 2),
    }

    respostasMilka = {
        ('milka','jukebox'): falas_chat_comum[0],
        ('milka', 'como vai?'): falas_chat_comum[1],
        ('milka', 'como', 'tocar', 'city pop?'): falas_chat_comum[2],
        ('usa', 'drogas'): falas_chat_comum[3],
        ('milka', 'qual é', 'seu estilo de música preferido?'): falas_chat_comum[4],
        ('tranquilo, camarada', 'cansada', 'dia todo.',): falas_chat_comum[5],
        ('acompanhar', 'muder', 'transmissão',): falas_chat_comum[6],
        ('federação', 'planejando', 'operação', 'articulando',): falas_chat_comum[7],
        ('não', 'você', 'preocupada',): falas_chat_comum[8]
    }

    await executofala(conversamuder, message)
    await faloUsers(respostasMilka, message, canal)
    def deve_enviar(canal_texto, canal_audio_esperado):
        return (
            message.channel.id == canal_texto and
            not (message.author.voice and message.author.voice.channel and message.author.voice.channel.id == canal_audio_esperado)
        )
    async def enviar_mensagem_ambiente(
    canal_id_texto,
    canal_id_audio,
    titulo,
    descricao,
    cor,
    imagem_url,
    message,
    nome_local
):
        user_id = message.author.id

        if not deve_enviar(canal_id_texto, canal_id_audio):
            return

        if message.author.bot:
            return

        mensagens_por_usuario[(user_id, canal_id_texto)] += 1
        count = mensagens_por_usuario[(user_id, canal_id_texto)]

        if count % 20 == 0 or count == 1:
            embed = discord.Embed(
                title=titulo,
                description=descricao.format(name=message.author.name),
                color=cor
        )
            embed.set_image(url=imagem_url)
            embed.add_field(
                name="🎧 Entrar no canal de áudio",
                value=f"[Clique aqui para entrar](https://discord.com/channels/{ID_SERVIDOR}/{canal_id_audio})",
                inline=False
        )
            await message.channel.send(embed=embed)

    # CORREDOR
    await enviar_mensagem_ambiente(
    CANAL_TEXTO_CORREDOR,
    CANAL_AUDIO_CORREDOR,
    "🌆 Corredor",
    "{name}, Perceba ao fundo... de longe você ouve a música que vem do bar enquanto está no corredor banhado pelo neon vermelho.",
    0xFF3C3C,
    "https://i.pinimg.com/736x/53/4e/0b/534e0b642a92c6bd5fe2a12929d899c8.jpg",
    message,
    "corredor"
)

    await enviar_mensagem_ambiente(
    CANAL_TEXTO_EXTERIOR,
    CANAL_AUDIO_EXTERIOR,
    "🌧️ Exterior",
    "{name}, ouça o som da noite... daqui das escadas você pode parar para apreciar a chuva e pássaros cantando.",
    0x00BFFF,
    "https://i.pinimg.com/736x/d4/32/49/d432499aa3a0c6d7bf7315caf4263e21.jpg",
    message,
    "exterior"
)

    await enviar_mensagem_ambiente(
    CANAL_TEXTO_ESCADARIA,
    CANAL_AUDIO_ESCADARIA,
    "🪜 Escadaria",
    "{name}, ficar sentado na escada pode ser relaxante, mas com música a experiência é inexplicável.",
    0x00BFFF,
    "https://i.pinimg.com/736x/17/06/23/170623e163253b2d45666438ffc4e034.jpg",
    message,
    "escadaria"
)

    await enviar_mensagem_ambiente(
    CANAL_TEXTO_BANHEIRO,
    CANAL_AUDIO_BANHEIRO,
    "🚽 Banheiro",
    "{name}, está aproveitando a solidão do banheiro? Você pode curtir ainda mais ativando o som ambiente:",
    0xAAAAAA,
    "https://i.pinimg.com/736x/28/7a/97/287a97445a31f65b973b14614d88816c.jpg",
    message,
    "banheiro"
)

    await enviar_mensagem_ambiente(
    CANAL_TEXTO_SALA,
    CANAL_TELEVISAO,
    "📺 Sala principal",
    "{name}, ligue a TV, talvez para ver um dos canais ou para ter um som de fundo diferente enquanto conversa.",
    0x00BFFF,
    "https://i.pinimg.com/736x/f7/88/eb/f788eb666869d349cc04690acdd6307d.jpg",
    message,
    "sala"
)

    await enviar_mensagem_ambiente(
    CANAL_TEXTO_BALCAO,
    CANAL_AUDIO_JUKEBOX,
    "🍸 Bar",
    "{name}, o som da jukebox te envolve com conforto. No balcão, um momento de pausa, como se o mundo lá fora estivesse longe demais pra importar agora.",
    0x00BFFF,
    "https://i.pinimg.com/736x/2d/bb/87/2dbb8795cb42d2380d14d1e8258700ab.jpg",
    message,
    "balcão"
)

    await enviar_mensagem_ambiente(
    CANAL_TEXTO_MESA_1,
    CANAL_AUDIO_JUKEBOX,
    "🪑mesa-um",
    "{name}, essa mesa perto da entrada sempre tem algo acontecendo. Entre um gole e outro, conversas desconexas e risadas atravessam o ar ao som da jukebox ao fundo.",
    0x00BFFF,
    "https://i.pinimg.com/736x/2d/bb/87/2dbb8795cb42d2380d14d1e8258700ab.jpg",
    message,
    "mesa 1"
)
    
    await enviar_mensagem_ambiente(
    CANAL_TEXTO_MESA_2,
    CANAL_AUDIO_JUKEBOX,
    "🪑mesa-dois",
    "{name}, essa mesa no canto é pra quem prefere observar. Pouca luz, muito silêncio. Só você, seu copo, e a música sussurrando memórias que nunca viveu.",
    0x00BFFF,
    "https://i.pinimg.com/736x/2d/bb/87/2dbb8795cb42d2380d14d1e8258700ab.jpg",
    message,
    "mesa 2"
)

    await enviar_mensagem_ambiente(
    CANAL_TEXTO_MESA_3,
    CANAL_AUDIO_JUKEBOX,
    "🪑mesa-três",
    "{name}, aqui o som pulsa mais alto, direto do coração da jukebox. Quem senta nessa mesa não quer paz — quer presença, ritmo, e talvez um motivo pra não voltar pra casa.",
    0x00BFFF,
    "https://i.pinimg.com/736x/2d/bb/87/2dbb8795cb42d2380d14d1e8258700ab.jpg",
    message,
    "mesa 3"
)
    
    retorno = await selectMilka("ULT_COM_")
    comodos = [com[0] for com in retorno]
    localmilka = comodos[0]
    estreseReturn = await selectMilka("HUMOR")
    estrese = [x[0] for x in estreseReturn][0]
    falasReturn = await selectTalks(estrese)
    falas = [x[0] for x in falasReturn]

    if message.content.lower() == 'milka' and canal.id == localmilka:
        await falo_padrão(falas, canal, msg=message)

    await bot.process_commands(message)

async def falo(extres, fala, canal):
    await canal.send(random.choice(fala[extres]))

async def falo_padrão(frase, canal, estress=None, msg = None):
    global ii
    #i = await valid_extress(extress, await vejoHumor())
    await msg.reply(frase[ii])
    await procuro_pendent(msg.author, str(msg.author.id), canal, msg)

    confirm_ = await bot.wait_for('message', check=lambda m: m.channel == canal)

    if confirm_.content == '>':
        ii += 1
        if ii > 2:
            ii = 0
        await falo_padrão(frase, canal, msg=msg)

async def valid_extress(extres1, extres2):
    estreseReturn = await selectMilka("CTRL_HUMOR")
    extres1 = [x[0] for x in estreseReturn][0]
    
    if extres1 < 3:
        await updtMilka("HUMOR", "NAME", 0, "Milka")
        return 0
    elif 5 > extres1 >= 3:
        await updtMilka("HUMOR", "NAME", 1, "Milka")
        return 1
    elif extres1 >= 5:
        await updtMilka("HUMOR", "NAME", 2, "Milka")
        return 2
    
async def procuro_pendent(author, id, canal, msg= None):
    global perguntados
    pends = await verifyUser('pendents')
    arquivo = [pendente[0] for pendente in pends]
    extressR = await selectMilka('HUMOR')
    extress = [x[0] for x in extressR][0]

    if int(id) in arquivo:
        
        await falo(await valid_extress(extress, await vejoHumor()), falas_pendent, canal)
        await asyncio.sleep(2)
        await func(author, True)
    
    else:
        retorno = await verifyaskeds('askeds', author.id) 
        askeds = [x[0] for x in retorno]
        nome_split = author.display_name.split()
        primeiro_nome = nome_split[0] if len(nome_split) > 1 else author.display_name

        if author.id not in askeds and msg is not None and len(arquivo) > 0 and await valid_extress(extress, await vejoHumor()) < 2 and random.randint(1, 4) == 1:
            await insertAsked(author.id, author.display_name)
            retorno = await verifyaskeds('askeds', author.id) 
            askeds = [x[0] for x in retorno]
            await canal.send(f'Ah, bem lembrado')
            await canal.send(f'Hey, {primeiro_nome}, você tem visto o {bot.get_user(int(random.choice(arquivo))).display_name}?')
            await canal.send(random.choice([f'Se você ver por aí, diga que venha falar comigo', f'Diga pra parar de me evitar.']))

@bot.event
async def on_voice_state_update(member, before, after):
    canal_cargo_map = {
        1365765011464523910: "sala",
        1354311386100011078: "bar",
        1377161141469315132: "escada",
        1376116149472727111: "banheiro",
        1366035560249954315: "exterior",
        1376065935235874948: "corredor",
    }

    # Ignora se não mudou de canal
    if before.channel == after.channel:
        return

    # Se entrou em um canal novo
    if after.channel and after.channel.id in canal_cargo_map:
        nome_novo_cargo = canal_cargo_map[after.channel.id]
        novo_cargo = discord.utils.get(member.guild.roles, name=nome_novo_cargo)

        # Remove todos os cargos do mapa (inclusive se vier de outro canal)
        cargos_para_remover = [
            discord.utils.get(member.guild.roles, name=nome)
            for nome in canal_cargo_map.values()
            if discord.utils.get(member.guild.roles, name=nome) in member.roles
        ]

        if cargos_para_remover:
            await member.remove_roles(*cargos_para_remover)
            print(f"{member.display_name} teve cargos antigos removidos: {[r.name for r in cargos_para_remover]}")

        # Remove "iniciante", se houver
        cargo_iniciante = discord.utils.get(member.roles, name="iniciante")
        if cargo_iniciante:
            await member.remove_roles(cargo_iniciante)
            print(f"{member.display_name} perdeu o cargo 'iniciante'.")

        # Adiciona o cargo novo
        if novo_cargo:
            await member.add_roles(novo_cargo)
            print(f"{member.display_name} recebeu o cargo '{nome_novo_cargo}'.")

    # Se saiu de um canal e não entrou em outro (desconectou)
    elif before.channel and not after.channel:
        print(f"{member.display_name} saiu de {before.channel.name}, manteve o cargo.")
        # Não remove o cargo, mantém acesso até nova entrada

@bot.command()
async def chamar(ctx):
    
    lista_canais = [
    CANAL_AUDIO_BANHEIRO, CANAL_TEXTO_BANHEIRO, CANAL_TEXTO_SALA, CANAL_TELEVISAO, CANAL_TEXTO_BALCAO, CANAL_AUDIO_JUKEBOX,
    CANAL_TEXTO_MESA_1, CANAL_TEXTO_MESA_2, CANAL_TEXTO_MESA_3, CANAL_AUDIO_CORREDOR, CANAL_TEXTO_CORREDOR, CANAL_AUDIO_EXTERIOR, CANAL_TEXTO_EXTERIOR,
    CANAL_AUDIO_ESCADARIA, CANAL_TEXTO_ESCADARIA
    ]

    if ctx.channel.id not in [1365765011464523910, 1354275870956851384]:
        await ctx.channel.send("Você só pode convocar uma reunião na sala principal.")
        return
    
    else:
        for x in lista_canais:
            canal = bot.get_channel(x)
            await canal.send(f"{ctx.author} está chamando a todos para uma reunião na sala principal.")

bot.run(getenv("TOKKEN_ADM_BOT"))