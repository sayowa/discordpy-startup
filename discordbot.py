import discord
from discord.ext import commands
import os
import asyncio

client = commands.Bot(command_prefix='/')
token = os.environ['DISCORD_BOT_TOKEN']

@client.event
async def on_message(message):
    if message.content == 'pthelp':
    await message.channel.send('【募集名】・【募集人数】・【募集リミット（分）】になってるｿﾞ！\n『・』は、半角スペースで頼むｿﾞ\n募集名以降は記載しない場合、デフォで人数は4人、リミットは30分ｿﾞ')

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    
@client.command()
async def pt(ctx, about = "募集", cnt = 4, settime = 30.0):
    cnt, settime = int(cnt), float(settime*60)
    reaction_member = ["参加者一覧"]
    test = discord.Embed(title=about,colour=0x1e90ff)
    test.add_field(name=f"あと{cnt}人 募集中\n", value='\n'.join(reaction_member), inline=True)
    msg = await ctx.send(embed=test)
    #投票の欄
    await msg.add_reaction('⏫')
    await msg.add_reaction('⏬')
    
    def check(reaction, user):
        emoji = str(reaction.emoji)
        if user.bot == True:    # botは無視
            pass
        else:
            return emoji == '⏫' or emoji == '⏬'
        
    while 0 <= cnt:
        try:
            reaction, user = await client.wait_for('reaction_add', timeout=settime, check=check)
        except asyncio.TimeoutError:
            await ctx.send('募集時間が過ぎたｿﾞ、再度、募集ｵﾅｼｬｽ!')
            break
        else:
            print(str(reaction.emoji))
            if str(reaction.emoji) == '⏫':
                #if user.name in reaction_member:
                    #await msg.remove_reaction(str(reaction.emoji), user)
                    #continue
                reaction_member.append(user.name)
                cnt -= 1
                test = discord.Embed(title=about,colour=0x1e90ff)
                test.add_field(name=f"あと__{cnt}__人 募集中\n", value='\n'.join(reaction_member), inline=True)
                await msg.edit(embed=test)
                
                if cnt == 0:
                    test = discord.Embed(title=about,colour=0x1e90ff)
                    test.add_field(name=f"あと__{cnt}__人 募集中\n", value='\n'.join(reaction_member), inline=True)
                    await msg.edit(embed=test)
                    finish = discord.Embed(title=about,colour=0x1e90ff)
                    finish.add_field(name="メンバーがきまったようｿﾞ\n復活の魂わすれるなよ！", value='\n'.join(reaction_member),inline=True)
                    await ctx.send(embed=finish)
                    
            elif str(reaction.emoji) == '⏬':
                if user.name in reaction_member:
                    reaction_member.remove(user.name)
                    cnt += 1
                    test = discord.Embed(title=about,colour=0x1e90ff)
                    test.add_field(name=f"あと__{cnt}__人 募集中\n", value='\n'.join(reaction_member), inline=True)
                    await msg.edit(embed=test)
                else:
                    pass
        # リアクション消す。メッセージ管理権限がないとForbidden:エラーが出ます。
        await msg.remove_reaction(str(reaction.emoji), user)
        
        
client.run(token)
