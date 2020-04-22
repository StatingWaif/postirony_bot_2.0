import vk
from DataBase import DataBase
import config
from random import randint
import discord
import aiohttp
from io import BytesIO
import mysql.connector

class VkThings:
    async def vkPic(self, ctx, url):
        async with ctx.typing():
            session = vk.Session(access_token=config.VK_TOKEN)
            vk_api = vk.API(session, v='5.0')

            owner_id = url.split('/')[-1].replace('album', '').replace('_00', '')

            photos = vk_api.photos.get(owner_id=owner_id, album_id='wall', rev=0, count=1000, photo_sizes=1)
            num_of_photos = photos['count']

            pic = randint(0, num_of_photos - 1)

            Base = DataBase()
            mycursor = Base.mydb.cursor()
            group = owner_id.replace('-', '')

            try:
                mycursor.execute(f'SELECT * FROM group_{group}')
            except mysql.connector.errors.ProgrammingError:
                mycursor.execute(f'CREATE TABLE group_{group} (pic INTEGER(10))')

            while await Base.isInBase(group, pic):
                pic = randint(0, num_of_photos - 1)

            offset = pic - (pic % 1000)
            photos = vk_api.photos.get(owner_id=owner_id, album_id='wall', rev=0, count=1000, photo_sizes=1, offset=offset)
            photo = photos['items'][pic - offset]['sizes'][-1]['src']

            async with aiohttp.ClientSession() as session:
                async with session.get(photo) as resp:
                    if resp.status == 200:
                        buffer = BytesIO(await resp.read())
                        group = owner_id.replace('-', '')
                        bufferfile = discord.File(buffer, filename=f'{group}_{pic}.jpg')
                        await ctx.send(file=bufferfile)	
                        print(pic)

    async def sendVk(self, message):
        session = vk.Session(access_token=config.SEND_TOKEN)
        vk_api = vk.API(session, v='5.45')
        vk_api.messages.send(domain=config.NAME_SEND, message=message, random_id=randint(0, 1000000000))