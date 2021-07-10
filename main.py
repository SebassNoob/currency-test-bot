import os
import discord
from discord.ext import commands
from async_functions import addDataBal, addDataCombatInv,addDataLoadout,addDataLvl, addDataInv
from keepAlive import keep_alive


#startup:
bot = commands.Bot(command_prefix='.', help_command = None)


@bot.event
async def on_message(message):
  if message.author == bot.user:
    return
  else:
    await addDataInv(message.author.id)
    await addDataBal(message.author.id)
    await addDataCombatInv(message.author.id)
    await addDataLoadout(message.author.id)
    await addDataLvl(message.author.id)
    await bot.process_commands(message)


@bot.event
async def on_ready():
  print("------------------------")
  print('{0.user}'.format(bot)+ " connected")
  print("------------------------")
  

@bot.event
async def on_command_error(ctx, error):
    
    if isinstance(error, discord.ext.commands.MissingRequiredArgument):
        await ctx.reply("You're missing an argument in that command, try again!")
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.reply('This command is on a **%.1fs** cooldown.' % error.retry_after)
    if isinstance(error, discord.ext.commands.CommandNotFound):
        pass

#cogs:
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')





keep_alive()
bot.run(os.getenv('TOKEN'))