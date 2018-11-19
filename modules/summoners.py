import discord
from discord.ext import commands
from .player import Player


class Summoners:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='info')
    async def get_summoner(self, ctx, summoner: str):
        """Returns information on a summoner"""

        player = Player(summoner)
        await ctx.send(player.to_string())


def setup(bot):
    bot.add_cog(Summoners(bot))
