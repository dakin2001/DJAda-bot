import discord
from discord.ext import commands
import config

class AntiSpamTrap(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.trap_channel_id = config.SPAM_TRAP_CHANNEL_ID

        print("🔁 AntiSpamTrap system loaded and automatically activated")

    @commands.Cog.listener()
    async def on_ready(self):

        print("🛡️ AntiSpamTrap on_ready triggered")

        for guild in self.bot.guilds:

            print(f"📌 Checking guild: {guild.name}")

            channel = guild.get_channel(self.trap_channel_id)

            if channel is None:
                print("❌ Spam trap channel not found")
                continue

            print(f"✅ Found channel: {channel.name}")

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

            print("✅ Anti-spam warning message sent")

async def setup(bot):
    await bot.add_cog(AntiSpamTrap(bot))