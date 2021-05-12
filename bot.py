import discord
from discord.ext import commands
#from DiscordBotsOrgAPI import DiscordBotsOrgAPI, dbl_setup
#from DiscordBotsOrgAPI import dbl_setup
import config
from VkThings import VkThings
import music
from random import randint, choice
import wikipediaapi
from bs4 import BeautifulSoup as bs
import pyowm
from DataBase import DataBase
import asyncio
import youtube_dl
from io import BytesIO


client = commands.Bot(commands.when_mentioned_or("!"))
client.remove_command('help')

#dbl_setup(client)
from discord.ext import tasks

import dbl

# This example uses tasks provided by discord.ext to create a task that posts guild count to top.gg every 30 minutes.

dbl_token = config.DBL_TOKEN  # set this to your bot's top.gg token
client.dblpy = dbl.DBLClient(client, dbl_token)

@tasks.loop(minutes=30)
async def update_stats():
    """This function runs every 30 minutes to automatically update your server count."""
    try:
        print(config.border)
        await bot.dblpy.post_guild_count()
        print(f'Posted server count ({bot.dblpy.guild_count})')
    except Exception as e:
        print('Failed to post server count\n{}: {}'.format(type(e).__name__, e))
    print(config.border)

update_stats.start()

@client.event
async def on_ready():
    print(config.border)
    print(f'{client.user} снова в игре')
    print(config.border)
    bot_activity = discord.Activity(name='Жыве Беларусь !help', type=discord.ActivityType.listening)
    await client.change_presence(activity=bot_activity)
    guilds = client.guilds
    
    message = f'{len(guilds)} - кол-во серверов'
    vk = VkThings()
    await vk.sendVk(message)

@client.event
async def on_guild_join(guild):
    print(config.border)
    print(f'Новый: {guild.name}')
    print(config.border)

@client.event
async def on_guild_remove(guild):
    print(config.border)
    print(f'Ушёл: {guild.name}')
    print(config.border)

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return

@client.command()
async def hello(ctx):
    async with ctx.typing():
        await ctx.send(f'{ctx.message.author.mention} ты што идиот??? Ты совсем жизнью контуженный? Зачем здороваться с роботом?')

vt = VkThings()

@client.command(aliases=['постироничная_картинка'])
async def postpic(ctx):
    await vt.vkPic(ctx, 'https://vk.com/album-162305728_00')

@client.command()
async def agrpic(ctx):
    await vt.vkPic(ctx, 'https://vk.com/album-184764992_00')

@client.command()
async def kindpic(ctx):
    await vt.vkPic(ctx, 'https://vk.com/album-147286578_00')

@client.command()
async def rompic(ctx):
    await vt.vkPic(ctx, 'https://vk.com/album-184394012_00')

@client.command()
async def progpic(ctx):
    await vt.vkPic(ctx, 'https://vk.com/album-187083413_00')

@client.command(aliases=['papapic'])
async def papichpic(ctx):
    await vt.vkPic(ctx, 'https://vk.com/album-181404250_00')

@client.command()
async def gachipic(ctx):
    await vt.vkPic(ctx, 'https://vk.com/album-73192688_00')

@client.command()
async def babkipic(ctx):
    await vt.vkPic(ctx, 'https://vk.com/album-199549875_00')

@client.command()
async def randompic(ctx):
    await vt.vkPic(ctx, 'https://vk.com/album-109290951_00')

@client.command()
async def girlpic(ctx):
    try:
        if ctx.channel.is_nsfw():
            await vt.vkPic(ctx, 'https://vk.com/album-43234662_00')
        else:
            await ctx.send(r'Канал должен быть **NSFW**  ¯\_(ツ)_/¯')
    except AttributeError:
        await ctx.send('Используйте эту команду только в **NSFW** канале')


@client.command()
async def hentaipic(ctx):
    try:
        if ctx.channel.is_nsfw():
            await vt.vkPic(ctx, 'https://vk.com/album-138698986_00')
        else:
            await ctx.send(r'Канал должен быть **NSFW**  ¯\_(ツ)_/¯')
    except AttributeError:
        await ctx.send('Используйте эту команду только в **NSFW** канале')

@client.command()
async def memepic(ctx):
    await vt.vkPic(ctx, 'https://vk.com/album-150550417_00')

@client.command()
async def jojopic(ctx):
    await vt.vkPic(ctx, 'https://vk.com/album-185642550_00')

@client.command()
async def picsource(ctx):
    embed = discord.Embed(title='Паблики вк с картинками', colour=discord.Colour.green())
    embed.add_field(name='Постироничные', value=config.links1)
    embed.add_field(name='Другие', value=config.links2)

    await ctx.send(embed=embed)

@client.command(aliases=['что', 'определение'])
async def what(ctx, *args):
    wiki_wiki = wikipediaapi.Wikipedia(language='ru', extract_format=wikipediaapi.ExtractFormat.HTML)

    page = ''
    for i in args:
        page += i + '_'

    page_py = wiki_wiki.page(page)
    if page_py.exists():
        soup = bs(page_py.summary, 'lxml')
        definition = soup.find('p').text
        await ctx.send(definition)
    else:
        await ctx.send(r'Такой страницы не существует ¯\_(ツ)_/¯')

@client.command(aliases=['погода'])
async def weather(ctx, city):
    owm = pyowm.OWM(config.PYOWM_TOKEN, language='ru')
    observation = owm.weather_at_place(city)
    w = observation.get_weather()
    temp = int(w.get_temperature('celsius')['temp'])

    if int(temp) > 0:
        temp = '+' + str(temp)
    status = w.get_detailed_status()
    windSpeed = w.get_wind()['speed']

    description = f'Температура: {temp}° \n \
    Статус: {status} \n \
    Скорость ветра: {windSpeed} м/с'

    embed = discord.Embed(title=city, colour=discord.Colour.green(), description=description)
    await ctx.send(embed=embed)

@client.command()
async def blacklist(ctx):
    channel = ctx.message.channel

    async for message in channel.history(limit=5):
        if message.author.discriminator == '2560' and message.author.bot and message.author.name == 'Постироничная шелупонь':
                
            file_name = message.attachments[0].filename
            group = file_name.split('_')[0]
            pic_num = int(file_name.split('_')[1].replace('.jpg', ''))

            animals = [':gorilla:', ':dog:', ':pig:', ':cow:', ':koala:', ':frog:', ':boar:', ':monkey_face:', ':panda_face:', ':clown:']

            if (ctx.message.author.discriminator == '3191' and ctx.message.author.name == 'StatingWaif') or \
            (ctx.message.author.discriminator == '2726' and ctx.message.author.name == 'Rendei<3'):
                Base = DataBase()

                await Base.getInDataBase(group, pic_num)
                                

                                
                await ctx.send(f'Ваше пожелание будет исполнено {choice(animals)}')
                print('blacklisted')
                break
            else:
                bufferfile = discord.File(BytesIO(await message.attachments[0].read()), filename=file_name)
                channel = client.get_channel(config.CHANNEL_ID)
                await channel.send(file=bufferfile)
                await ctx.send(f'Спасибо за содействие {choice(animals)}')
                try:
                    print(f'[{ctx.message.guild.name}] blacklist')
                except:
                    print(f'[user {ctx.message.author.name}] blacklist')
                break

@client.command()
async def help(ctx):
    embed = discord.Embed(title='Список команд для использования бота', colour=discord.Colour.green())

    embed.add_field(name='Команды для постироничных картинок', value=config.postValue)
    embed.add_field(name='Команды для других картинок', value=config.otherValue)
    embed.add_field(name='Команды для музыки', value=config.musicValue)
    embed.add_field(name='Остальные команды', value=config.notPicValue)
        
    await ctx.send(embed=embed)
        
client.add_cog(music.Music(client))
client.run(config.BOT_TOKEN)