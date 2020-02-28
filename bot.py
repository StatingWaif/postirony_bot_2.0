import discord
from discord.ext import commands
from DiscordBotsOrgAPI import DiscordBotsOrgAPI, dbl_setup
from DiscordBotsOrgAPI import dbl_setup
import config
from VkThings import VkThings
from random import randint, choice
import wikipediaapi
from bs4 import BeautifulSoup as bs
import pyowm
from DataBase import DataBase

client = commands.Bot(command_prefix = '!')
client.remove_command('help')

dbl_setup(client)

@client.event
async def on_ready():
        print('bot is ready')
        bot_activity = discord.Activity(name='своих родителей !help для списка команд', type=discord.ActivityType.listening)
        await client.change_presence(activity=bot_activity)
        guilds = client.guilds
        servers = []

        for guild in guilds:
                servers.append(guild.name)

        message = f'Кол-во серверов: {len(guilds)}. \n' + ', '.join(servers) + '.'
        vk = VkThings()
        await vk.sendVk(message)
        print(config.border)

@client.event
async def on_member_join(member):
        print(f'{member} зашел на сервер {member.guild.name}')

@client.event
async def on_member_remove(member):
        print(f'{member} вышел с сервера {member.guild.name}')

@client.event
async def on_guild_join(guild):
        print(config.border)
        print(f'Теперь ещё и {guild.name}')
        print(config.border)

@client.command()
async def hello(ctx):
        async with ctx.typing():
                await ctx.send(f'{ctx.message.author.mention} ты што идиот??? Ты совсем жизнью контуженный? Зачем здороваться с роботом?')

vt = VkThings()

@client.command(aliases=['постироничная_картинка'])
async def postpic(ctx):
        await vt.vkPic(ctx, 'https://vk.com/album-162305728_00')

@client.command()
async def schoolpic(ctx):
        await vt.vkPic(ctx, 'https://vk.com/album-185340181_00')

@client.command()
async def agrpic(ctx):
        await vt.vkPic(ctx, 'https://vk.com/album-184764992_00')

@client.command()
async def kindpic(ctx):
        await vt.vkPic(ctx, 'https://vk.com/album-184003532_00')

@client.command()
async def villpic(ctx):
        await vt.vkPic(ctx, 'https://vk.com/album-186137194_00')

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
async def girlpic(ctx):
        try:
                if ctx.channel.is_nsfw():
                        await vt.vkPic(ctx, 'https://vk.com/album-43234662_00')
                else:
                        await ctx.send(r'Канал должен быть **NSFW**  ¯\_(ツ)_/¯')
        except AttributeError:
                await ctx.send('Используйте эту команду только в **NSFW** канале')

@client.command()
async def memepic(ctx):
        await vt.vkPic(ctx, 'https://vk.com/album-150550417_00')

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
        if (ctx.message.author.discriminator == '3191' and ctx.message.author.name == 'StatingWaif') or (ctx.message.author.discriminator == '2726' and ctx.message.author.name == 'Rendei<3'):
                channel = ctx.message.channel

                async for message in channel.history(limit=5):
                        if message.author.discriminator == '2560' and message.author.bot and message.author.name == 'Постироничная шелупонь':
                                file_name = message.attachments[0].filename
                                group = file_name.split('_')[0]
                                pic_num = int(file_name.split('_')[1].replace('.jpg', ''))

                                Base = DataBase()

                                await Base.getInDataBase(group, pic_num)
                                break
                animals = [':gorilla:', ':dog:', ':pig:', ':cow:', ':koala:', ':frog:', ':boar:', ':monkey_face:', ':panda_face:']
                await ctx.send(f'Ваше пожелание будет исполнено{choice(animals)}')
                print('blacklisted')

@client.command()
async def help(ctx):
        embed = discord.Embed(title='Список команд для использования бота', colour=discord.Colour.green())

        embed.add_field(name='Команды для постироничных картинок:', value=config.postValue)
        embed.add_field(name='Команды для других картинок:', value=config.otherValue)
        embed.add_field(name='Остальные команды:', value=config.notPicValue)
        await ctx.send(embed=embed)

client.run(config.BOT_TOKEN)