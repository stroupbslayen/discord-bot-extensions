import discord
from discord.ext import commands
from bot.database.models.CurrencyModels import Accounts, Banks

import inflection


def grammar(bank: Banks, amount: int):
    curr = bank.currency
    if amount in (-1, 1):
        return inflection.singularize(curr)
    else:
        return inflection.pluralize(curr)


def is_owner_or_approved():
    def predicate(ctx: commands.Context):
        guild = ctx.guild
        if ctx.author is guild.owner:
            return True
        bank = Banks.find(guild.id)
        if any(role.id in bank.approved for role in ctx.author.roles):
            return True

    return commands.check(predicate)


class Currency(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    def check_guild(self, guild: discord.Guild = None):
        guilds = Banks.lists("id")
        if guild and guild.id not in guilds:
            Banks(id=guild.id).save()
        else:
            added = list(
                {"id": guild.id} for guild in self.bot.guilds if guild.id not in guilds
            )
            Banks.insert(added)

    @commands.Cog.listener()
    async def on_ready(self):
        self.check_guild()

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        self.check_guild(guild)

    @commands.guild_only()
    @is_owner_or_approved()
    @commands.command(aliases=["add", "give"])
    async def deposit(
        self, ctx: commands.Context, amount: int = 0, member: discord.Member=None
    ):
        """
        : Deposit currency into a members account
        usage:
            deposit <amount> <@member>
        """
        member = member or ctx.author
        bank = Banks.find(ctx.guild.id)
        account = bank.get_account(member)
        account.balance += amount
        account.save()
        await ctx.send(
            f"{amount} {grammar(bank, amount)} has been given to {member.mention}"
        )

    @commands.guild_only()
    @is_owner_or_approved()
    @commands.command(aliases=["remove", "take"])
    async def withdraw(
        self, ctx: commands.Context, amount: int = 0, member: discord.Member=None
    ):
        """
        : Withdraw currency from a members account
        usage:
            withdraw <amount> <@member>
        """
        member = member or ctx.author
        bank = Banks.find(ctx.guild.id)
        account = bank.get_account(member)
        account.balance -= amount
        account.save()
        await ctx.send(
            f"{amount} {grammar(bank, amount)} has been taken from {member.mention}"
        )

    @commands.guild_only()
    @commands.command(aliases=["bank", "stash"])
    async def balance(self, ctx: commands.Context, member: discord.Member = None):
        """
        : Check the balance of your account or another member
        """
        member = member or ctx.author
        bank = Banks.with_("accounts").find(ctx.guild.id)
        account = bank.get_account(member)
        balance = account.balance
        await ctx.send(f"{member.mention}, you have {balance} {grammar(bank, balance)}")

    @commands.guild_only()
    @commands.is_owner()
    @commands.command(aliases=["addrole"])
    async def addApproved(self, ctx, roles: commands.Greedy[discord.Role]):
        """
        : Add roles that can deposit or withdraw currency from members
        usage:
            addApproved <@role>
        note:
            multiple roles can be added in one command
        """
        Banks.find(ctx.guild.id).add_roles(*roles)
        await ctx.send("Approved roles have been added!")

    @commands.guild_only()
    @commands.is_owner()
    @commands.command(aliases=["delrole"])
    async def delApproved(self, ctx, roles: commands.Greedy[discord.Role]):
        """
        : Remove roles that can deposit or withdraw currency from members
        usage:
            delApproved <@role>
        note:
            multiple roles can be added in one command
        """
        Banks.find(ctx.guild.id).remove_roles(*roles)
        await ctx.send("Approved roles have been removed!")

    @commands.guild_only()
    @is_owner_or_approved()
    @commands.command()
    async def approved(self, ctx):
        """
        : Get a list of approved roles that can deposit or withdraw from members
        usage:
            approved
        """
        guild = ctx.guild
        bank = Banks.find(guild.id)
        description = "\n".join(
            guild.get_role(role).mention
            for role in bank.approved
            if guild.get_role(role)
        )
        embed = discord.Embed(
            title="Approved Roles", description=description, color=discord.Color.green()
        )
        await ctx.send(embed=embed)

    @commands.guild_only()
    @is_owner_or_approved()
    @commands.command(aliases=["currencyname"])
    async def changeCurrency(self, ctx, name: str = "dollar"):
        """
        : Change the currency name that the server is using
        usage:
            changeCurrency <currency_name>
        note:
            default currency is 'dollars'
        """
        bank = Banks.find(ctx.guild.id)
        bank.currency = name
        bank.save()
        await ctx.send(
            f"The currency has been changed to **{inflection.pluralize(name)}**"
        )

    @commands.guild_only()
    @commands.command()
    async def leaderboard(self, ctx: commands.Context):
        '''
        : Get a leaderboard showing the top 10 members with the largest account.
        '''
        bank = Banks.with_("accounts").find(ctx.guild.id)
        accounts = (
            bank.accounts.reject(lambda account: not ctx.guild.get_member(account.id))
            .sort(lambda account: account.balance * -1)
            .chunk(10)
        )
        if accounts:
            members = "\n".join(
                f"{ctx.guild.get_member(account.id).__str__().ljust(30)}{str(account.balance).rjust(10)}"
                for account in accounts[0]
            )
            embed = discord.Embed(
                title="TOP 10",
                description=f'{"```Member".ljust(30)}{bank.currency.rjust(10)}\n{members}```',
            )
            await ctx.send(embed=embed)
        else:
            await ctx.send("I got nuth'n")


def setup(bot):
    bot.add_cog(Currency(bot))

