import discord
from discord.ext import commands
from moviepy.editor import *
from pytube import YouTube
import os

client = commands.Bot(command_prefix="!")

#Apertura del file in cui è salvato il token e salvataggio variabile
f = open("token.txt", 'r')
TOKEN = f.readline()
f.close()

@client.event
async def on_ready():
    print("Bot Online")

@client.command()
async def play(ctx, url : str):
    print("!play")
    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
    except PermissionError:
        await ctx.send("Attendi che la musica in riproduzione finisca o usa il comando !stop")
        return

    voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='Music')
    await voiceChannel.connect()
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)

    #Get youtube videos with highest resolution
    yt = YouTube(url)
    #ys = yt.streams.filter(only_audio=True,file_extension='mp4').first()
    ys = yt.streams.get_lowest_resolution()

    #Get title name of video
    titleName = ys.title.replace('.', '').replace(',', '').replace(':', '')

    #Add .mp4 to tile name
    newTitleName = titleName + ".mp4"

    print("Download Audio Start")

    #Download it in Downloads\Videos
    ys.download('Downloads\Audio')

    #Change the current directory
    cwd = os.getcwd()
    os.chdir(cwd + 'Downloads\Audio')

    #Trasform mp4 file into mp3 file
    videoclip = VideoFileClip(newTitleName)
    audioclip = videoclip.audio
    audioclip.write_audiofile('song.mp3')
    audioclip.close()
    videoclip.close()

    #Remove .mp4 original file
    os.remove(newTitleName) 

    print('Youtube Audio Download Complete in "Downloads\Audio"')
    voice.play(discord.FFmpegPCMAudio("song.mp3"))


@client.command()
async def leave(ctx):
    print('!leave')
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_connected():
        await voice.disconnect()
        await ctx.send("Sono uscito dalla chat vocale")
    else:
        await ctx.send("Non sono in nessun canale vocale")


@client.command()
async def pause(ctx):
    print('!pause')
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
        await ctx.send("Audio stoppato")
    else:
        await ctx.send("Non sto riproducendo nessun audio")


@client.command()
async def resume(ctx):
    print('!resume')
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
        await ctx.send("Audio ripartito")
    else:
        await ctx.send("Non ci sono audio in pausa")


@client.command()
async def stop(ctx):
    print('!stop')
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    voice.stop()
    await ctx.send("Audio tolto")

client.run(TOKEN)