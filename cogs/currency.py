import discord
from discord.ext import commands
from async_functions import addDataBal, getDataBal, chanceExp
import random
import json
import asyncio

class Currency(commands.Cog):
  def __init__(self, bot):
        self.bot = bot


  @commands.cooldown(1,3)
  @commands.command()
  async def beg(self, ctx):

    uid = ctx.message.author.id
    await chanceExp(uid)
    
    user = await getDataBal()
    

    prevAmt = user[str(uid)]["wallet"]

    
    begChances = [0,random.randint(10,100),random.randint(100,300)]
    begAmt = random.choices(begChances, weights = [3, 2, 1])[0]
    

    d = {"wallet" : prevAmt + begAmt}
    user[str(uid)].update(d)
    
    with open("./json_files/userBal.json","w") as f:
      json.dump(user,f)

    await ctx.send("You gained: Cy$**"+str(begAmt)+"**")
  

  @commands.command(name = 'deposit', aliases = ["dep"])
  async def deposit(self,ctx, arg):
    uid = ctx.message.author.id
    await addDataBal(uid)
    user = await getDataBal()
    wallet = user[str(uid)]["wallet"]
    bank = user[str(uid)]["bank"]
    space = user[str(uid)]["bankspace"]

    if arg == 'all' or arg == 'max':
      arg = str(wallet)
    if arg == 'half':
      arg = str(wallet/2)

    if arg.isdigit() == True:
      


      if (bank + int(arg)) > space:
        arg = space - bank
        
        if arg == 0:
          await ctx.send("Your bank is full!")
        else:
          d = {"wallet" : wallet - int(arg), "bank" : bank + int(arg)}
          user[str(uid)].update(d)

          with open("./json_files/userBal.json","w") as f:
            json.dump(user,f)
          await ctx.send("Cy$**"+str(arg)+'** deposited.')


      if wallet < int(arg):
        await ctx.send("You only have Cy$**"+str(wallet)+"**, in your wallet, and can't deposit that much.")


      if (bank + int(arg)) < space and wallet > int(arg):
        d = {"wallet" : wallet - int(arg), "bank" : bank + int(arg)}
        user[str(uid)].update(d)

        with open("./json_files/userBal.json","w") as f:
          json.dump(user,f)
        await ctx.send("Cy$**"+str(arg)+'** deposited.')
    else:
      await ctx.send("That's not a valid number?!")


  @commands.command(name = 'withdraw', aliases = ["with"])
  async def withdraw(self,ctx, arg):
    uid = ctx.message.author.id
    await addDataBal(uid)
    user = await getDataBal()
    wallet = user[str(uid)]["wallet"]
    bank = user[str(uid)]["bank"]

    if arg == 'all' or arg == 'max':
      arg = str(bank)
    if arg == 'half':
      arg = str(bank/2)
    
    if arg.isdigit() == True:
      
      if bank < int(arg):
        await ctx.send("You only have Cy$**"+str(bank)+"** in your bank, and can't withdraw that much.")
      
      else:
        d = {"wallet" : wallet + int(arg), "bank" : bank - int(arg)}
        user[str(uid)].update(d)

        with open("./json_files/userBal.json","w") as f:
          json.dump(user,f)
        await ctx.send("Cy$**"+str(arg)+'** withdrawn.')
    else:
      await ctx.send("That's not a valid number?!")


  @commands.command(name = 'balance', aliases = ['bal'])
  async def balance(self,ctx):
    uid = ctx.message.author.id
    await addDataBal(uid)
    user = await getDataBal()
    wallet = user[str(uid)]["wallet"]
    bank = user[str(uid)]["bank"]
    space = user[str(uid)]["bankspace"]
    
    
    

    em = discord.Embed(color = 0x00ff00)
    
    em.add_field(name ='{}'.format(ctx.author)+"'s balance" , value = "**Wallet**: Cy$ `"+ str(wallet)+"`\n**Bank**: Cy$ `"+ str(bank) +'/'+str(space)+'`', inline = False)
    await ctx.send(embed = em)





def setup(bot):
    bot.add_cog(Currency(bot))