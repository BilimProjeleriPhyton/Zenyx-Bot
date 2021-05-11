from discord.errors import Forbidden
from utils.error_handler import MissingArgument, MissingPermissionOnMember, RoleNotFound, embed_success
import discord, praw
from discord.ext import commands
from datetime import datetime
from main import CLUSTER
from utils.constants import  COLOUR_ROLES_DICT, get_channel_id, get_command_description

r = praw.Reddit(client_id="7oE7yB5GJJua2Q", client_secret="ooidPB-ETJxbRflpja6a65KX03g", user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36', username="PhantomVipermon", check_for_async=False)
last_check = datetime.utcnow

class Misc(commands.Cog):
    """
    Miscellaneous related commands.
    """
    def __init__(self, client):
        self.client = client
    
    @commands.command(aliases=["st", "shower", "showerthought"])
    async def _get_shower_thought(self, ctx):
        """Sends random shower thought from r/showerthoughts"""

        sub = r.subreddit('showerthoughts')
        sub = sub.random()
        text = sub.selftext

        if text  == "":
            text = sub.title
            if text == "":
                await ctx.send("Could not find text")
                return
        

        embed=discord.Embed(title="", description=f"{text}\n\n{sub.url}", inline=False
        ).set_author(name=f"Showerthought by {sub.author}")

        await ctx.send(embed=embed)

    @commands.command()
    async def invites(self, ctx, member : discord.Member = None):
        """Sends amount of invites [member] has"""

        if member is None:
            member = ctx.author

        total_invites = len([invite for invite in await ctx.guild.invites() if invite.inviter == ctx.author])
        await ctx.send(f"{member} has invited {total_invites} member{'' if total_invites == 1 else 's'} to the server!")


    @commands.command(aliases=['m'])
    async def mirror(self, ctx):        
        """?mirror [message]"""
        message = ctx.message.content
        message = message.partition(' ')[2]
        
        if message == "":
            raise MissingArgument("Message", get_command_description("mirror"))    

        await ctx.message.delete()
        if message[0] == str(self.client.command_prefix):
            return

        channel = self.client.get_channel(get_channel_id(ctx.message.guild.id, "channel_general"))
        await channel.send(message)
            


    @commands.command()
    async def serverinfo(self, ctx):
        """Sends information about the server"""

        embed = discord.Embed(
            title=str(ctx.guild.name) + " Server Information",
            description=str(ctx.guild.description),
            color=discord.Color.blue()
            
            ).set_thumbnail(url=str(ctx.guild.icon_url)
            ).add_field(name="Owner", value=str(ctx.guild.owner), inline=True
            ).add_field(name="Server ID", value=str(ctx.guild.id), inline=True
            ).add_field(name="Region", value=str(ctx.guild.region), inline=True
            ).add_field(name="Member Count", value=str(ctx.guild.member_count), inline=True
        )

        await ctx.reply(embed=embed)
 
    '''
    @commands.command()
    async def confess(self, ctx, *, confession = None):
        """?confess [confession]"""
        if isinstance(ctx.channel, discord.channel.DMChannel) and CONFESSION_BOOL:

            if confession is None:
                raise MissingArgument("Confession", get_command_description("confess"))
            channel = self.client.get_channel(int(CHANNEL_CONFESSION_ID))

            embed=discord.Embed(
                title=f"New Anonymous Confession!", 
                description=confession
            )

            await channel.send(embed=embed)

        elif isinstance(ctx.channel, discord.channel.DMChannel) and CONFESSION_BOOL == False:
            await ctx.send("Confess is disabled due to misuse of the command.")
    '''
    
    @commands.command(aliases=['color', 'colour', 'role'])
    async def _colour(self, ctx, colour : str = None):
        """?colour <colour>"""

        if colour is None:
            raise MissingArgument("Colour", get_command_description("_colour"))
        
       
        await ctx.message.delete()                 
        role = discord.utils.get(ctx.guild.roles, name=colour.upper())

        try:

            for key in COLOUR_ROLES_DICT.keys():
                if discord.utils.get(ctx.message.guild.roles, name=key) in ctx.author.roles:
                    await ctx.author.remove_roles(discord.utils.get(ctx.guild.roles, name=key))

            await ctx.author.add_roles(role)
            await ctx.send(embed=embed_success(f"Added {role.mention} to {ctx.author.mention}"))

        except Forbidden:
            raise MissingPermissionOnMember("Edit role", ctx.author)

        except AttributeError:
            raise RoleNotFound(colour.upper())
                
    @commands.command()
    async def ping(self, ctx):
        """Sends the ping of the bot"""

        embed=discord.Embed(title=f"", description=f'Pong :ping_pong:    {round(self.client.latency * 1000)}ms!')
        await ctx.reply(embed=embed)
        
    @commands.command(aliases=["av"])
    async def avatar(self, ctx, member : discord.Member=None):
        """Sends an avatar image / gif of [member]"""

        if member == None:
            member = ctx.message.author    
    
        url_png = str(member.avatar_url)[:-14] + "png?size=1024"
        url_jpg = str(member.avatar_url)[:-14] + "jpg?size=1024"
        url_webp = str(member.avatar_url)[:-14] + "webp?size=1024"

        embed=discord.Embed(
            description=f"[PNG]({url_png}) | [JPEG]({url_jpg}) | [WEBP]({url_webp})",
            inline=False, 
            color=0x912aad
            ).set_author(name=f"Avatar for: {member}", icon_url=f"{member.avatar_url}"
        )

        if ".gif?" in str(member.avatar_url):
            embed.set_image(url=f"{member.avatar_url}")
            
        else:
            embed.set_image(url=f"{url_png}")
        
        await ctx.send(embed=embed)
    
    @commands.command(aliases=["whois"])
    async def userinfo(self,ctx, member: discord.Member = None):
        """Sends information about [member]"""

        if not member:
            member = ctx.message.author

        embed = discord.Embed(colour=discord.Colour.purple(), title=f"User Info - {member}"
            ).set_thumbnail(url=member.avatar_url
            ).set_footer(text=f"Requested by {ctx.author}"

            ).add_field(name="ID:", value=member.id
            ).add_field(name="Display Name:", value=member.display_name

            ).add_field(name="Created Account On:", value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC")
            ).add_field(name="Joined Server On:", value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC")

            ).add_field(name="Highest Role:", value=member.top_role.mention
        )
        await ctx.send(embed=embed)
    
    """
    @commands.command()
    @commands.has_permissions(add_reactions=True,embed_links=True)
    async def help(self,ctx, word = "None"):
        # TODO
        pass
    """
def setup(client):
    client.add_cog(Misc(client))