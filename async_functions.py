
import json
import random
import asyncio


async def addDataBal(uid):
  
  user = await getDataBal()
  if str(uid) in user:
    return False
  else:
    user[str(uid)] = {}
    user[str(uid)]["wallet"] = 0
    user[str(uid)]["bank"] = 0
    user[str(uid)]["bankspace"] = 1000
    user[str(uid)]["guntokens"] = 0


  with open("./json_files/userBal.json","w") as f:
    json.dump(user,f)
  return True

async def getDataBal():
  with open("./json_files/userBal.json","r") as f:
    user = json.load(f)
  return user

async def addDataLoadout(uid):
  
  user = await getDataLoadout()
  if str(uid) in user:
    return False
  else:
    user[str(uid)] = {}
    user[str(uid)]["slot1"] = 'g01-01_00/00'
    user[str(uid)]["slot2"] = None
    user[str(uid)]["armour"] = None
    user[str(uid)]["misc"] = None


  with open("./json_files/userLoadout.json","w") as f:
    json.dump(user,f)
  return True


async def getDataLoadout():
  with open("./json_files/userLoadout.json","r") as f:
    user = json.load(f)
  return user


async def addDataCombatInv(uid):
  
  user = await getDataCombatInv()
  if str(uid) in user:
    return False
  else:
    user = {}
    user[str(uid)] = ['g01-01_00/00']
    


  with open("./json_files/userCombatInv.json","w") as f:
    json.dump(user,f)
  return True


async def getDataCombatInv():
  with open("./json_files/userCombatInv.json","r") as f:
    user = json.load(f)
  return user


async def addDataLvl(uid):
  
  user = await getDataLvl()
  if str(uid) in user:
    return False
  else:
    user[str(uid)] = {}
    user[str(uid)]["level"] = 0
    user[str(uid)]["exp"] = 0
    


  with open("./json_files/userLevel.json","w") as f:
    json.dump(user,f)
  return True

async def getDataLvl():
  with open("./json_files/userLevel.json","r") as f:
    user = json.load(f)
  return user


async def add_experience(bal,user, uid, exp):
  user[str(uid)]['exp'] += exp
  bal[str(uid)]['bankspace'] += exp*50
  with open("./json_files/userLevel.json","w") as f:
    json.dump(user, f)
  with open("./json_files/userBal.json","w") as f:
    json.dump(bal, f)

async def level_up(user, uid):
  if user[str(uid)]['exp'] >= 100:
    user[str(uid)]['exp'] -= 100
    user[str(uid)]['level'] += 1
    
    with open("./json_files/userLevel.json","w") as f:
      json.dump(user, f)
  else:
    pass


 
  


async def chanceExp(uid):
  user = await getDataLvl()
  userBal = await getDataBal()
  n = random.randint(0,2)
  if n == 2:
    await add_experience(userBal,user,uid,1)
  await level_up(user,uid)
  
  prev_tokens = userBal[str(uid)]['guntokens']
  
  if user[str(uid)]['level'] % 2 == 0 and user[str(uid)]['exp'] == 0:
    
    d = {"guntokens" : prev_tokens + 1}
    userBal[str(uid)].update(d)
    
    with open("./json_files/userBal.json","w") as f:
      json.dump(userBal,f)
      
      
  
    
    
async def addDataInv(uid):
  
  user = await getDataInv()
  if str(uid) in user:
    return False
  else:
    user[str(uid)] = {}
    user[str(uid)]["item1"] = '0'
    
    
    


  with open("./json_files/userInv.json","w") as f:
    json.dump(user,f)
  return True


async def getDataInv():
  with open("./json_files/userInv.json","r") as f:
    user = json.load(f)
  return user