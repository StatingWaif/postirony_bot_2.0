import dbl
from discord.ext import commands
import config

class DiscordBotsOrgAPI(commands.Cog):
        def __init__(self, bot):
                self.bot = bot
                self.token = config.DBL_TOKEN
                self.dblpy = dbl.DBLClient(self.bot, self.token)
                self.updating = self.bot.loop.create_task(self.update_stats())

        async def update_stats(self):
                while not self.bot.is_closed():
                        print(config.border)
                        print('Attempting to post server count')
                        try:
                                await self.dblpy.post_guild_count()
                                print('Posted server count ({})'.format(self.dblpy.guild_count()))
                        except Exception as e:
                                print('Failed to post server count\n{}: {}'.format(type(e).__name__, e))
                        await asyncio.sleep(1800)

                        print(config.border)

def dbl_setup(bot):
        bot.add_cog(DiscordBotsOrgAPI(bot))

