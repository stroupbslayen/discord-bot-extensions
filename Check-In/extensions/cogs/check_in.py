import datetime
from datetime import datetime

import discord
from discord.ext import commands

from ...database.models.user import User


def calc_time(seconds: float) -> str:
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    hours = f"{hours} hour(s)" if hours else ""
    minutes = f"{minutes} minute(s)" if minutes else ""
    seconds = f"{round(seconds,2)} second(s)" if seconds else ""
    return f"{hours} {minutes} {seconds}".strip()


class CheckIn(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    @commands.guild_only()
    async def checkin(self, ctx: commands.Context):
        """: Check yourself in"""
        member: discord.Member = ctx.author
        user = User.get(member)
        if not user.checked_in:
            # user.touch()
            user.checked_in = True
            user.save()
            await ctx.send(f"{member.mention}, you've been checked in!")
        else:
            seconds = (datetime.utcnow() - user.updated_at).total_seconds()
            await ctx.send(
                f"{member.mention}, you checked in *{calc_time(seconds)}* ago"
            )

    @commands.command()
    @commands.guild_only()
    async def checkout(self, ctx: commands.Context):
        """:Check yourself out"""

        member: discord.Member = ctx.author
        user = User.get(member)
        if user.checked_in:
            seconds = (datetime.utcnow() - user.updated_at).total_seconds()
            user.total_time += seconds
            user.checked_in = False
            user.save()
            await ctx.send(
                f"{member.mention}, you were checked in for *{calc_time(seconds)}*"
            )
        else:
            await ctx.send(f"{member.mention}, you're not currently checked in!")

    @commands.command()
    @commands.guild_only()
    async def maintime(self, ctx: commands.Context):
        """: See your total check-in time"""
        member: discord.Member = ctx.author
        user = User.get(member)
        await ctx.send(
            f"{member.mention}, your total checkin time is *{calc_time(user.total_time)}*"
        )

    @commands.has_any_role(
        "Admin", "Moderator"
    )  # change to any roles that can use the leaderboard command
    @commands.command()
    @commands.guild_only()
    async def leaderboard(self, ctx: commands.Context):
        """: See a leaderboard showing the top 10 in your server"""
        users = (
            User.all()
            .reject(lambda user: not ctx.guild.get_member(user.id))
            .sort(lambda user: user.total_time * -1)
            .chunk(10)
        )
        if users:
            members = "\n".join(
                f"{ctx.guild.get_member(user.id).__str__().ljust(30)}{calc_time(user.total_time).rjust(10)}"
                for user in users[0]
            )
            embed = discord.Embed(
                title="TOP 10",
                description=f'{"```Member".ljust(30)}\n{members}```',
            )
            await ctx.send(embed=embed)
        else:
            await ctx.send("If members have checked-in, they have not checked-out yet.")


def setup(bot):
    bot.add_cog(Timeclock(bot))
