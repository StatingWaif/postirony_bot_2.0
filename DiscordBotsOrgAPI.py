import dbl
from discord.ext import commands, tasks
import config
import asyncio

class DiscordBotsOrgAPI(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.token = config.DBL_TOKEN
        self.dblpy = dbl.DBLClient(self.bot, self.token)
        self.update_stats.start()

    def cog_unload(self):
        self.update_stats.cancel()

    @tasks.loop(minutes=30)
    async def update_stats(self):
        await self.bot.wait_until_ready()
        try:
            server_count = len(self.bot.guilds)
            await self.dblpy.post_guild_count(server_count)
            print('Posted server count ({})'.format(server_count))
        except Exception as e:
            print('Failed to post server count\n{}: {}'.format(type(e).__name__, e))

        print(config.border)

def dbl_setup(bot):
    bot.add_cog(DiscordBotsOrgAPI(bot))

