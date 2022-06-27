from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from bot import Bot

import os
import traceback


async def load_extensions(
    bot: "Bot", extensions: dict, ignore_exceptions: bool = False
) -> dict:
    result = {}
    for extension, commands in extensions.items():
        bot.log.info(f"Cog {extension}:")
        if type(commands) != list:
            commands = [
                f.replace(".py", "")
                for f in os.listdir(f"./cogs/{extension}")
                if os.path.isfile(os.path.join(f"./cogs/{extension}", f))
            ]
        for command in commands:
            try:
                result[f"{extension}.{command}"] = {"status": "OK", "error": None}
                await bot.load_extension(f"cogs.{extension}.{command}")
            except Exception as e:
                bot.log.error(f"Failed to load extension {extension}.{command}")
                bot.log.error(f"{traceback.print_exc()}")
                result[f"{extension}.{command}"]["status"] = "ERROR"
                result[f"{extension}.{command}"]["error"] = e
                if ignore_exceptions == False:
                    raise Exception(e)
            else:
                bot.log.info(f"    {command} loaded")
    return result


async def unload_extensions(
    bot: "Bot", extensions: dict, ignore_exceptions: bool = False
) -> dict:
    result = {}
    for extension, commands in extensions.items():
        bot.log.info(f"Cog {extension}:")
        if type(commands) != list:
            commands = []
            for extension_ in bot.extensions:
                extension_ = extension_.split(".")
                dir = extension_[1]
                name = extension_[2]
                if dir == extension:
                    commands.append(name)
        for command in commands:
            try:
                result[f"{extension}.{command}"] = {"status": "OK", "error": None}
                await bot.unload_extension(f"cogs.{extension}.{command}")
            except Exception as e:
                bot.log.error(f"Failed to load extension {extension}.{command}")
                bot.log.error(f"{traceback.print_exc()}")
                result[f"{extension}.{command}"]["status"] = "ERROR"
                result[f"{extension}.{command}"]["error"] = e
                if ignore_exceptions == False:
                    raise Exception(e)
            else:
                bot.log.info(f"    {command} unloaded")
    return result
