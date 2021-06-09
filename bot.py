import discord
import os
import re
import random
import sqlite3
import asyncio

from dotenv import load_dotenv
from os.path import dirname, join

dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)
DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")


con = sqlite3.connect("test.db")

cur = con.cursor()

client = discord.Client()


@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("-reg"):
        baba = message.author.id
        cur.execute("SELECT EXISTS(SELECT 1 FROM ramdev WHERE user_id=:hm LIMIT 1)", {"hm": baba})

        record = cur.fetchone()

        if record[0]:
            await message.channel.send("dude you are already registered.")
        else:
            cur.execute("INSERT INTO ramdev VALUES (?, ?)", (baba, 1000))
            print(f"New user registered. UserId: {baba}")
            await message.channel.send("successfully registered")
            con.commit()

    if message.content.startswith("-pky"):
        baba = message.author.id
        cur.execute("SELECT EXISTS(SELECT 1 FROM ramdev WHERE user_id=:hm LIMIT 1)", {"hm": baba})
        record = cur.fetchone()
        if record[0]:

            moni = cur.execute("select moni from ramdev where user_id =:hm", {"hm": baba})
            moni = cur.fetchone()

            money = moni[0]

            await message.channel.send(
                f"{message.author.mention}, you have {money} pakistani yen(the greatest currency of all time allah hu akbar)"
            )
        else:
            await message.channel.send(
                "you are not registered for gambling in this karachi casino of hamood. to register, type '-reg'"
            )

    if message.content.startswith("-gg"):
        await message.channel.send("hm ok. lemme check")
        baba = message.author.id
        cur.execute("SELECT EXISTS(SELECT 1 FROM ramdev WHERE user_id=:hm LIMIT 1)", {"hm": baba})
        record = cur.fetchone()
        if record[0]:

            moni = cur.execute("select moni from ramdev where user_id =:hm", {"hm": baba})

            moni = cur.fetchone()[0]

            x = int(re.sub("[^0-9]", "", message.content))
            if x > moni:
                await message.channel.send("ur broke bruv, stay in ur awkat")
            else:
                cur.execute("update ramdev set moni = moni-:bet where user_id =:hm", {"hm": baba, "bet": x})
                con.commit()
                await message.channel.send(f"uh, {message.author.mention}, the spin wheel spins...")
                await asyncio.sleep(10)
                spin = random.randint(1, 7)
                if spin < 3:
                    await message.channel.send(f"hahaha {message.author.mention}, get fucked! you aint getting money")
                    print(f"Spin number: ${spin}")
                if spin == 3:
                    await message.channel.send(
                        f"{message.author.mention},damn you got the joker thing. check ur money."
                    )
                    jokermoni = random.randint(100, 10000)
                    cur.execute(
                        "update ramdev set moni = moni+:bet where user_id =:hm", {"hm": baba, "bet": x + jokermoni}
                    )
                    con.commit()
                if spin == 4:
                    await message.channel.send(
                        f"uh {message.author.mention}, you got ur money back but you didnt get any bonus or shit like that"
                    )
                    cur.execute("update ramdev set moni = moni+:bet where user_id =:hm", {"hm": baba, "bet": x})
                    con.commit()

                if 5 <= spin < 7:
                    await message.channel.send(f"{message.author.mention}, you got double the money you bet")
                    cur.execute("update ramdev set moni = moni+:bet where user_id =:hm", {"hm": baba, "bet": x * 2})
                    con.commit()
                if spin == 7:
                    await message.channel.send(f"{message.author.mention}, you got triple the money you bet")
                    cur.execute("update ramdev set moni = moni+:bet where user_id =:hm", {"hm": baba, "bet": x * 3})
                    con.commit()
        else:
            await message.channel.send(
                "you are not registered for gambling in this karachi casino of hamood. to register, type '-reg'"
            )
    if message.content.startswith("-moni"):
        baba = message.author.id
        cur.execute("SELECT EXISTS(SELECT 1 FROM ramdev WHERE user_id=:hm LIMIT 1)", {"hm": baba})
        record = cur.fetchone()
        if record[0]:
            moni = cur.execute("select moni from ramdev where user_id =:hm", {"hm": baba})

            moni = cur.fetchone()[0]

            if moni > 2000:
                await message.channel.send("dude you have enough money")

            else:
                cur.execute("update ramdev set moni = 2000 where user_id =:hm", {"hm": baba})

                con.commit()
                await message.channel.send(f"{message.author.mention}, you have 2000 pky.")
        else:
            await message.channel.send(
                "you are not registered for gambling in this karachi casino of hamood. to register, type '-reg'"
            )


client.run(DISCORD_TOKEN)
