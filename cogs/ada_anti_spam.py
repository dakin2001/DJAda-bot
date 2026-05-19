from email.mime import message

import discord
from discord.ext import commands
import asyncio
import datetime
import config
from res.emojis import Emojis

class AntiSpamTrap(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.enabled = True
        print("🔁 AntiSpamTrap system loaded and automatically activated")

        self.trap_channel_id = config.SPAM_TRAP_CHANNEL_ID
        self.staff_role_id = config.STAFF_ROLE_ID


    async def setup(bot):

        cog = AntiSpamTrap(bot)
        await bot.add_cog(cog)

        print("🛡️ AntiSpamTrap loaded, checking startup message...")

        channel = bot.get_channel(config.SPAM_TRAP_CHANNEL_ID)

        if channel is None:
            print("❌ Channel not found")
            return

        # Vérifie les derniers messages
        async for msg in channel.history(limit=10):

            if (
                msg.author == bot.user
                and msg.embeds
                and msg.embeds[0].title == "It's a Trap!"
            ):
                print("ℹ️ Message already exists, skipping...")
                return

        embed = discord.Embed(
            title="It's a Trap!",
            description=(
                "This channel is a spam-bot trap. It's here to protect the server from scam/spam bots.\n\n"
                "So please... Do NOT type here. <:Emoji_Cry_Headmaster:1441146922948624616> \n\n"
                "If you accidentally trigger the system, you should be automatically unbanned after 5 minutes <:Emoji_Wait_Val:1430608423963332710>."
            ),
            color=0xef87ff
        )

        await channel.send(embed=embed)

        print("✅ Anti-spam message sent")


async def setup(bot):
    await bot.add_cog(AntiSpamTrap(bot))