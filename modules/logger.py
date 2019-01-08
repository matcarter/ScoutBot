from discord.ext import commands
from discord.ext.commands import CommandNotFound
import json
import time

"""
    Things to log
     * Report a bug - !bug [module] (report of bug)
     * Request a feature - !feature [module] (feature specifications)
     * Submit feedback - !feedback (feedback submission)
"""


class Logger:
    def __init__(self, bot):
        self.bot = bot


def setup(bot):
    bot.add_cog(Logger(bot))
