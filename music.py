import asyncio
import discord
import youtube_dl
from discord.ext import commands
from bs4 import BeautifulSoup as bs
import aiohttp

names = {}
urls = {}

cursong = {}
youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': True,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'
}

ffmpeg_options = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.duration = data.get('duration')
        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

def song_duration(s):
    print(s, type(s))
    s = int(s)
    h = s // 3600
    s -= h * 3600
    m = s // 60
    s -= m * 60

    if h == 0:
        dur = f'{m}:{s // 10}{s % 10}'
    else:
        dur = f'{h}:{m // 10}{m % 10}:{s // 10}{s % 10}'
    if dur == '0.0:0.00.0':
        dur = 'stream'
    
    print(dur)
    return dur

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def for_play(self, ctx, *, url='https://www.youtube.com/watch?v=dQw4w9WgXcQ', playlist=False):
        guild = ctx.message.guild

        def check_queue(error):
            if ctx.voice_client:
                if urls[guild.id] != []: 
                
                    source = urls[guild.id].pop(0)
                    names[guild.id].pop(0)

                    make_player = YTDLSource.from_url(source, loop=self.bot.loop, stream=True)
                    try_player = asyncio.run_coroutine_threadsafe(make_player, self.bot.loop)

                    try:
                        player = try_player.result()
                    except:
                        pass
                
                    cursong[guild.id] = f'{player.title} ({song_duration(player.duration)})'

                    coro = ctx.send('Сейчас играет: **{} ({})**'.format(player.title, song_duration(player.duration)))
                    fut = asyncio.run_coroutine_threadsafe(coro, self.bot.loop)
                    try:
                        fut.result()
                    except:
                        pass
                    if ctx.voice_client != None:
                        ctx.voice_client.play(player, after=check_queue)

                else:
                    coro = ctx.send("That's all folks!")
                    cursong[guild.id] = None
                    sec = ctx.voice_client.disconnect()
                    fut2 = asyncio.run_coroutine_threadsafe(sec, self.bot.loop)
                    fut = asyncio.run_coroutine_threadsafe(coro, self.bot.loop)
                    try:
                        fut.result()
                        fut2.result()
                    except:
                        pass
            else:
                cursong[guild.id] = None


        if not guild.id in urls:
            urls[guild.id] = []
            names[guild.id] = []

        if guild.id in cursong and cursong[guild.id] != None:
            player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)

            
            urls[guild.id].append(url)
            names[guild.id].append(f'{player.title} ({song_duration(player.duration)})')
            
            if not playlist:
                await ctx.send(f'**{player.title} ({song_duration(player.duration)})** теперь в очереди')
        else:
            
            player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)

            ctx.voice_client.play(player, after=check_queue)
            await ctx.send('Сейчас играет: **{} ({})**'.format(player.title, song_duration(player.duration)))
            cursong[guild.id] = f'{player.title} ({song_duration(player.duration)})'
    
    async def for_playlist(self, ctx, *, url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as source:
                if source.status == 200:
                    content = await source.read()
                    soup = bs(content, 'lxml')

                    links = soup.find_all('a', attrs={'class':"pl-video-title-link yt-uix-tile-link yt-uix-sessionlink spf-link"})

                    message = await ctx.send('**Начинаю добавлять плейлист**')

                    count = 1
                    for i in links:
                        try:
                            music_source = i['href']
                            new_url = f'youtube.com{music_source}'

                            await self.for_play(ctx=ctx, url=new_url, playlist=True)
                            content = f'**Из плейлиста добавлено песен {count} из {len(links)}**'
                            await message.edit(content=content)
                        except:
                            continue
                        count += 1

    @commands.command()
    async def sr(self, ctx, *, url):
        if '/playlist' in url:
            #await self.for_playlist(ctx=ctx, url=url)
            pass
        else:
            await self.for_play(ctx=ctx, url=url)

    @commands.command()
    async def skip(self, ctx):
        if ctx.voice_client is None:
            pass
        else:
            ctx.voice_client.stop()
    
    @commands.command()
    async def songlist(self, ctx):
        if not ctx.message.guild.id in names:
            names[ctx.message.guild.id] = []
            urls[ctx.message.guild.id] = []

        songs = names[ctx.message.guild.id]

        if songs == []:
            await ctx.send('В очереди ничего нет')
        elif len(songs) > 34:
            await ctx.send(f'Композиций в очереди: {len(songs)}')
        else:
            message = ''

            for i in range(len(songs)):
                song = songs[i]
                message += f'**{i + 1}) {song}** \n'
            embed = discord.Embed(title='Треки в очереди', colour=discord.Colour.green(), description=message)

            await ctx.send(embed=embed)
        
    @commands.command()
    async def cursong(self, ctx):
        if ctx.voice_client is None:
            pass
        else:
            song = cursong[ctx.message.guild.id]
            await ctx.send(f'Сейчас играет: **{song}**')
        
    @commands.command()
    async def pause(self, ctx):
        if ctx.voice_client is None:
            pass
        else:
            ctx.voice_client.pause()

    @commands.command()
    async def resume(self, ctx):
        if ctx.voice_client is None:
            pass
        else:
            ctx.voice_client.resume()

    @commands.command()
    async def clearq(self, ctx):
        guild = ctx.message.guild
        if guild.id in urls:
            urls[guild.id] = []
            names[guild.id] = []
            await ctx.send('Очередь очищена')
    
    @sr.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send(f"{ctx.message.author.mention} Подключись к войсу сначала :clown:")
