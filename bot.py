import discord
import os
import re
import random
import time

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

moni = 1000

@client.event
async def on_message(message):
    if message.author == client.user:
      return
    
    global moni

    if message.content.startswith("-pky"):
      await message.channel.send(f"{message.author.mention}, you have {moni} pakistani yen(the greatest currency of all time allah hu akbar)")

    if message.content.startswith('-gg'):
      await message.channel.send('hm ok. lemme check')

      x = int(re.sub('[^0-9]', '', message.content))
      if x > moni:
        await message.channel.send('ur broke bruv, stay in ur awkat')
      else:
        moni -= x
        await message.channel.send(f'uh, {message.author.mention}, the spin wheel spins...')
        time.sleep(10)
        spin = random.randint(1,6)
        if spin <= 3:
          await message.channel.send(f'hahaha {message.author.mention}, get fucked! you aint getting money')
        if spin == 4:
          await message.channel.send(f'uh {message.author.mention}, you got ur money back but you didnt get any bonus or shit like that')
          moni += x
        if spin == 5:
          await message.channel.send(f'{message.author.mention}, you got double the money you bet')
          moni += x*2
        if spin == 6:
          await message.channel.send(f"{message.author.mention}, you got triple the money you bet")
          moni += x*3

client.run(os.getenv('token'))
