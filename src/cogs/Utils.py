import discord
from discord.ext import commands
import subprocess
import aiohttp
import json
import os
import sys
from control.model.users import Perms



class Utils(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        


    @commands.command(name='echo',description='O bot repete qualquer frase que for esccrita.')
    async def echo(self,ctx, *args):
        await ctx.message.delete()
        value = ' '.join(args)
        await ctx.send(value)



    @commands.command(name='avatar', description='Mostra o avatar de alguem que seja identificado ou o seu próprio caso não seja dado argumento')
    async def avatar(self,ctx,args: discord.User=None):
        embed = discord.Embed(color=self.bot.embed_color)
        if args == None:
            embed.set_image(url=ctx.message.author.avatar_url)
        else:
            embed.set_image(url=args.avatar_url)
        await ctx.send(embed=embed)



    @commands.command(name='setavatar', description='Altera o avatar do bot.\n Necessita de ser um link para uma imagem quadrada',brief=Perms.ADMIN)
    async def setavatar(self,ctx, url_or_mention=None):

        if url_or_mention == None and ctx.message.attachments[0] != None:
            url_or_mention = ctx.message.attachments[0].url
        elif url_or_mention.startswith('<'):
            print(ctx.message.mentions[0].avatar)
            try:
                url_or_mention = "https://cdn.discordapp.com/avatars/" + str(ctx.message.mentions[0].id) + "/" + ctx.message.mentions[0].avatar + ".png?size=1024"
                print(url_or_mention)
            except Exception as error:
                print(error)
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url_or_mention) as r:
                data = await r.read()
        
        try:
            await self.bot.user.edit(avatar=data)
            await ctx.send('Avatar mudado com sucesso')
        except Exception as error:
            await ctx.send(error)



    @commands.command(name='setgame', description='Muda o jogo que o bot esta a jogar para o que estiver escrito na string do argumento', brief=Perms.ADMIN)
    async def setgame(self,ctx,*args):
        output = ' '.join(args)
        await self.bot.change_presence(activity=discord.Game(name=str(output)))



    @commands.command(name='clear', description='Limpa um máximo de 100 mensagens e se nao for lhe dado um argumento limpa apenas 2 (a contar com o comando).', brief=Perms.ADMIN)
    async def clear(self,ctx, amount=1):
        channel = ctx.message.channel
        messages = []
        async for message in channel.history(limit=int(amount) + 1):   
            await message.delete()   


    @commands.command(name="test",description="test")
    async def test(self,ctx,):
        await ctx.send("Test command!")


#    @commands.command(name='cantina',description='Ementa da cantina da UMinho')
#    async def cantina(self,ctx):
#        usr = self.bot.get_user(418819228632612865)#181002804813496320)#
#        print(usr)
#        await usr.send('*cantina')
#        i = usr.dm_channel.history(limit=1)
#        async for msg in i:
#            embed = msg.embeds[0]
#        await ctx.send(embed=embed)



def setup(bot):
    bot.add_cog(Utils(bot))


#def convert_menu(menu):
##get a list of string and returna string in all lower cases
#    menu = ' '.join(menu)
#    return menu.lower()