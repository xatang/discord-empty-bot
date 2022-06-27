import logging
import traceback
from datetime import datetime

import discord
from apscheduler import events
from apscheduler.schedulers import SchedulerAlreadyRunningError
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord.ext import commands

from config import bot_token, owner_id
from database.schema import async_session
from utils.extensions import load_extensions

initial_extensions = {"test": ["test1", "test2", "test3"]}


class Bot(commands.Bot):
    def __init__(self, **kwargs):
        super().__init__(
            command_prefix=self.command_prefix,
            intents=self.intents(),
            case_insensitive=True,
            owner_id=owner_id,
        )
        handler = logging.StreamHandler()
        dt_fmt = "%Y-%m-%d %H:%M:%S"
        formatter = logging.Formatter(
            "{levelname:<5} {name}: {message}", dt_fmt, style="{"
        )
        handler.setFormatter(formatter)
        logger = logging.getLogger("discord")
        logger.addHandler(handler)
        logging.getLogger("discord").setLevel(logging.INFO)
        logging.getLogger("discord.http").setLevel(logging.WARNING)
        logging.getLogger("discord.gateway").setLevel(logging.WARNING)

        scheduler = AsyncIOScheduler(timezone="UTC")
        logging.getLogger("apscheduler").setLevel(logging.ERROR)

        self.log = logger
        self.scheduler = scheduler
        self.db = async_session
        ###
        self.start_time = None

    @staticmethod
    def command_prefix(self, message: discord.Message):
        prefixes = ["/"]
        return commands.when_mentioned_or(*prefixes)(self, message)

    async def setup_hook(self):
        await load_extensions(self, initial_extensions, True)

    @staticmethod
    def intents():
        intents = discord.Intents.default()
        intents.bans = True
        intents.members = True
        intents.voice_states = True
        intents.message_content = True
        return intents

    async def on_ready(self):
        self.remove_command("help")
        self.log.info(
            f"Logged in as: {self.user.name} - {self.user.id}\nVersion: {discord.__version__}\n"
        )
        await self.change_presence(status=discord.Status.dnd)
        self.log.info("Successfully loaded, the initialization of the modules...")

        self.scheduler.add_listener(self.listen_to_exceptions, events.EVENT_JOB_ERROR)
        try:
            self.scheduler.start()
        except SchedulerAlreadyRunningError:
            pass
        self.scheduler.print_jobs()
        self.start_time = datetime.utcnow()

    def listen_to_exceptions(self, event):
        self.loop.create_task(self.listen_to_exceptions_async(event))

    async def listen_to_exceptions_async(self, event):
        error_str = traceback.format_exception(
            type(event.exception), event.exception, event.exception.__traceback__
        )
        error_str = "".join(error_str)
        self.log.error(error_str)

    async def on_error(self, event, *args, **kwargs):
        error = traceback.format_exc()
        error_msg = (
            f"\nevent:\n{event}\nargs:\n{args}\nkwargs:\n{kwargs}\nerror:\n{error}"
        )
        self.log.error(error_msg)


bot = Bot()
bot.run(bot_token, reconnect=True, log_handler=None)
