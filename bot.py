import discord
import asyncio
import os


TOKEN = os.environ.get("DISCORD_TOKEN")
client = discord.Client()
category_missed_id = 677069135946973204
category_successed_id = 677069170260574219

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author.bot:
        return

    if message.content == '/am-apply':
        member = message.author
        role = discord.utils.find(lambda r: r.name == 'makingapply', member.guild.roles)
        await member.add_roles(role)
        category_qa = client.get_channel(676613443809181716)  
        channel_name = f'{str(member)}さんの申請受付。'
        payload = {'name': channel_name, 'category': category_qa, 'position': 0}
        channel_qa = await message.guild.create_text_channel(**payload)
        await message.channel.send(f'{member.mention}さん用運営申請チャンネルを作成しました。{channel_qa.mention}')
        embed = discord.Embed(title="PlzSelect",description = f'申請したいランクに沿ったリアクションを押して下さい。\n:a:Admin\n:b:Assistant',color=discord.Colour.from_rgb(0, 255, 255))
        await channel_qa.send(f'For {member.mention}')
        send_msg = await channel_qa.send(embed=embed)
        await send_msg.add_reaction('🅰')
        await send_msg.add_reaction('🅱')
        
    def react_check(reaction,user):
        emoji = str(reaction.emoji)
        if reaction.message.id != send_msg.id:
            return 0
        if user.bot:
            return 0
        else:
            return emoji,user

    while not client.is_closed():
        try:
            reaction,user = await client.wait_for('reaction_add',check=react_check,timeout=7200.0)
        except asyncio.TimeoutError:
            await message.channel_qa.send('時間切れ')
            return
        else:
            emoji = str(reaction.emoji)
            if emoji == "🅰":
                applyrole = discord.utils.find(lambda r: r.name == 'Admin',member.guild.roles)
            if emoji == "🅱":
                applyrole = discord.utils.find(lambda r: r.name == 'Assistant',member.guild.roles)
            embed = discord.Embed(title="PlzWrite",description = f'申請ランクは{str(applyrole.mention)}\n次に運営としてやりたいことを１メッセージで入力してください。',color=discord.Colour.from_rgb(0, 255, 255))
            send_msg = await channel_qa.send(embed=embed)

            def check(msg):
                if message.author != msg.author:
                    return 0
                else:
                    return 1
            while not client.is_closed():
                try:
                    msg = await client.wait_for('message',check=check,timeout=7200.0)
                except asyncio.TimeoutError:
                    await message.channel_qa.send('時間切れ')
                    return
                else:
                    reason = msg.content
                    embed = discord.Embed(title="FinalCheck",description = f'以上の内容で申請確定してもよろしいですか？',color=discord.Colour.from_rgb(0, 255, 255))
                    send_msg = await channel_qa.send(embed=embed)
                    await send_msg.add_reaction('✅')
                    await send_msg.add_reaction('❎')
                    while not client.is_closed():
                        try:
                            reaction,user = await client.wait_for('reaction_add',check=react_check,timeout=7200.0)
                        except asyncio.TimeoutError:
                            await message.channel_qa.send('時間切れ')
                            return
                        else:
                            emoji = str(reaction.emoji)
                            if emoji == "✅":
                                await channel_qa.send(f'申請が完了しました。人事権を持つ運営の返答をお待ちください。')
                                await channel_qa.purge()
                                humanresource = discord.utils.find(lambda r: r.name == '人事課',member.guild.roles)
                                await channel_qa.send(f'For {humanresource.mention}')
                                embed = discord.Embed(title="ApplyComplete",description = f'志望者→{member.mention}\n希望役職→{applyrole.mention}\n志望動機→{reason}',color=discord.Colour.from_rgb(0, 255, 255))
                                send_msg = await channel_qa.send(embed=embed)
                                role = discord.utils.find(lambda r: r.name == 'makingapply', member.guild.roles)
                                await member.remove_roles(role)
                                role = discord.utils.find(lambda r: r.name == 'applying', member.guild.roles)
                                await member.add_roles(role)
                                await channel_qa.edit(category = channel_qa.guild.get_channel(category_successed_id))
                                return
                            
                            if emoji == "❎":
                                await channel_qa.purge()
                                embed = discord.Embed(title="ApplyComplete",description = f'志望者→{member}\n希望役職→{applyrole.mention}\n志望動機→{reason}',color=discord.Colour.from_rgb(0, 255, 255))
                                send_msg = await channel_qa.send(embed=embed)
                                humanresource = discord.utils.find(lambda r: r.name == '人事課',member.guild.roles)
                                await channel_qa.send(f'{member.mention}さん再度申請をする場合は申請を作り直してください。{humanresource.mention}')
                                await channel_qa.edit(category = channel_qa.guild.get_channel(category_missed_id))
                                role = discord.utils.find(lambda r: r.name == 'makingapply', member.guild.roles)
                                await member.remove_roles(role)
                                return

client.run(TOKEN)
