#fucao di
@bot.command()
async def disconnect(ctx):
    if not ctx.author.voice or not ctx.guild.voice_client:
        return

    if ctx.author.voice.channel != ctx.guild.voice_client.channel:
        return
    if ctx.voice_client:
        await ctx.voice_client.disconnect()

@bot.command()
async def testmsg(ctx):
    channel = bot.get_channel(TARGET_TEXT_CHANNEL_ID)
    if channel:
        await channel.send("✅ Teste de envio no chat vinculado ao canal de voz!")
    else:
        await ctx.send("❌ Não achei o canal de texto para enviar a mensagem.")

#func fita

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
    

    with open('musics.txt', 'w') as file:
        file.write(caminho + '\n')
        file.write(os.path.basename(caminho) + '\n')

    with open('estadojuke\\nome.txt', 'w') as file:
        file.write(caminho)

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

    # Espera o chiado terminar
    while voice_client_global.is_playing():
        await asyncio.sleep(1)

    # Para o cronômetro ao fim do áudio
    cronometro_task.cancel()
    with open("estadojuke\\cronometro.txt", "w") as f:
        f.write("0")  # reseta ao fim (opcional)

    #canais manuais

    @bot.command()
async def canal01(ctx):
    if not ctx.author.voice or not ctx.guild.voice_client:
        #await ctx.send("❌ Você ou o bot não estão em um canal de voz.")
        return

    # Verifica se estão no MESMO canal
    if ctx.author.voice.channel != ctx.guild.voice_client.channel:
        #await ctx.send("⚠️ Você precisa estar no mesmo canal de voz que o bot para usar esse comando.")
        return
    await trocar.invoke(ctx, canal_nome='canal 01')

@bot.command()
async def canal02(ctx):
    if not ctx.author.voice or not ctx.guild.voice_client:
        #await ctx.send("❌ Você ou o bot não estão em um canal de voz.")
        return

    # Verifica se estão no MESMO canal
    if ctx.author.voice.channel != ctx.guild.voice_client.channel:
        #await ctx.send("⚠️ Você precisa estar no mesmo canal de voz que o bot para usar esse comando.")
        return
    await trocar.invoke(ctx, canal_nome='canal 02')

@bot.command()
async def canal03(ctx):
    if not ctx.author.voice or not ctx.guild.voice_client:
        #await ctx.send("❌ Você ou o bot não estão em um canal de voz.")
        return

    # Verifica se estão no MESMO canal
    if ctx.author.voice.channel != ctx.guild.voice_client.channel:
        #await ctx.send("⚠️ Você precisa estar no mesmo canal de voz que o bot para usar esse comando.")
        return
    await trocar.invoke(ctx, canal_nome='canal 03')

#canais n manuais

'canal 01', 'canal 02', 'canal 03', 'canal 04', 'canal 05', 'canal 06'

#condição canal 06

if canal_nome == 'canal 06':
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

#func canal secreto

def canal06():
    agora = datetime.datetime.now()
    
    if agora.hour == 8 and 2 <= agora.minute <= 3:
        return 1
    
    return 0

bot.run(TOKEN)