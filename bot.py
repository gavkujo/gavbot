import asyncio
import os
import random
import re
import sqlite3
from os.path import dirname, join

import discord
from dotenv import load_dotenv

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
    user_id = message.author.id
    if message.author == client.user:
        return

    if message.content.startswith("-reg"):
        cur.execute("SELECT EXISTS(SELECT 1 FROM ramdev WHERE user_id=:user_id LIMIT 1)", {"user_id": user_id})

        record = cur.fetchone()

        if record[0]:
            await message.channel.send("dude you are already registered.")
        else:
            cur.execute("INSERT INTO ramdev VALUES (?, ?, ?)", (user_id, 1000, 0))
            print(f"New user registered. UserId: {user_id}")
            await message.channel.send("successfully registered")
            con.commit()

    elif message.content.startswith("-gg"):
        try:
            bet_amount = int(re.sub("[^0-9]", "", message.content))

            if isinstance(bet_amount, int):
                await message.channel.send("hm ok. lemme check")

            cur.execute("SELECT EXISTS(SELECT 1 FROM ramdev WHERE user_id=:user_id LIMIT 1)", {"user_id": user_id})

            record = cur.fetchone()

            if record[0]:

                moni = cur.execute("select moni from ramdev where user_id =:user_id", {"user_id": user_id})

                moni = cur.fetchone()[0]

                if bet_amount > moni:
                    await message.channel.send("ur broke bruv, stay in ur awkat")
                else:
                    cur.execute(
                        "update ramdev set moni = moni-:bet where user_id =:user_id",
                        {"user_id": user_id, "bet": bet_amount},
                    )
                    con.commit()
                    await message.channel.send(f"uh, {message.author.mention}, the spin wheel spins...")
                    await asyncio.sleep(10)
                    spin = random.randint(1, 7)
                    if spin < 3:
                        await message.channel.send(
                            f"hahaha {message.author.mention}, get fucked! you aint getting money"
                        )
                        print(f"Spin number: {spin}")
                    if spin == 3:
                        await message.channel.send(
                            f"{message.author.mention}, damn you got the joker thing. check ur money."
                        )
                        joker_easter_egg = random.randint(100, 10000)
                        cur.execute(
                            "update ramdev set moni = moni+:bet where user_id =:user_id",
                            {"user_id": user_id, "bet": bet_amount + joker_easter_egg},
                        )
                        con.commit()
                    if spin == 4:
                        await message.channel.send(
                            f"uh {message.author.mention}, you got ur money back but you didnt get any bonus or shit like that"
                        )
                        cur.execute(
                            "update ramdev set moni = moni+:bet where user_id =:user_id",
                            {"user_id": user_id, "bet": bet_amount},
                        )
                        con.commit()

                    if 5 <= spin < 7:
                        await message.channel.send(f"{message.author.mention}, you got double the money you bet")
                        cur.execute(
                            "update ramdev set moni = moni+:bet where user_id =:user_id",
                            {"user_id": user_id, "bet": bet_amount * 2},
                        )
                        con.commit()
                    if spin == 7:
                        await message.channel.send(f"{message.author.mention}, you got triple the money you bet")
                        cur.execute(
                            "update ramdev set moni = moni+:bet where user_id =:user_id",
                            {"user_id": user_id, "bet": bet_amount * 3},
                        )
                        con.commit()
        except:
            await message.channel.send("type a number, dude")

        else:
            await message.channel.send(
                "you are not registered for gambling in this karachi casino of hamood. to register, type '-reg'"
            )

    elif message.content.startswith("-loan"):
        try:
            loan_amount = int(re.sub("[^0-9]", "", message.content))
            if isinstance(loan_amount, int):
                cur.execute("SELECT EXISTS(SELECT 1 FROM ramdev WHERE user_id=:user_id LIMIT 1)", {"user_id": user_id})
                record = cur.fetchone()
                if record[0]:
                    if loan_amount >= 694200:
                        await message.channel.send("ayo awkat ke bahar calm down")
                    else:
                        cur.execute(
                            "UPDATE ramdev SET moni = moni+:loan, loan = loan+:loan WHERE user_id =:user_id",
                            {"user_id": user_id, "loan": loan_amount},
                        )
                        con.commit()
                        print("added loan")
                        await message.channel.send(
                            f"{message.author.mention}, you have loaned {loan_amount} from the iyesiyes bank."
                        )
                else:
                    await message.channel.send(
                        "you are not registered for gambling in this karachi casino of hamood. to register, type '-reg'"
                    )
            else:
                await message.channel.send("Enter a number for the loan amount, you troglodyte")
        except:
            pass

    elif message.content.startswith("-repay"):
        try:
            repay = int(re.sub("[^0-9]", "", message.content))
            if isinstance(repay, int):
                cur.execute("SELECT EXISTS(SELECT 1 FROM ramdev WHERE user_id=:user_id LIMIT 1)", {"user_id": user_id})
                record = cur.fetchone()
                if record[0]:
                    moni = cur.execute("select moni from ramdev where user_id =:user_id", {"user_id": user_id})
                    moni = cur.fetchone()
                    moni = moni[0]
                    loan = cur.execute("select loan from ramdev where user_id =:user_id", {"user_id": user_id})
                    loan = cur.fetchone()
                    loan = loan[0]
                    if loan <= 0:
                        await message.channel.send("you good bro")
                    else:
                        if repay > moni:
                            await message.channel.send(f"{message.author.mention}, you dont have the money dude...")
                        else:
                            if repay > loan:
                                await message.channel.send(
                                    f"{message.author.mention}, dude type '-pky' to check the money that you have loaned and only pay that amount or less."
                                )
                            else:
                                cur.execute(
                                    "update ramdev set moni = moni-:rep, loan = loan-:rep2 where user_id =:user_id",
                                    {"user_id": user_id, "rep": repay, "rep2": repay},
                                )
                                await message.channel.send(f"{message.author.mention}, {repay} pky repaid.")
                                con.commit()
                else:
                    await message.channel.send(
                        "you are not registered for gambling in this karachi casino of hamood. to register, type '-reg'"
                    )
            else:
                await message.channel.send("Enter a number for the repay amount, you troglodyte")
        except:
            pass

    elif message.content.startswith("-pky"):
        cur.execute("SELECT EXISTS(SELECT 1 FROM ramdev WHERE user_id=:user_id LIMIT 1)", {"user_id": user_id})

        record = cur.fetchone()

        if record[0]:

            moni = cur.execute("select moni from ramdev where user_id =:user_id", {"user_id": user_id})
            moni = cur.fetchone()
            loan = cur.execute("select loan from ramdev where user_id =:user_id", {"user_id": user_id})
            loan = cur.fetchone()

            await message.channel.send(
                f"{message.author.mention}, you have {moni[0]} pakistani yen(the greatest currency of all time allah hu akbar). (and you owe {loan[0]} to iyesiyes bank (protip: dont commit fraud))"
            )
        else:
            await message.channel.send(
                "you are not registered for gambling in this karachi casino of hamood. to register, type '-reg'"
            )


client.run(os.getenv("token"))
