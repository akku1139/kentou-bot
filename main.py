# 検討Bot
VERSION = "0.4.1"

import discord
from discord import app_commands
import random
import web_master
from misc import get_kentou_speed, key_test_and_create
from in_list import in_list
from out_list import out_list_cache_keys, out_list_cache_values
import koizumi
from replit import db
import os

TOKEN = os.getenv("DISCORD_TOKEN")
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@client.event
async def on_message(message):
  # 送信者がbotである場合は99.95%弾く
  if message.author.bot and random.random() < 0.995:
    return
  m = message.content
  debug = False
  debug_msg = ""
  if "debug_k_bot" in m:
    debug = True

  # 加速度の調節
  # DMを弾く
  bias = 1
  if message.guild:
    if message.channel.name == "スーパー検討":
      bias = 5

  # 抽選。
  # キーワードがなくても0.1%で検討する。
  probability = 0.1
  debug_prob = [{"all": 0.1}]
  for s in in_list:
    if s in m:
      probability += in_list[s]
      debug_prob.append({s: in_list[s]})
  rand = random.random() * 100

  if (rand) < probability:
    # 画像を貼るための抽選を行う
    await message.reply(random.choices(out_list_cache_keys, weights=out_list_cache_values)[0])

  if "増税メガネ" in m:
    await message.reply("はい、あの色々な呼び方はあるものだなと思っております。")

  if debug:
    debug_msg=(f'Debug info.\n'
    f'確率リスト: {str(debug_prob)}\n'
    f'合計確率: {probability}%\n'
    f'ランダム値: {rand}\n'
    f'加速度バイアス: {bias}\n'
    f'加速度合計: {probability * bias}')
    await message.reply(debug_msg)

  # 事後処理
  s = get_kentou_speed()
  s += probability * bias
  db["kentou_speed"] = s
  
  # 光速を超えて検討を行う
  if s > 299792458:
    await message.reply("# 検討速度が光速(299'792'458 m/s)を超えました。\n"
                        "爆発します。")

  return

# コマンド
@tree.command(name="kentou_speed", description="現在の検討速度を表示")
async def cmd_kentou_speed(interaction: discord.Interaction):
  await interaction.response.send_message(f'現在、秒速{int(get_kentou_speed())}mで検討が進んでいます。')

@tree.command(name="servers_count", description="現在参加しているサーバーの数")
async def cmd_servers_count(interaction: discord.Interaction):
  await interaction.response.send_message(f'現在、{len(client.guilds)}個のサーバーで検討が進んでいます。')

@tree.command(name="version", description="Botのバージョン")
async def cmd_version(interaction: discord.Interaction):
  await interaction.response.send_message(f'➤検討Bot バージョン {VERSION}')

@tree.command(name="koizumi", description="某小泉氏の名言をランダムに表示します")
async def cmd_koizumi(interaction: discord.Interaction):
  await interaction.response.send_message(f'{koizumi.rand()}')

# 起動に関する部分
cmd_ver = 4
@client.event
async def on_ready():
  # 無駄に同期しすぎないため
  if int(db["cmd_version"]) != cmd_ver :
    await tree.sync()
    db["cmd_version"] = cmd_ver
    print("コマンドを同期します。")

key_test_and_create("kentou_speed")
key_test_and_create("cmd_version")

try:
  client.run(str(TOKEN))
except:
  os.system("kill 1")
