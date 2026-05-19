import discord
from discord.ext import commands
import config

class AntiSpamTrap(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.trap_channel_id = config.SPAM_TRAP_CHANNEL_ID

        print("🔁 AntiSpamTrap system loaded")

async def setup(bot):

    cog = AntiSpamTrap(bot)
    await bot.add_cog(cog)

    print("🛡️ Sending anti-spam message...")

    channel = bot.get_channel(config.SPAM_TRAP_CHANNEL_ID)

    if channel is None:
        print("❌ Channel not found")
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

    print("✅ Message sent")