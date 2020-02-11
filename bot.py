import discord
import os

TOKEN = os.environ.get("DISCORD_TOKEN")

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):    
  
#権限申請のプログラム
        if message.content.startswith('/am-apply'):
        member = message.author
        role = discord.utils.find(lambda r: r.name == 'applied', member.guild.roles)
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
        @client.event
        async def on_raw_reaction_add(payload):
            if payload.member.bot == False:
                if str(payload.emoji) == '🅰':
                    applyrole = 'Admin'
                if str(payload.emoji) == '🅱':
                    applyrole = 'Assistant'
                embed = discord.Embed(title="PlzWrite",description = f'申請ランクは{str(applyrole)}\n次に運営としてやりたいことを１メッセージで入力してください。',color=discord.Colour.from_rgb(0, 255, 255))
                send_msg = await channel_qa.send(embed=embed)
                @client.event
                async def on_message(message):
                    if message.author.bot:
                        return
                    reason = message.content
                    embed = discord.Embed(title="FinalCheck",description = f'以上の内容で申請確定してもよろしいですか？',color=discord.Colour.from_rgb(0, 255, 255))
                    send_msg = await channel_qa.send(embed=embed)
                    await send_msg.add_reaction('✅')
                    await send_msg.add_reaction('❎')
                    @client.event
                    async def on_raw_reaction_add(payload):
                        if payload.member.bot == False:
                            if str(payload.emoji) == '✅':
                                await channel_qa.send(f'申請が完了しました。人事権を持つ運営の返答をお待ちください。')
                                await message.channel.purge()
                                humanresource = discord.utils.find(lambda r: r.name == '人事課',member.guild.roles)
                                await channel_qa.send(f'For {humanresource.mention}')
                                embed = discord.Embed(title="ApplyComplete",description = f'志望者→{member}\n希望役職→{applyrole}\n志望動機→{reason}',color=discord.Colour.from_rgb(0, 255, 255))
                                send_msg = await channel_qa.send(embed=embed)
                                role = discord.utils.find(lambda r: r.name == 'applying', member.guild.roles)
                                await member.remove_roles(role)
                                return


                            if str(payload.emoji) == '❎':
                                await channel_qa.send(f'/ap-deleteで申請を削除し、再度作成してください。')
                                return

                        else:
                            pass
            else:
                pass                    
                        
client.run(TOKEN)
