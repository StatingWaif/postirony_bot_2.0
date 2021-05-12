#import dbl
#from discord.ext import commands, tasks
#import config
#import asyncio

#class DiscordBotsOrgAPI(commands.Cog):
#    def __init__(self, bot):
#        self.bot = bot
#        self.token = config.DBL_TOKEN
#        self.dblpy = dbl.DBLClient(self.bot, self.token)
#        self.update_stats.start()

#    def cog_unload(self):
#        self.update_stats.cancel()

#    @tasks.loop(minutes=30)
#    async def update_stats(self):
#        await self.bot.wait_until_ready()
#        try:
#            print(config.border)
#            server_count = len(self.bot.guilds)
#            await self.dblpy.post_guild_count(server_count)
#            print('Posted server count ({})'.format(server_count))
#        except Exception as e:
#            print('Failed to post server count\n{}: {}'.format(type(e).__name__, e))

#        print(config.border)

#def dbl_setup(bot):
#    bot.add_cog(DiscordBotsOrgAPI(bot))

from discord.ext import tasks

import dbl
import config
from bot import client

# This example uses tasks provided by discord.ext to create a task that posts guild count to top.gg every 30 minutes.

dbl_token = config.DBL_TOKEN  # set this to your bot's top.gg token
bot.dblpy = dbl.DBLClient(client, dbl_token)

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