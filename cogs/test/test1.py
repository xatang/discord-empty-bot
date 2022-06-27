from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from bot import Bot

import discord
from discord.ext import commands


class TestCogTest1(commands.Cog):
    def __init__(self, bot: "Bot"):
        self.bot = bot

    def cog_unload(self):
        pass

    #############################
    # Commands

    @commands.is_owner()
    @commands.bot_has_permissions(send_messages=True)
    @commands.command(
        name="test1",
        description="Тестовая команда",
        usage="**аргумент** и **аргумент**",
    )
    async def test(self, ctx, arg1):
        """Если нет сработает, то надо чинить"""

        pass

    #############################
    # Tasks

    #############################
    # Events

    #############################
    # Other functions


async def setup(bot: "Bot"):
    await bot.add_cog(TestCogTest1(bot))
