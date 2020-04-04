import asyncio
import discord
import youtube_dl
from discord.ext import commands
from bs4 import BeautifulSoup as bs
import aiohttp

queues = {}
cursong = {}
youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
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

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def for_play(self, ctx, *, url='https://www.youtube.com/watch?v=dQw4w9WgXcQ'):
        guild = ctx.message.guild

        def check_queue(error):
            if queues[guild.id] != []: 
                
                player = queues[guild.id].pop(0)
                
                cursong[guild.id] = player.title

                coro = ctx.send('Сейчас играет: {}'.format(player.title))
                fut = asyncio.run_coroutine_threadsafe(coro, self.bot.loop)
                try:
                    fut.result()
                except:
                    pass

                ctx.voice_client.play(player, after=check_queue)
            else:
                coro = ctx.send("That's all folks!")
                sec = ctx.voice_client.disconnect()
                fut2 = asyncio.run_coroutine_threadsafe(sec, self.bot.loop)
                fut = asyncio.run_coroutine_threadsafe(coro, self.bot.loop)
                try:
                    fut.result()
                    fut2.result()
                except:
                    pass
        if not guild.id in queues:
            queues[guild.id] = []

        if (ctx.voice_client.is_playing() or queues[guild.id] != []): 
            player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)

            
            queues[guild.id].append(player)
            

            await ctx.send(f'{player.title} теперь в очереди')
        else:
            
            player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
            ctx.voice_client.play(player, after=check_queue)
            await ctx.send('Сейчас играет: {}'.format(player.title))
            cursong[guild.id] = player.title
    
    @commands.command()
    async def sr(self, ctx, *, url):
        await self.for_play(ctx=ctx, url=url)

    @commands.command()
    async def skip(self, ctx):
        ctx.voice_client.stop()
    
    @commands.command()
    async def songlist(self, ctx):
        if not ctx.message.guild.id in queues:
            queues[ctx.message.guild.id] = []
        if queues[ctx.message.guild.id] == []:
            await ctx.send('В очереди ничего нет')
        else:
            message = ''

            for i in range(len(queues[ctx.message.guild.id])):
                song = queues[ctx.message.guild.id][i]
                message += f'{i + 1}) {song.title} \n'

            await ctx.send(message)
        
    @commands.command()
    async def cursong(self, ctx):
        song = cursong[ctx.message.guild.id]
        await ctx.send(f'Сейчас играет: {song}')
        
    @commands.command()
    async def pause(self, ctx):
        ctx.voice_client.pause()

    @commands.command()
    async def resume(self, ctx):
            ctx.voice_client.resume()

    
    @sr.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send(f"{ctx.message.author.mention} Подключись к войсу сначала, дурачок")
