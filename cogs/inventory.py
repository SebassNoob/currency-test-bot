import discord
from discord.ext import commands
from async_functions import addDataCombatInv, getDataCombatInv,chanceExp, getDataBal, getDataInv
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
  async def buy(self,ctx,c, itemno = None):
    uid = ctx.message.author.id
    await chanceExp(uid)
    
    
    
    combatitemprices = ['1g','1g','2g','3g','4g','1g','3g','2g','1g','3g','1g','2g']
    combatitemids = ['g01','g02','g03','g04','g05','a01','a02','h01','h02','h03','h04','h05']
    combatitemnames=['semiautopistol','assaultrifle','sniperrifle','submachinegun', 'grenade','kevlarvest','riothelmet','smokebomb','cocainestimulant','coffee','gasshell','firstaidkit']

    itemprices = ['1000c','2000c']
    
    itemnames = ['item1','item2']
    bal = await getDataBal()
    guntokens = bal[str(uid)]["guntokens"]
    wallet = bal[str(uid)]["wallet"]
    combatinv = await getDataCombatInv()
    inv = await getDataInv()
    #combatinv buy

    def findStr(string,arr):
      for i in arr:
        if string in i:
          return True

    
      
    if c in combatitemnames and itemno == None:
      
      if findStr(combatitemids[combatitemnames.index(c)],combatinv[str(uid)]) ==None:
        
        if len(combatinv[str(uid)]) < 10:
          itemid = combatitemids[combatitemnames.index(c)]
          if itemid.startswith("g"):
            itemid = itemid+"-01_00/00"
          if itemid.startswith("h"):
            itemid = itemid+"-01"
          if itemid.startswith("a"):
            itemid = itemid+"-01_00"
          itemprice = combatitemprices[combatitemnames.index(c)]
          if itemprice.endswith("g"):
            x= itemprice.split("g")
            value = x[0]
            if guntokens >= int(value):
              await ctx.send("The item `" +c+"` will set you back `"+value+"` guntokens. Are you sure you wanna buy it?\nType `y` or `n`.")
            elif guntokens < int(value):
              await ctx.send("You don't have enough guntokens to complete this purchase.")
              raise Exception
          def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel and msg.content.lower() in ['y','n']
          try:
            msg = await self.bot.wait_for("message",timeout=30,check=check)
            if msg.content == 'y':
              d = {"guntokens": bal[str(uid)]["guntokens"] - int(value)}
              bal[str(uid)].update(d)
              combatinv[str(uid)].append(str(itemid))
              with open("./json_files/userBal.json","w") as f:
                json.dump(bal,f)
              with open("./json_files/userCombatInv.json","w") as f:
                json.dump(combatinv,f)
              await ctx.reply("You bought `"+c+"` successfully.")
            if msg.content == 'n':
              await ctx.send("You cancelled your purchase.") 
          except asyncio.TimeoutError:
            await ctx.send("You didn't reply in time, so I've cancelled your purchase.")
        else:
          await ctx.send("Your combat inventory is too full! Sell an item free up an inventory slot.")
      else:
        await ctx.send("You already have an item of the same type!")

    #normalinv buy
    elif c in itemnames:
      
      itemprice = itemprices[itemnames.index(c)]
      if itemno == None:
        itemno = 1
      
      if itemprice.endswith("c"):
          x= itemprice.split("c")
          value = int(x[0])*int(itemno)
          
          
          if wallet >= int(value):
            d = {"wallet": bal[str(uid)]["wallet"] - int(value)}
            bal[str(uid)].update(d)
            
            if not c in inv[str(uid)]:
              
              inv[str(uid)][c] = itemno
            else:
              
              e = {c: int(inv[str(uid)][c]) + int(itemno)}
              inv[str(uid)].update(e)
            
            with open("./json_files/userBal.json","w") as f:
              json.dump(bal,f)
            with open("./json_files/userInv.json","w") as f:
              json.dump(inv,f)

            await ctx.reply("You bought "+itemno+" `"+c+"` successfully.")
            
          elif wallet < int(value):
            await ctx.send("You don't have enough money in your wallet to complete this purchase.")
            raise Exception
    else:
      await ctx.send("That's not a valid item!")
      raise Exception


  @commands.command()
  async def sell(self,ctx,c):
    uid = ctx.message.author.id
    combatitemprices = ['1g','1g','2g','3g','4g','1g','3g','2g','1g','3g','1g','2g']
    combatitemids = ['g01','g02','g03','g04','g05','a01','a02','h01','h02','h03','h04','h05']
    combatitemnames=['semiautopistol','assaultrifle','sniperrifle','submachinegun', 'grenade','kevlarvest','riothelmet','smokebomb','cocainestimulant','coffee','gasshell','firstaidkit']

    itemprices = ['1000c','2000c']
      
    itemnames = ['item1','item2']

    bal = await getDataBal()
    guntokens = bal[str(uid)]["guntokens"]
    wallet = bal[str(uid)]["wallet"]
    combatinv = await getDataCombatInv()
    inv = await getDataInv()

    def findStrTorN(string,arr):
        for i in arr:
          if string in i:
            return True

    def findStr(string,arr):
        for i in arr:
          if string in i:
            return i
   
    if c in combatitemnames:
      tid = combatitemids[combatitemnames.index(c)]
      
      if findStrTorN(tid, combatinv[str(uid)]) ==True:
        itemid = findStr(tid,combatinv[str(uid)])
        

      
        
      

    


    




    
def setup(bot):
    bot.add_cog(Inventory(bot))