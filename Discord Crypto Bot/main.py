import discord
import requests
from replit import db
from threading import Timer
from keep_alive import keep_alive

# check whether the priceTargets are integers
def check(priceTargets):
  try:
    return all(isinstance(int(x),int) for x in priceTargets)
  except:
    return False

# getting crypto data
def getCryptoPrices(crypto):
  URL ='https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd'
  r = requests.get(url=URL)
  data = r.json()

  # putting the cryptocurrencies and their prices in db
  for i in range(len(data)):
    db[data[i]['id']] = data[i]['current_price']

  if crypto in db.keys():
    return db[crypto]
  else:
    return None

# check if a cryptocurrency is supported in this bot
def isCryptoSupported(crypto):
  if crypto in db.keys():
    return True
  else:
    return False

def checkPriceTrend(startPrice,endPrice,priceTargets):
    if startPrice < endPrice:
        return normal_alert(startPrice,endPrice)
    elif startPrice == endPrice:
        return []
    else:
        return reverse_alert(startPrice,endPrice,priceTargets)
        
def reverse_alert(startPrice,endPrice,priceTargets):
    noti = []
    priceTargets = priceTargets[::-1]
    for priceTarget in priceTargets:
        if endPrice <= priceTarget:
            noti.append(priceTarget)
        else:
            continue
    return noti
 
def normal_alert(startPrice,endPrice,priceTargets):
    noti = []
    for priceTarget in priceTargets:
        if priceTarget <= endPrice:
            noti.append(priceTarget)
        else:
            continue
    return noti

def checkTwoListOrder(list1,list2):
    sorted_elements_1 = [list1[index] <= list1[index+1] for index in range(len(list1)-1)]
    sorted_elements_2 = [list2[index] <= list2[index+1] for index in range(len(list2)-1)]
    return all(sorted_elements_1) and all(sorted_elements_2)

# send discord notificaiton to a channel
async def sendMessage(message):
  await discord.utils.get(client.get_all_channels(),name='general').send(message)

# detecting price alerts
async def detectPriceAlert(crypto,priceTargets):
  current_price = getCryptoPrices(crypto)

  if db['hitPriceTarget'] not in range(min(current_price,db['hitPriceTarget']),max(current_price,db['hitPriceTarget'])+1) and min(priceTargets) <= current_price <= max(priceTargets):
        db['hitPriceTarget'] = 0
  else:
      # compute noti
      if len(checkPriceTrend(db['hitPriceTarget'],current_price,priceTargets)) != 0:
          if db['noti']!= checkPriceTrend(db['hitPriceTarget'],current_price,priceTargets):
              # increasing in value: 
              if db['hitPriceTarget'] < current_price:
                  if checkTwoListOrder(normal_alert(db['hitPriceTarget'],current_price),db['noti']):
                    for priceTarget in list(set(normal_alert(db["hitPriceTarget"],current_price)) - set(db["noti"])):
                        await sendMessage(f'The price of {crypto} has just passed {priceTarget} USD. The current price is: {current_price} USD.')
                  else:
                    for priceTarget in list(set(normal_alert(db["hitPriceTarget"],current_price)) - set(db["noti"])):
                      await sendMessage(f'The price of {crypto} has just passed {priceTarget} USD. The current price is: {current_price} USD.')
                  
              # decreasing in value:
              elif db['hitPriceTarget'] >= current_price:
                  if checkTwoListOrder(reverse_alert(db['hitPriceTarget'],current_price,priceTargets),db["noti"]):
                    for priceTarget in list(set(db["noti"]) - set(reverse_alert(db["hitPriceTarget"],current_price,priceTargets))):
                      await sendMessage(f'The price of {crypto} has just fallen below {priceTarget} USD. The current price is: {current_price} USD.')
                  else:
                    for priceTarget in list(set(db["noti"]) - set(reverse_alert(db["hitPriceTarget"],current_price,priceTargets))):
                      await sendMessage(f'The price of {crypto} has just fallen below {priceTarget} USD. The current price is: {current_price} USD.')
              else:
                  pass
  
          if db['hitPriceTarget'] < current_price:
              db["noti"]= normal_alert(db['hitPriceTarget'],current_price)
              db['hitPriceTarget'] = max(normal_alert(db['hitPriceTarget'],current_price))
              
          if db['hitPriceTarget'] > current_price:
              db["noti"]= reverse_alert(db['hitPriceTarget'],current_price,priceTargets)
              db['hitPriceTarget'] = min(reverse_alert(db['hitPriceTarget'],current_price,priceTargets))
              
      else:
          db['hitPriceTarget'] = 0

  # set a thread that runs detectPriceAlert every 5 seconds
  Timer(5.0, await detectPriceAlert(crypto,priceTargets)).start() 
  print("--Finished--")



# instantiate a discord client
client = discord.Client()

@client.event
async def on_ready():
  print(f'You have logged in as {client}')
  channel = discord.utils.get(client.get_all_channels(),name='general')

  db['hitPriceTarget'] = 0
  db['noti'] = []

  await client.get_channel(channel.id).send('bot is now online!')

# called whether there is a message in the chat
@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.content.startswith('ya'):
    await message.channel.send('yeet')

  # send crypto price directly 
  if message.content.lower() in db.keys():
    await message.channel.send(f'The current price of {message.content} is: {getCryptoPrices(message.content.lower())} USD')

  # list all the available coins
  if message.content.startswith('$list'):
    cryptoSupportedList = [key for key in db.keys()]
    await message.channel.send(cryptoSupportedList)

  # check whether a coin is being supported
  if message.content.startswith('$support '):
    cryptoToBeChecked = message.content.split('$support ',1)[1].lower()
    await message.channel.send(isCryptoSupported(cryptoToBeChecked))

  # setting mutliple price alerts
  if message.content.startswith('$set '):
    messageList = message.content.split(' ')
    cryptoConcerned = messageList[1]

    priceTargets = []
    for i in range(len(messageList) - 2):
      priceTargets.append(int(messageList[2 + i]))

    # input validation
    if isCryptoSupported(cryptoConcerned) and check(priceTargets):
      db['detect crypto'] = cryptoConcerned
      db['detect price'] = priceTargets

      await message.channel.send(f'Successfully set price alert for {db["detect crypto"]} at {list(db["detect price"])} USD.')

    else:
      await message.channel.send(f'Unsuccessful setting of price alerts. Please try again.')

  if message.content.startswith('$start'):
    await message.channel.send(f'Started detecting price alert for {db["detect crypto"]} at {list(db["detect price"])} USD.')
    await detectPriceAlert(db["detect crypto"],db["detect price"])
  

keep_alive()

BOT_TOKEN = 'YOUR_BOT_TOKEN'
client.run(BOT_TOKEN)