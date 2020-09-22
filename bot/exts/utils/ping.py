import socket
from datetime import datetime

import aioping
from discord import Embed
from discord.ext import commands

from bot.bot import Bot
from bot.constants import Emojis, URLs

DESCRIPTIONS = (
    "Time to receive command information",
    "Python Discord website latency",
    "Discord API latency"
)
ROUND_LATENCY = 3


class Latency(commands.Cog):
    """Getting the latency between the bot and websites."""

    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @commands.command()
    async def ping(self, ctx: commands.Context) -> None:
        """
        Gets different measures of latency within the bot.

        Returns bot, Python Discord Site, Discord Protocol latency.
        """
        # datetime.datetime objects do not have the "milliseconds" attribute.
        # It must be converted to microseconds before converting to milliseconds.
        bot_ping = (datetime.utcnow() - ctx.message.created_at).total_seconds() / 1000
        bot_ping = f"{round(bot_ping, ROUND_LATENCY)} ms"

        try:
            delay = await aioping.ping(URLs.site, family=socket.AddressFamily.AF_INET) * 1000
            site_ping = f"{round(delay, ROUND_LATENCY)} ms"

        except TimeoutError:
            site_ping = f"{Emojis.cross_mark} Connection timed out."

        # Discord Protocol latency return value is in seconds, must be multiplied by 1000 to get milliseconds.
        discord_ping = f"{round(self.bot.latency * 1000, ROUND_LATENCY)} ms"

        embed = Embed(title="Pong!")

        for desc, latency in zip(DESCRIPTIONS, [bot_ping, site_ping, discord_ping]):
            embed.add_field(name=desc, value=latency, inline=False)

        await ctx.send(embed=embed)


def setup(bot: Bot) -> None:
    """Load the Latency cog."""
    bot.add_cog(Latency(bot))
