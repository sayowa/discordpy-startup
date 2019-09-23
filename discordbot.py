import discord
from discord.ext import commands
import os
import asyncio

client = commands.Bot(command_prefix='/')
token = os.environ['DISCORD_BOT_TOKEN']


@client.command()
async def pt(ctx, about = "募集", cnt = 8, settime = 3600.0):
    cnt, settime = int(cnt), float(settime)
    cntb = cnt
    reaction_member = ["下記は参加者一覧です。↑で参加表明、↓で離脱が行えます。集まらなかった場合も1時間後に募集は破棄されます。"]
    test = discord.Embed(title=about,colour=0xffffff)
    test.add_field(name=f"{cntb}人PTで残り{cnt}人募集\n", value="下記は参加者一覧です。↑で参加表明、↓で離脱が行えます。集まらなかった場合も1時間後に募集は破棄されます。", inline=True)
    msg = await ctx.send(embed=test)

    await msg.add_reaction(':arrow_up:')
    await msg.add_reaction(':arrow_down:')

    def check(reaction, user):
        emoji = str(reaction.emoji)
        if user.bot == True:
            pass
        else:
            return emoji == ':arrow_up:' or emoji == ':arrow_down:'

    while len(reaction_member)-1 <= 8:
        try:
            reaction, user = await client.wait_for('reaction_add', timeout=settime, check=check)
        except asyncio.TimeoutError:
            await ctx.send('時間になったので'+about+'は〆ます。')
            break
        else:
            print(str(reaction.emoji))
            if str(reaction.emoji) == ':arrow_up:':
                reaction_member.append(user.name)
                cnt -= 1
                test = discord.Embed(title=about,colour=0xffffff)
                test.add_field(name=f"{cntb}人PTで残り{cnt}人募集\n", value='\n'.join(reaction_member), inline=True)
                await msg.edit(embed=test)
                if cnt == 0:
                    test = discord.Embed(title=about,colour=0xffffff)
                    test.add_field(name=f"{cntb}人PTで残り{cnt}人募集\n", value='\n'.join(reaction_member), inline=True)

                    await msg.edit(embed=test)

                    await ctx.send('メンバーが集まったので'+about+'は〆ます。')
                    break

            elif str(reaction.emoji) == ':arrow_down:':
                if user.name in reaction_member:
                    reaction_member.remove(user.name)
                    cnt += 1
                    test = discord.Embed(title=about,colour=0xffffff)
                    test.add_field(name=f"{cntb}人PTで残り{cnt}人募集\n", value='\n'.join(reaction_member), inline=True)
                    await msg.edit(embed=test)
                else:
                    pass

        await msg.remove_reaction(str(reaction.emoji), user)

client.run(token)
