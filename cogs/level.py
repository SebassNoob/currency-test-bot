import discord
from discord.ext import commands
from async_functions import getDataLvl,getDataBal,getDataCombatInv
import random
import json
import asyncio

class Level(commands.Cog):
  def __init__(self, bot):
      self.bot = bot

  @commands.command()
  async def profile(self,ctx):
    uid = ctx.message.author.id
    userLvl = await getDataLvl()
    lvl = userLvl[str(uid)]['level']
    exp = userLvl[str(uid)]['exp']
    userBal = await getDataBal()
    wallet = userBal[str(uid)]['wallet']
    bank = userBal[str(uid)]['bank']
    bankspace = userBal[str(uid)]['bankspace']
    tokens = userBal[str(uid)]['guntokens']
    userInv = await getDataCombatInv()
    invNo = len(userInv.keys())

    em = discord.Embed(color = 0x000000)
    em.set_author(name='{}'.format(ctx.author)+"'s profile", icon_url = ctx.author.avatar_url)
    em.add_field(name = "**Level info**", value = "Level: `"+str(lvl)+"`\nExperience: `"+str(exp)+"`",inline = True)
    em.add_field(name = "**Coins info**", value = "Wallet: Cy$`"+str(wallet)+"`\nBank: Cy$`"+str(bank)+"`\nBankspace: Cy$`"+str(bankspace)+"`\n Gun tokens: `"+str(tokens)+"`",inline = True)
    em.add_field(name = "**Inventory**", value = str(invNo) + " items",inline = True)
    await ctx.send(embed = em)



def setup(bot):
    bot.add_cog(Level(bot))