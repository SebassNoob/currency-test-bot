import discord
from discord.ext import commands
from async_functions import addDataCombatInv, getDataCombatInv,chanceExp, getDataBal
import random
import json
import asyncio

class Inventory(commands.Cog):
  def __init__(self, bot):
      self.bot = bot
  
  @commands.command(name = 'combatinventory', aliases = ['combatinv','cinv'])
  async def inventory(self,ctx):
    uid = ctx.message.author.id
    await addDataCombatInv(uid)
    user = await getDataCombatInv()

    itemids = ['g01','g02','g03','g04','g05','a01','a02','h01','h02','h03','h04']
    itemnames=['Semi-auto pistol','Assault rifle','Sniper rifle','Submachine gun', 'Grenade','Kevlar vest','Riot helmet',"Smokebomb",'Cocaine stimulant','Coffee','Gas shell','First-aid kit']

    gunmods = ['none','supressed','scoped','dual','heavy','burst','automatic']
    gunmodids = ['00','01','02','03','04','05','06']

    armourmods = ['none','reinforced','lightweight','deflect','energyshield']
    armourmodids = ['00','01','02','03','04']



    em = discord.Embed(color = 0x000000)
    for items in user[str(uid)]:
      x = items.split('-')
      item = itemnames[itemids.index(x[0])]
      
      mod1 = None
      mod2 = None
      if x[0].startswith("g"):
        y= x[1].split('_')
        lvl = y[0]
        z = y[1].split('/')

        mod1= gunmods[gunmodids.index(str(z[0]))]
        mod2 = gunmods[gunmodids.index(str(z[1]))]

        if x[0] == 'g01':
          emoji = "<:semiautopistol:861530110338793492>"
        if x[0] == 'g02':
          emoji = "<:assaultrifle:861530110461345812>"
        if x[0] == 'g03':
          emoji = "<:sniperrifle:861530164990705675>"
        if x[0] == 'g04':
          emoji = "<:submachinegun:861532743330562068>"
        if x[0] == 'g05':
          emoji = "<:grenade:861533317223809054>"
        em.add_field(name = emoji+" " + str(item), value = "Level: "+str(lvl)+"\nModifier 1: "+str(mod1)+"\nModifier 2: "+str(mod2),inline = True)

      if x[0].startswith("a"):
        y= x[1].split('_')
        lvl = y[0]
        z = y[1].split('/')
        mod1= armourmods[armourmodids.index(str(z[0]))]
        em.add_field(name = str(item), value = "Level: "+str(lvl)+"\nModifier 1: "+str(mod1),inline = True)

      if x[0].startswith("h"):
        value = "Level: "+ x[1]

        em.add_field(name = str(item), value = value,inline = True)
        
      
      
    await ctx.send(embed = em)
    
      


  @commands.command()
  async def buy(self,ctx,*args):
    uid = ctx.message.author.id
    await chanceExp(uid)
    c = ''
    for arg in args:
      c = c +arg
    
    
    itemprices = ['1g','1g','2g','3g','4g','1g','3g','2g','1g','3g','1g','2g']
    itemids = ['g01','g02','g03','g04','g05','a01','a02','h01','h02','h03','h04','h05']
    itemnames=['semiautopistol','assaultrifle','sniperrifle','submachinegun', 'grenade','kevlarvest','riothelmet','smokebomb','cocainestimulant','coffee','gasshell','firstaidkit']
    bal = await getDataBal()
    guntokens = bal[str(uid)]["guntokens"]
    wallet = bal[str(uid)]["wallet"]
    inv = await getDataCombatInv()


    if c in itemnames:
      if len(inv[str(uid)]) < 10:
        itemid = itemids[itemnames.index(c)]

        if itemid.startswith("g"):
          itemid = itemid+"-01_00/00"
        if itemid.startswith("h"):
          
          itemid = itemid+"-01"
        if itemid.startswith("a"):
          itemid = itemid+"-01_00"




        itemprice = itemprices[itemnames.index(c)]
        if itemprice.endswith("g"):
          x= itemprice.split("g")
          value = x[0]
          ty = "guntokens"
          if guntokens >= int(value):
            await ctx.send("The item `" +c+"` will set you back `"+value+"` guntokens. Are you sure you wanna buy it?\nType `y` or `n`.")
          elif guntokens < int(value):
            await ctx.send("You don't have enough guntokens to complete this purchase.")
            raise Exception


        if itemprice.endswith("c"):
          x= itemprice.split("c")
          value = x[0]
          ty = "wallet"
          print(wallet)
          if wallet >= int(value):
            await ctx.send("The item `" +c+"` will set you back Cy$`"+value+"`. Are you sure you wanna buy it?\nType `y` or `n`.")
            
          elif wallet < int(value):
            await ctx.send("You don't have enough money in your wallet to complete this purchase.")
            raise Exception


        def check(msg):
          return msg.author == ctx.author and msg.channel == ctx.channel and msg.content.lower() in ['y','n']
        try:
          msg = await self.bot.wait_for("message",timeout=30,check=check)
          if msg.content == 'y':
            d = {ty: bal[str(uid)][ty] - int(value)}
            bal[str(uid)].update(d)
            
            inv[str(uid)].append(str(itemid))
            
            
            with open("./json_files/userBal.json","w") as f:
              json.dump(bal,f)
            with open("./json_files/userCombatInv.json","w") as f:
              json.dump(inv,f)

            await ctx.reply("You bought `"+c+"` successfully.")

          if msg.content == 'n':
            await ctx.send("You cancelled your purchase.")
          
          
        except asyncio.TimeoutError:
          await ctx.send("You didn't reply in time, so I've cancelled your purchase.")
      else:
        await ctx.send("Your combat inventory is too full! Sell an item free up an inventory slot.")

      
    else:
      await ctx.send("That's not a valid item!")
      raise Exception



    
      
    

    


    




    
def setup(bot):
    bot.add_cog(Inventory(bot))