import discord 
import openai
from openai import OpenAI
import os
import argparse
import sys
import discord
import time
import os
import time
from discord.ext import commands, tasks
import openai
from openai import OpenAI
from datetime import datetime, timedelta
import logging
from nltk.tokenize import word_tokenize
from datetime import datetime
from discord import Option
from discord import Embed
from discord import AutoShardedBot
from discord import commands
import discord
import time
import os
import time
from discord.ext import commands, tasks
import openai
from openai import OpenAI
from datetime import datetime, timedelta
import logging
from nltk.tokenize import word_tokenize
from datetime import datetime
from discord import Option
from discord import Embed
import argparse
import json
import asyncio
import pyotp
import re
import create


parser = argparse.ArgumentParser()
parser.add_argument("--shard-id", type=int, required=True)
parser.add_argument("--shard-count", type=int, required=True)
args = parser.parse_args()


client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
assistant = client.beta.assistants.retrieve(assistant_id='asst_yTdEoEPANInWV6VxNKGVpiJY')
parser = argparse.ArgumentParser()
parser.add_argument("--shard-id", type=int, required=True)
parser.add_argument("--shard-count", type=int, required=True)
args = parser.parse_args()

bot = commands.AutoShardedBot(
    shard_id=args.shard_id,
    shard_count=args.shard_count,
    command_prefix="!",
    intents=discord.Intents.all()
)


@bot.check
async def isAdmin(ctx):
    if ctx.author.id == 73759038950617914:
        return True
    
    else :
        return False

@bot.check
async def isServer(ctx):
    if ctx.guild.id == 194512507616903328 :
        return True
    else : 
        ctx.respond("사용 제한됨")
        return False


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name} ({bot.user.id})")
    print("Syncing commands...")
        
    try:
        await bot.sync_commands()
        print("Commands synced.")

    except Exception as e:
        print(f"Failed to sync commands: {e}")

# @bot.slash_command(name = "info_load", description = "load user info")
# async def serverid(ctx, user_id :str):
#     user = await bot.fetch_user(user_id)
#     await ctx.respond(user)


@bot.slash_command(name="post_self", description = "post by self")
async def create_embed(ctx, title: str, content: str):
    # 업로드 시간 생성
    upload_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    author = ctx.author  # 명령어를 실행한 사용자

    # 임베드 생성
    embed = discord.Embed(
        title=title,
        description=content,
        color=discord.Color.blue(),  # 색상 설정
        timestamp=datetime.now()  # 임베드 하단에 타임스탬프 추가
    )

    # 필드 추가
    embed.add_field(name="업로드 시간", value=upload_time, inline=False)
    embed.add_field(name="올린 사람", value=author.mention, inline=False)

    # 메시지 전송
    await ctx.send(embed=embed)



# 버튼 View 클래스
class ConfirmView(discord.ui.View):
    def __init__(self, ctx, embed):
        super().__init__(timeout=60)  # 버튼 활성화 시간 설정
        self.ctx = ctx
        self.embed = embed
        self.result = None

    @discord.ui.button(label="Yes", style=discord.ButtonStyle.green)
    async def confirm(self, button: discord.ui.Button, interaction: discord.Interaction):
        if interaction.user != self.ctx.author:
            await interaction.response.send_message("이 명령어를 실행한 사용자만 응답할 수 있습니다.", ephemeral=True)
            return
        
        self.result = True
        await interaction.response.send_message("내용이 승인되었습니다! 임베드를 게시합니다.", ephemeral=True)
        await self.ctx.channel.send(embed=self.embed)
        self.stop()

    @discord.ui.button(label="No", style=discord.ButtonStyle.red)
    async def cancel(self, button: discord.ui.Button, interaction: discord.Interaction):
        if interaction.user != self.ctx.author:
            await interaction.response.send_message("이 명령어를 실행한 사용자만 응답할 수 있습니다.", ephemeral=True)
            return
        
        self.result = False
        await interaction.response.send_message("내용이 거부되었습니다. 임베드를 폐기합니다.", ephemeral=True)
        self.stop()


@bot.slash_command(name="post_gpts", description="post by bot")
async def create_embed(ctx, _content: str):
    upload_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    author = ctx.author  # 명령어를 실행한 사용자

    # OpenAI 응답 (예제 함수로 가정)
    ret = create.respond_message_to_openai(_content, client)
    print(ret)
    title, content = ret.split("`split`")

    # 임베드 생성
    embed = discord.Embed(
        title=title,
        description=content,
        color=discord.Color.blue(),
        timestamp=datetime.now()
    )
    embed.add_field(name="업로드 시간", value=upload_time, inline=False)
    embed.add_field(name="올린 사람", value=author.mention, inline=False)

    # 버튼 View 생성
    view = ConfirmView(ctx, embed)
    await ctx.respond(f"제목 : {title}\n내용 : {content}\n내용을 수락하시겠어요?", view=view,ephemeral=True)


bot.run(os.environ.get("DISCORD_BOT_MPSB"))