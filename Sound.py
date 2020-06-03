import discord
from discord.ext import commands
from discord.utils import get
import youtube_dl
import os
import shutil

bot_token = 'bot_token'
bot_command_prefix = 'NS-'
bot = commands.Bot(command_prefix=bot_command_prefix)


@bot.event
async def on_ready():
    print("Sound_Online ---> Logged in as: " + bot.user.name)


@bot.command(pass_context=True, aliases=['j', 'jo'])
async def join(ctx):
    global voice
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.connect():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
        print(f'The bot has connected to {channel}.')

    await ctx.send(f'Join {channel}')


@bot.command(pass_context=True, aliases=['l', 'lea'])
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.connect():
        await voice.disconnect()
        print(f'The bot has leave to {channel}.')
        await ctx.send(f'Leave {channel}')
    else:
        print("Bot was told to leave voice channel, but was not in one.")
        await ctx.send("Dont think I was on some voice channel")


@bot.command(pass_context=True, aliases=['p', 'pl'])
async def play(ctx, url: str):
    def check_q():
        q_infile = os.path.isdir("./Queue")
        if q_infile is True:
            Dir = os.path.abspath(os.path.realpath("Queue"))
            length = len(os.listdir(Dir))
            still_q = length - 1
            try:
                first_file = os.listdir(Dir)[0]
            except:
                print("No more song(s).")
                queues.clear()
                return
            main_location = os.path.dirname(os.path.realpath(__file__))
            song_path = os.path.abspath(os.path.realpath("Queue") + "\\" + first_file)
            if length != 0:
                print("Song done, playing next queued.\n")
                print(f"Songs still in queue: {still_q}")
                song_there = os.path.isfile("song.mp3")
                if song_there:
                    os.remove("song.mp3")
                shutil.move(song_path, main_location)
                for file in os.listdir("./"):
                    if file.endswith(".webm"):
                        os.rename(file, 'song.mp3')
                voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: check_q())
                voice.source = discord.PCMVolumeTransformer(voice.source)
                voice.source.volume = 1
            else:
                queues.clear()
                return
        else:
            queues.clear()
            print("No any song were queued before the ending of the last song\n")

    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
            queues.clear()
            print("Removed old song(s) file")
    except PermissionError:
        print("Trying to delete song file but its being played.")
        await ctx.send(f'Error music playing.')
        return

    q_in_file = os.path.isdir("./Queue")
    try:
        q_folder = "./Queue"
        if q_in_file is True:
            print("Removed old Queue Folder.")
            shutil.rmtree(q_folder)
    except:
        print("No old Queue folder.")

    await ctx.send("Getting every thing ready now")
    voice = get(bot.voice_clients, guild=ctx.guild)
    ydl_opts = {
        'format': 'bestaudio/best',
        'extractaudio': True,
        'audioformat': 'mp3',
        'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
        'restrictfilenames': True,
        'noplaylist': True,
        'nocheckcertificate': True,
        'ignoreerrors': False,
        'logtostderr': False,
        'quiet': True,
        'no_warnings': True,
        'default_search': 'auto',
        'source_address': '0.0.0.0',
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print("Downloading audio now....\n")
        ydl.download([url])

    for file in os.listdir():
        if file.endswith(".webm"):
            name = file
            os.rename(file, 'song.mp3')
    voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: check_q())
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 1

    nname = name.rsplit("-", 2)
    await ctx.send(f"Playing now: {nname}")
    print("playing")


@bot.command(pass_context=True, aliases=['s', 'st'])
async def stop(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)

    queues.clear()


    if voice and voice.is_playing():
        print("Music stoped.")
        voice.pause()
        await ctx.send(" Stoped playing now")
    else:
        print("Music not playing")
        await ctx.send("Music not playing")


@bot.command(pass_context=True, aliases=['r', 're'])
async def resume(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_paused():
        print("Resume playing now")
        voice.resume()
        await ctx.send("Resume playing music now")
    else:
        print("Music not playing")
        await ctx.send("Music not playing")


queues = {}


@bot.command(pass_context=True, aliases=['q', 'qu'])
async def queue(ctx, url: str):
    Queue_in = os.path.isdir("./Queue")
    if Queue_in is False:
        os.mkdir("Queue")
    Dir = os.path.abspath(os.path.realpath("Queue"))
    q_num = len(os.listdir(Dir))
    q_num += 1
    add_q = True
    while add_q:
        if q_num in queues:
            q_num += 1
        else:
            add_q = False
            queues[q_num] = q_num
    q_path = os.path.abspath(os.path.realpath(("Queue") + f"\song{q_num}.%(ext)s"))
    ydl_opts = {
        'format': 'bestaudio/best',
        'extractaudio': True,
        'audioformat': 'mp3',
        'outtmpl': q_path,
        'restrictfilenames': True,
        'noplaylist': True,
        'nocheckcertificate': True,
        'ignoreerrors': False,
        'logtostderr': False,
        'quiet': True,
        'no_warnings': True,
        'default_search': 'auto',
        'source_address': '0.0.0.0',
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print("Downloading audio now....\n")
        ydl.download([url])
    await ctx.send("Adding song " + str(q_num) + " to the queue.")

    print("Song added to queue.\n")


bot.run(bot_token)
