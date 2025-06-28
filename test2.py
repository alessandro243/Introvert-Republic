import discord
from discord.ext import commands
from collections import defaultdict
from dotenv import load_dotenv
from os import getenv
import os
import asyncio
import random
import datetime
from milka_docs.falas import falas_pendent, fala_padrao, fala_bots

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
intents.guilds = True
intents.members = True
intents.presences = True
extress = 0
ii = 0

bot = commands.Bot(command_prefix="!", intents=intents)

CANALCADASTRO = 1383461556993527980

ROLEINIT = 1383461909646278656
MEMBER_ROLE = 1386002510736658432

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

apresentacoes = ['Não perambule por aí sem antes falar comigo, novato!', 'Veio se juntar à república? Eu já vi você por aí. Me diga...', 'Lá vamos nós de novo, temo que esse lugar fique mais cheio do que eu gostaria, mas ainda precisamos de mais membros.']
apresentacoes2 = ['Ah... é você, você ficou de me passar algumas informações.', 'Resolveu aparecer pra fazer o registro? Eu tava te procurando.']
images = ['imagens/Milka_1.png']

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
            print(f"{member.name} saiu do server!")
        
            await dellDesk("on_server")
        
        print('tô vivo!')
        
        await asyncio.sleep(10)  # Diminui a frequência pra evitar ser rate-limited

@bot.command()
async def found(ctx):
    canal_user = ctx.channel.id
    bots_on_channel = []
    bots = {
        'milka': 'milka_docs/ultimocomodo.txt',
        'mingau': 'mingau_docs/ultimocomodo.txt',
        'muder': 'muder/ultimocomodo.txt',
}
    for x, y in bots.items():
        with open(y, 'r') as file:
            vari = file.readlines()[0].strip()
        if vari == str(canal_user):
            bots_on_channel.append(x)
    
    if len(bots_on_channel) < 1:
        await ctx.reply("O cômodo está vazio")
        
    else:
        variavel = ''
        for x in bots_on_channel:
            string = f'{x} está no cômodo \n'
            variavel += string

        await ctx.reply(variavel)
    

async def verif():
    guild = bot.get_guild(1354266715785134160)  # Use o ID fixo do servidor
    if not guild:
        print("Guild não encontrada!")
        return

    membros = guild.members

    with open('milka_docs/ids.txt', 'r') as file:
        arquivo = [linha.strip() for linha in file.readlines()]  # Tira o '\n'

    with open('milka_docs/pendents.txt', 'r') as file:
        arquivo2 = [linha.strip() for linha in file.readlines()]

    for x in membros:
        if str(x.id) not in arquivo and not x.bot:
            print(f"O usuário {x} não está registrado")
            if str(x.id) not in arquivo2:
                with open('milka_docs/pendents.txt', 'a') as file:
                    file.write(str(x.id)+'\n')

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

def faco(x, y):
    def inter():
        agora = datetime.datetime.now()
        if agora.hour == x:
            with open('milka_docs/ultimocomodo.txt', 'w') as file:
                file.write(str(y))
    return inter

async def calltask():
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

    possibles = {
            str(hora_milka_balcao): faco(hora_milka_balcao, CANAL_TEXTO_BALCAO),
            str(hora_milka_sala): faco(hora_milka_sala, CANAL_TEXTO_SALA),
            str(hora_milka_exterior): faco(hora_milka_exterior, CANAL_TEXTO_EXTERIOR),
            str(hora_milka_corredor): faco(hora_milka_corredor, CANAL_TEXTO_CORREDOR),
            str(hora_milka_mesa): faco(hora_milka_mesa, random.choice(mesas))
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
                y()

        await achoBot_id(comodos_dos_bots ,bots_no_canal, 'milka_docs/ultimocomodo.txt', 'muder/ultimocomodo.txt', 'mingau_docs/ultimocomodo.txt')
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
        if not os.path.exists('milka_docs/hoje.txt'):
            with open('milka_docs/hoje.txt', 'w') as f:
                f.write('0')

        # Lê o último dia que a Milka disparou
        with open('milka_docs/hoje.txt', 'r') as f:
            content = f.read().strip()
            try:
                dia_executado = int(content)
            except ValueError:
                dia_executado = 0  # Caso o arquivo esteja corrompido
    
        # Se for o horário alvo e ainda não executou hoje
        if hora_atual == target_hour and dia_executado != hoje:
            #envio = 2
            hora_milka_coversation, hora_milka_coversation2 = random.sample(range(24), 2)
            minute_milka_conversation, minute_milka_conversation2 = random.sample(range(60), 2)
            # ✅ Faz a verificação de pendentes ANTES de disparar as mensagens
            await verif()

            guild = bot.get_guild(1354266715785134160)
            if guild:
                try:
                    with open('milka_docs/pendents.txt', 'r') as file:
                        pendentes = [linha.strip() for linha in file.readlines() if linha.strip()]

                    for user_id in pendentes:
                        membro = guild.get_member(int(user_id))
                        if membro:
                            try:
                                await membro.send(f"{membro.display_name}, preciso falar com você")
                                await membro.send(f"Não sei como você passou por mim sem se registrar. Então, não me faça perder tempo e venha falar comigo!")
                            except Exception as e:
                                print(f"Erro ao tentar mandar mensagem para {membro.display_name}: {e}")

                    # Atualiza o dia de execução para hoje
                    with open('milka_docs/hoje.txt', 'w') as f:
                        f.write(str(hoje))

                    print(f"Milka disparou as mensagens do dia {hoje}.")
                except Exception as e:
                    print(f"Erro durante o envio das mensagens: {e}")

        # Dorme 60 segundos antes de verificar de novo
        await asyncio.sleep(5)

async def escrevoHumor(x):
    with open('milka_docs/humor.txt', 'w') as file:
        file.write(str(x))

async def vejoHumor():
    with open('milka_docs/humor.txt', 'r') as file:
        return int(file.read())

async def func(member, pedente=False):
    global extress
    
    i = 0
    i2 = 0
    i3 = 0

    with open('milka_docs/pendents.txt', 'r') as file2:
        arquivo2 = [linha.strip() for linha in file2 if linha.strip()]

    name = member.display_name
    primeiro_nome = name.split()[0] if len(name.split()) > 1 else name
    como_chegou = ''
    estilo_musical = ''

    # Criar canal privado para o membro com permissões exclusivas
    overwrites = {
            member.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            member: discord.PermissionOverwrite(read_messages=True),
            bot.user: discord.PermissionOverwrite(read_messages=True)
    }
    canal = await member.guild.create_text_channel(f'cadastro-{primeiro_nome}', overwrites=overwrites)
    
    role_inicial = member.guild.get_role(ROLEINIT)

    convidado = ['não conheço', 'não vi', 'esqueci', 'desconhecido', 'não reconheci', 'não lembro', 'não conhecia', 'não deu pra ver', ' não deu tempo de ver','me convidaram', 'me convidou', 'deram um convite', 'um convite de', 'um amigo', 'uma amiga', 'o convite', 'um convite']
    validlist = ['sou', 'sou sim', 'yes', 'é', 'é sim', 'e n', 'sim', 'isso', 'isso mesmo', 'no', 'not', 'não', 's', 'n', 'não é', 'é não','nao', 'é nao']
    forget = ['não conheço', 'não vi', 'esqueci', 'desconhecido', 'não reconheci', 'não me lembro', 'não lembro', 'não conhecia', 'não deu pra ver', ' não deu tempo de ver', 'não consegui ver']
    perguntas = [
            f"Aqui diz que seu nome é {member.display_name}? diga sim, caso sejá e não, caso não.",
            f"Como você ficou sabendo da república?",
            f"Entre esses qual você diria que mais gosta?\n[1] jpop\n[2] rock\n[3] pop\n[4] oldrock\n[5] vinil\n[6] alternative\n[7] mpb\n[8] lofi",
    ]
    task1 = asyncio.create_task(isOn(member, canal))
    task1.set_name("on_server")
    if role_inicial:
        await member.add_roles(role_inicial)
        await canal.send(random.choice(apresentacoes if str(member.id) not in arquivo2 else apresentacoes2)) if not pedente else ...

        async def imge():
            with open(random.choice(images), "rb") as f:
                imagem = discord.File(f)
                return await canal.send(file=imagem)

        async def msge(x=False):
            if not x:
                return '-'
            await imge()
            print(member.status)
            return await canal.send(perguntas[i])
        
        async def milk(name, eu, st):
            if eu.lower() == 'milka':
                await canal.send("Eu? eu não te convidei... O Cordano deve ter posto alguém pra te vigiar.")
                await asyncio.sleep(1)
                eu = f'{name} alegou que foi convidado por min.'
                return eu
            
            elif any(x in eu.lower() for x in forget):
                await canal.send("Então você não consegue me dizer, entendi...")
                await asyncio.sleep(1)
                eu = f'{name} não lembra ou não sabe quem lhe deu o convite, suspeito! Fiquem de olho!'
                return eu
            
            else:
                st = f' convidou.'
                eu = eu + st
                return eu

        async def ender(nome, convite, estilo):
            
            if extress < 3:
                await escrevoHumor(0)

            elif 5 > extress >= 3:
                await escrevoHumor(1)
            
            elif extress >= 5:
                await escrevoHumor(2)

            extress_ = await vejoHumor()

            if extress_ == 0:
                await imge()
                await canal.send('Isso vai ficar ótimo na jukebox')
                await canal.send(f'Então é isso, {nome}, você é oficialmente um membro da república')
                await asyncio.sleep(1)
                await canal.send(f'Pegue esse cd de {estilo}, você pode usa-lo na jukebox.')
                await asyncio.sleep(1)
                await canal.send(f'O bar é só para membros, exceto nos domingos, quando Cordano abre para o público.')
                await asyncio.sleep(1)
                await canal.send(f'Só de pensar naquela falação já fico estreçada, enfim, bom ter você aqui.')
                await asyncio.sleep(1)
                print("antes", extress)

            elif extress_ == 1:
                await imge()
                await canal.send('Entendi...')
                await canal.send(f'Terminamos aqui. Você pode ir, leva esse cd com vc.')
                await asyncio.sleep(1)
                await canal.send(f'Se precisar de alguma coisa fale com Cordano no bar')
                await asyncio.sleep(1)
                await canal.send(f'Ou veja se o Cordano tá por aí. toma, leva esse cd.')
                await asyncio.sleep(1)
                print("antes", extress)

            elif extress_ == 2:
                await imge()
                await canal.send('Só podia ser...')
                await canal.send(f'Acabamos')
                await asyncio.sleep(1)
                await canal.send(f'Leva esse cd e encontre um lugar pra vc. Pra min já deu')
                await asyncio.sleep(1)
                await canal.send(f'Eu preciso de uma bebida... CORDANO!!!')
                await asyncio.sleep(1)
                print("antes", extress)

        respostas = []
        
        with open('milka_docs/ids.txt', 'r') as file:
            arquivo = [linha.strip() for linha in file.readlines() if linha.strip()]
            
            if str(member.id) in arquivo:
                try:
                    await canal.send(f"Eu já vi você por aqui antes... {member.display_name}, você voltou...")
                    await asyncio.sleep(1) 
                    await canal.send("Esqueceu alguma coisa?")
                    await asyncio.sleep(1) 
                    await canal.send("Seu espaço no bar ainda está guardado.")
                    await canal.send("Agora você seguirá para a república, pronto?")
                    alguem2 = await bot.wait_for('message', check=lambda m: m.channel == canal, timeout=20)

                    if alguem2.content:
                    
                        role_membro = member.guild.get_role(MEMBER_ROLE)
                        await member.remove_roles(role_inicial)
                        if role_membro:
                            await member.add_roles(role_membro)
                
                        await canal.delete()
                        await dellDesk('on_server')

                        extress -= 1
                        if extress < 0:
                            extress = 0
                        print(extress)
                        return
                
                except asyncio.TimeoutError:
                    role_membro = member.guild.get_role(MEMBER_ROLE)
                    await member.remove_roles(role_inicial)
                    if role_membro:
                        await member.add_roles(role_membro)

            # Apagar o canal de cadastro
                    await canal.delete()
                    print(respostas)
                    await verifico_id_lista(str(member.id), 'milka_docs/ids.txt')
                    await dellDesk("on_server")
                    print(extress)

        def check(m):
            return m.author == member and m.channel == canal

        try:
            x = True
            while i < len(perguntas):
                await msge(x)
                msg = await bot.wait_for('message', check=check, timeout=120)

                if '?' in msg.content:
                    await canal.send('Eu faço as perguntas, aqui! Pare de fugir e me fala...')
                    x = False
                    continue

                if i == 0 and msg.content.lower() in validlist:

                    if msg.content.lower() in ['sou', 'sou sim', 's', 'sim', 'é', 'é sim', 'isso', 'isso mesmo', 'e s']:
                        await canal.send('...')
                        i += 1
                        x = True
                        respostas.append(name)
                        continue

                    elif msg.content.lower() in ['no', 'not','não', 'n', 'não é','e n', 'nao', 'é n', 'é nao']:
                        if i2 < 1:
                            await canal.send('Não?')
                            i2 += 1
                            x = False
                            await asyncio.sleep(1)
                            continue

                        elif i2 == 1:
                            i2 += 1
                            await imge()
                            await canal.send('Escuta aqui, Eu não gosto que mintam pra min! Você quer que tenhamos problemas aqui?')
                            await asyncio.sleep(2)
                            await canal.send(f'Você é ou não o {primeiro_nome}?')
                            x = False
                            extress += 1
                            await asyncio.sleep(1)
                            continue

                        else:
                            await imge()
                            await canal.send(f'Tá bom, engraçadinho, nós dois sabemos que seu nome é {member.display_name}!')
                            await asyncio.sleep(2)
                            await canal.send('Você quer que eu mencione seu endereço também? O de toda a sua família? Eu sei quantos dentes seu avozinho perdeu esse ano!')
                            await asyncio.sleep(2)
                            await canal.send(f'Francamente... Vai ser {member.display_name}!')
                            resp = member.display_name
                            i2 = 0
                            i += 1
                            x = True
                            extress += 2
                            respostas.append(name)
                            continue

                elif i == 0 and msg.content.lower() not in validlist:
                    if i3 < 1:
                        await canal.send(f'O que?... Presta ateção!')
                        await asyncio.sleep(1)
                        await canal.send(f'me fala, o teu primeiro nome é {primeiro_nome}?')
                        i3 += 1
                        x = False
                        extress += 1
                        continue

                    elif i3 == 1:
                        await imge()
                        await canal.send('Um dia eu vou me cansar disso...')
                        await asyncio.sleep(2)
                        await canal.send(f'É {primeiro_nome} ou não?')
                        i3 += 1
                        x = False
                        extress += 1
                        continue
                    else:
                        await imge()
                        await canal.send('Vocês me cansam!')
                        resp = member.display_name
                        i3 = 0
                        i += 1
                        x = True
                        extress += 2
                        respostas.append(name)
                        continue
                    
                xi = 'QR code'
                if i == 1 and xi.lower() in msg.content.lower():
                    como_chegou = msg.content
                    i += 1
                    x = True
                    respostas.append(como_chegou)
                    await canal.send('Em um papel que alguém deixou? interessante')
                    await asyncio.sleep(2)
                    await canal.send('Não é que funcionou mesmo, direi ao Mikhail...')
                    await asyncio.sleep(2)
                    continue

                elif i == 1 and any(x in msg.content.lower() for x in convidado):
                    alguem = ''
                    st = f''
                    await canal.send('O nome de quem te convidou?')
                    alguem = await bot.wait_for('message', check=check, timeout=60)
                    alguem.content = await milk(primeiro_nome, alguem.content, st)
                    respostas.append(alguem.content)
                    i += 1
                    x = True
                    await asyncio.sleep(1)
                    continue

                if i == 2 and '1' in msg.content:
                    ritmo = '01'
                    estilo_musical = 'jpop'
                    await ender(name, '', estilo_musical)
                    respostas.append(ritmo)

                elif i == 2 and '2' in msg.content:
                    ritmo = '02'
                    estilo_musical = 'rock'
                    await ender(name, '', estilo_musical)
                    respostas.append(ritmo)

                elif i == 2 and '3' in msg.content:
                    ritmo = '03'
                    estilo_musical = 'pop'
                    await ender(name, '', estilo_musical)
                    respostas.append(ritmo)

                elif i == 2 and '4' in msg.content:
                    ritmo = '04'
                    estilo_musical = 'oldrock'
                    await ender(name, '', estilo_musical)
                    respostas.append(ritmo)

                elif i == 2 and '5' in msg.content:
                    ritmo = '05'
                    estilo_musical = 'vinil'
                    await ender(name, '', estilo_musical)
                    respostas.append(ritmo)

                elif i == 2 and '6' in msg.content:
                    ritmo = '06'
                    estilo_musical = 'alternative'
                    await ender(name, '', estilo_musical)
                    respostas.append(ritmo)

                elif i == 2 and '7' in msg.content:
                    ritmo = '07'
                    estilo_musical = 'mpb'
                    await ender(name, '', estilo_musical)
                    respostas.append(ritmo)

                elif i == 2 and '8' in msg.content:
                    ritmo = '08'
                    estilo_musical = 'lofi'
                    await ender(name, '', estilo_musical)
                    respostas.append(ritmo)

                i += 1

            # Aqui você pode salvar as respostas se quiser
            await canal.send(f"{member.mention}, Terminamos.")
            await canal.send(f"Agora você seguirá para a república, pronto?")
            try:
                alguem = await bot.wait_for('message', check=check, timeout=20)
            # Troca de role: remove a role de verificação e dá a de membro
                if alguem.content:
                    role_membro = member.guild.get_role(MEMBER_ROLE)
                    await member.remove_roles(role_inicial)
                    if role_membro:
                        await member.add_roles(role_membro)
                    extress -= 1
                    if extress < 0:
                        extress = 0

            # Apagar o canal de cadastro
                    await verifico_id_lista(str(member.id), 'milka_docs/ids.txt')
                    await canal.delete()
                    if str(member.id) in arquivo2:
                        arquivo2.remove(str(member.id))  # Removendo da lista carregada

                # Agora, reescreve o arquivo com o conteúdo novo (sem o ID removido)
                        with open('milka_docs/pendents.txt', 'w') as file2:
                            for linha in arquivo2:
                                file2.write(f"{linha}\n")

            except asyncio.TimeoutError:
                role_membro = member.guild.get_role(MEMBER_ROLE)
                await member.remove_roles(role_inicial)
                if role_membro:
                    await member.add_roles(role_membro)

            # Apagar o canal de cadastro
                await canal.delete()
                print(respostas)
                await verifico_id_lista(str(member.id), 'milka_docs/ids.txt')
                await dellDesk("on_server")
                extress -= 1
                if extress < 0:
                    extress = 0
                print(extress)

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

@bot.event
async def on_message(message):
    global on_channel
    canal = message.channel
    user_id = message.author.id

    if message.author == bot.user:
        return

    if message.content == f'respondendo Milka.':
        await asyncio.sleep(2)
        await message.reply(fala_bots.get("muder")[1])
    
    if message.content == "Segunda resposta para Milka.":
        await asyncio.sleep(2)
        await message.reply(fala_bots.get("muder")[2])

    def deve_enviar(canal_texto, canal_audio_esperado):
        return (
            message.channel.id == canal_texto and
            not (message.author.voice and message.author.voice.channel and message.author.voice.channel.id == canal_audio_esperado)
        )

    # CORREDOR
    if deve_enviar(CANAL_TEXTO_CORREDOR, CANAL_AUDIO_CORREDOR):
        if message.author.bot:
            return
        mensagens_por_usuario[(user_id, CANAL_TEXTO_CORREDOR)] += 1
        count = mensagens_por_usuario[(user_id, CANAL_TEXTO_CORREDOR)]
        if count % 20 == 0 or count == 1:
            embed = discord.Embed(
                title="🌆 Corredor",
                description=f"{message.author.name}, Perceba ao fundo... de longe você ouve a música que vem do bar enquanto está no corredor banhado pelo neon vermelho.",
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
                title=": 🪜 Escadaria",
                description=f"{message.author.name}, ficar sentado na escada pode ser relaxante, mas com música a experiência é inexplicável.",
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
                title="📺 Sala pricipal",
                description=f"{message.author.name}, ligue a TV, talvez para ver um dos canais ou para ter um som de fundo diferente enquanto conversa.",
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
        if message.author.bot:
            return
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
    
    with open('milka_docs/ultimocomodo.txt', 'r') as file:
        localmilka = file.read()

    if message.content.lower() == 'milka' and canal.id == int(localmilka):
        await falo_padrão(fala_padrao, canal, msg=message)

    await bot.process_commands(message)

async def falo(extres, fala, canal):
    await canal.send(random.choice(fala[extres]))

async def falo_padrão(frase, canal, estress=None, msg = None):
    global ii
    i = await valid_extress(extress, await vejoHumor())
    await msg.reply(frase[i][ii])
    await procuro_pendent(msg.author, str(msg.author.id), 'milka_docs/pendents.txt', canal, msg)

    confirm_ = await bot.wait_for('message', check=lambda m: m.channel == canal)
    
    if confirm_.content == '>':
        ii += 1
        if ii > 2:
            ii = 0
        await falo_padrão(frase, canal, msg=msg)


async def valid_extress(extres1, extres2):
    if extres1 < 3:
        extres2 = 0

    elif 5 > extres1 >= 3:
        extres2 = 1
            
    elif extres1 >= 5:
        extres2 = 2
    
    return extres2

#extress_
async def procuro_pendent(author, id, doc, canal, msg= None):
    global extress, perguntados

    with open(doc, 'r') as file:
        arquivo = [x.strip() for x in file.readlines()]
    
    if str(id) in arquivo:
        
        await falo(await valid_extress(extress, await vejoHumor()), falas_pendent, canal)
        await asyncio.sleep(2)

        await func(author, True)
    
    else:
        with open('milka_docs/perguntados.txt', 'r') as file:
            nome_split = author.display_name.split()
            primeiro_nome = nome_split[0] if len(nome_split) > 1 else author.display_name
            perguntados = [x.strip() for x in file.readlines()]
        if msg is not None and len(arquivo) > 0 and await valid_extress(extress, await vejoHumor()) < 2 and author.display_name not in perguntados and random.randint(1, 4) == 1:
            
            with open('milka_docs/perguntados.txt', 'w') as file:
                file.write("")
                perguntados.append(author.display_name)

            with open('milka_docs/perguntados.txt', 'a') as file:
                for x in perguntados:
                    file.write(x + '\n')

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



# Coloque seu token aqui
bot.run(getenv("TOKKEN_ADM_BOT"))