
import discord
from discord.ext import commands

# add roles that can use some commands
APPROVED_ROLES = ['Admin', 'Mod', 8675309]


def is_approved():
    def predicate(ctx):
        author = ctx.message.author
        if author is ctx.message.guild.owner:
            return True
        if any(role.name in APPROVED_ROLES for role in author.roles):
            return True
    return commands.check(predicate)

class Queue(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot= bot
        self.queue = []
        self.qtoggle = False


    @commands.command()
    async def add(self, ctx):
        ''': Add yourself to the queue!'''
        author = ctx.message.author
        if self.qtoggle:
            if author not in self.queue:
                self.queue.append(author)
                await ctx.send(f'{ctx.author.mention}, you have been added to the queue.')
            else:
                await ctx.send(f'{ctx.author.mention}, you are already in the queue!')
        else:
            await ctx.send('The queue is closed.')

    @commands.command()
    async def remove(self, ctx):
        ''': Remove yourself from the queue'''
        author = ctx.message.author
        if author in self.queue:
            self.queue.remove(author)
            await ctx.send(f'{ctx.author.mention}, you have been removed from the queue.')
        else:
            await ctx.send(f'{ctx.author.mention}, you were not in the queue.')

    @commands.command(name='queue')
    async def _queue(self, ctx):
        ''': See who's up next!'''
        guild = ctx.guild
        message = ''
        for place, member in enumerate(self.queue):
            message += f'**#{place+1}** : {member.mention}\n'
        if message != '':
            await ctx.send(message)
        else:
            await ctx.send('Queue is empty')

    @commands.command()
    async def position(self, ctx):
        ''': Check your position in the queue'''
        author = ctx.message.author
        if author in self.queue:
            _position = self.queue.index(author)+1
            await ctx.send(f'{ctx.author.mention}, you are **#{_position}** in the queue.')
        else:
            await ctx.send(f'{ctx.author.mention}, you are not in the queue, please use the `add` command to add yourself to the queue.')

    @commands.has_any_role(*APPROVED_ROLES)
    @commands.command(name='next')
    async def _next(self, ctx):
        ''': Call the next member in the queue'''
        if len(self.queue) > 0:
            member = self.queue[0]
            await ctx.send(f'You are up **{member.mention}**! Have fun!')
            self.queue.remove(self.queue[0])

    @commands.has_any_role(*APPROVED_ROLES)
    @commands.command()
    async def clear(self, ctx):
        ''': Clears the queue'''
        self.queue = []
        await ctx.send('Queue has been cleared')

    @commands.has_any_role(*APPROVED_ROLES)
    @commands.command()
    async def toggleq(self, ctx):
        ''': Toggles the queue open or closed'''
        self.qtoggle = not self.qtoggle
        if self.qtoggle:
            state = 'OPEN'
        else:
            state = 'CLOSED'
        await ctx.send(f'Queue is now **{state}**')

def setup(bot):
    bot.add_cog(Queue(bot))


