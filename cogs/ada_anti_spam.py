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

    @commands.Cog.listener()
    async def on_message(self, message):

        # Ignore bots
        if message.author.bot:
            return

        # System disabled
        if not self.enabled:
            return

        # Wrong channel
        if message.channel.id != self.trap_channel_id:
            return

        guild = message.guild
        member = guild.get_member(message.author.id)

        if member is None:
            print("❌ Member not found")
            return

        # Ignore staff
        if any(role.id == self.staff_role_id for role in member.roles):
            return

        print(f"⚠️ Trap triggered by {member}")

        try:
            await message.delete()
        except:
            pass

        # ===================================
        # DM USER
        # ===================================
        try:

            dm = await member.create_dm()

            await dm.send("<:Emoji_Think_Patrick:1430608408188420116>")
            await asyncio.sleep(1)

            message_part1 = (
                f"Hello {member.mention}.\n\n"
                "You triggered the **Bleeding Legend Anti-Spam System**.\n"
                "A temporary moderation action has been applied to your account.\n"
            )

            await dm.send(message_part1)
            await asyncio.sleep(2)

            message_part2 = (
                "If this was a mistake, you can rejoin the server in a few minutes.\n"
                "Repeated suspicious activity may result in a permanent ban."
            )

            await dm.send(message_part2)
      
        except discord.Forbidden:
            print(f"Impossible d'envoyer un DM à {member} (DM fermé)")

        # ===================================
        # 1️⃣ TIMEOUT IMMÉDIAT
        # ===================================
        try:
            await member.timeout(
                datetime.timedelta(minutes=5),
                reason="Spam trap triggered"
            )

            print(f"🔇 {member} timeout 5 min")

        except Exception as e:
            print(f"Timeout error: {e}")

        # ===================================
        # 2️⃣ TEMPBAN
        # ===================================
        try:

            await guild.ban(
                member,
                reason="Spam trap auto tempban",
                delete_message_days=0
            )

            print(f"🔨 {member} tempbanned")

            await message.channel.send(f"<:Emoji_Wow_Patrick:1430608431768932393> {member.mention} triggered the anti-spam trap.\n Temporary ban applied for 5 minutes.")

            # Wait 5 min
            await asyncio.sleep(300)

            # Unban
            await guild.unban(
                discord.Object(id=member.id),
                reason="Tempban expired"
            )

            print(f"✅ {member} unbanned")

        except Exception as e:
            print(f"Ban error: {e}")

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

async def setup(bot):
    await bot.add_cog(AntiSpamTrap(bot))