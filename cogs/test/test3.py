from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from bot import Bot

import discord
from discord.ext import commands


class TestCogTest3(commands.Cog):
    def __init__(self, bot: "Bot"):
        self.bot = bot

    def cog_unload(self):
        pass

    #############################
    # Commands

    #############################
    # Tasks

    #############################
    # Events

    #############################
    # Other functions


async def setup(bot: "Bot"):
    await bot.add_cog(TestCogTest3(bot))
