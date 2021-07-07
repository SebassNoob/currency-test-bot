import discord
from discord.ext import commands
from async_functions import addDataLoadout, getDataLoadout
import random
import json
import asyncio

class Loadout(commands.Cog):
  def __init__(self, bot):
      self.bot = bot
  



  @commands.command(name = 'setLoadout', aliases = ['setl','setloadout'])
  async def setloadout(self,ctx,*args):
    uid = ctx.message.author.id
    await addDataLoadout(uid)
    user = await getDataLoadout()
    
    c = ''
    for arg in args:
      c = c +arg
    

    #001
    if c == 'semiautopistol':
      await ctx.send("Which slot would you like to place a *semi-auto pistol* in?\n Type `1 or 2`.")
      def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel and msg.content.lower() in ["1", "2"]
      try:
        msg = await self.bot.wait_for("message",timeout=30,check=check)
        a=''
        if msg.content == '1':
          a = 'slot1'
        if msg.content == '2':
          a = 'slot2'
        
        

        
        d = {a : '001'}
        user[str(uid)].update(d)
        with open("./json_files/userLoadout.json","w") as f:
          json.dump(user,f)
        
        await ctx.send("You've set *semi-auto pistol*  to slot `"+ msg.content +'`')
      except asyncio.TimeoutError:
        await ctx.send("You didn't reply in time!")



    #002
    if c == 'assaultrifle':
      await ctx.send("Which slot would you like to place a *assault rifle* in?\n Type `1, 2 or 3`.")
      def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel and msg.content.lower() in ["1", "2","3"]
      try:
        msg = await self.bot.wait_for("message",timeout=30,check=check)
        a=''
        if msg.content == '1':
          a = 'slot1'
        if msg.content == '2':
          a = 'slot2'
        if msg.content == '3':
          a = 'slot3'
        
          
        

        
        d = {a : '002'}
        user[str(uid)].update(d)
        with open("./json_files/userLoadout.json","w") as f:
          json.dump(user,f)
        
        await ctx.send("You've set *assault rifle*  to slot `"+ msg.content +'`')
      except asyncio.TimeoutError:
        await ctx.send("You didn't reply in time!")


    #003
    if c == 'sniperrifle':
      await ctx.send("Which slot would you like to place a *sniper rifle* in?\n Type `1, 2 or 3`.")
      def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel and msg.content.lower() in ["1", "2","3"]
      try:
        msg = await self.bot.wait_for("message",timeout=30,check=check)
        a=''
        if msg.content == '1':
          a = 'slot1'
        if msg.content == '2':
          a = 'slot2'
        if msg.content == '3':
          a = 'slot3'
        
          
        

        
        d = {a : '003'}
        user[str(uid)].update(d)
        with open("./json_files/userLoadout.json","w") as f:
          json.dump(user,f)
        
        await ctx.send("You've set *sniper rifle*  to slot `"+ msg.content +'`')
      except asyncio.TimeoutError:
        await ctx.send("You didn't reply in time!")
        
    #004
    if c == 'submachinegun':
      await ctx.send("Which slot would you like to place a *submachine gun* in?\n Type `1, 2 or 3`.")
      def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel and msg.content.lower() in ["1", "2","3"]
      try:
        msg = await self.bot.wait_for("message",timeout=30,check=check)
        a=''
        if msg.content == '1':
          a = 'slot1'
        if msg.content == '2':
          a = 'slot2'
        if msg.content == '3':
          a = 'slot3'
        
          
        

        
        d = {a : '004'}
        user[str(uid)].update(d)
        with open("./json_files/userLoadout.json","w") as f:
          json.dump(user,f)
        
        await ctx.send("You've set *submachine gun*  to slot `"+ msg.content +'`')
      except asyncio.TimeoutError:
        await ctx.send("You didn't reply in time!")


    #005
    if c == 'grenade':
      await ctx.send("Which slot would you like to place a *grenade* in?\n Type `1, 2 or 3`.")
      def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel and msg.content.lower() in ["1", "2","3"]
      try:
        msg = await self.bot.wait_for("message",timeout=30,check=check)
        a=''
        if msg.content == '1':
          a = 'slot1'
        if msg.content == '2':
          a = 'slot2'
        if msg.content == '3':
          a = 'slot3'
        
          
        

        
        d = {a : '005'}
        user[str(uid)].update(d)
        with open("./json_files/userLoadout.json","w") as f:
          json.dump(user,f)
        
        await ctx.send("You've set *grenade*  to slot `"+ msg.content +'`')
      except asyncio.TimeoutError:
        await ctx.send("You didn't reply in time!")

    if c == 'bunchograpes':
      d = {'healing' : '101'}
      user[str(uid)].update(d)
      with open("./json_files/userLoadout.json","w") as f:
        json.dump(user,f)
        
      await ctx.send("You've set *bunch o grapes*  to your healing slot")








  @commands.command()
  async def loadout(self,ctx):
    uid = ctx.message.author.id
    await addDataLoadout(uid)
    user = await getDataLoadout()
    
    slot1 = user[str(uid)]["slot1"]
    slot2 = user[str(uid)]["slot2"]
    slot3 = user[str(uid)]["slot3"]
    healing = user[str(uid)]["healing"]
    
    
    if slot1 == None:
      slot1 = "Nothing equipped."
    if slot2 == None:
      slot2 = "Nothing equipped."
    if slot3 == None:
      slot3 = "Nothing equipped."
    if healing == None:
      healing = "Nothing equipped."
    
    
    






    
    embedVar = discord.Embed( color=0x000000)
    embedVar.set_author(name='{}'.format(ctx.author), icon_url = ctx.author.avatar_url)
    embedVar.add_field(name='**Slot 1:**', value = str(slot1), inline = True)
    embedVar.add_field(name='**Slot 2:**', value = str(slot2), inline = True)
    embedVar.add_field(name='**Slot 3:**', value = str(slot3), inline = True)
    embedVar.add_field(name='**Healing:**', value = str(healing), inline = True)
    
    await ctx.send(embed=embedVar)



    
    



def setup(bot):
    bot.add_cog(Loadout(bot))