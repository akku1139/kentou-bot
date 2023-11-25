## Keep Alive
# https://qiita.com/Pumila/items/449d9f4d484b78e95479
from fastapi import FastAPI
import uvicorn
from replit import db
from threading import Thread
from misc import get_kentou_speed
import koizumi

app = FastAPI()

# Uptime Robotのため
@app.head("/")
@app.get("/")
async def root():
  return {"message": "検討Bot"}

@app.get("/cmd/")
async def cmd():
  return "Discordと同じコマンドを使える。"

@app.get("/cmd/kentou_speed")
def cmd_kentou_speed():
  return f'現在、秒速{int(get_kentou_speed())}mで検討が進んでいます。'

@app.get("/cmd/servers_count")
async def cmd_servers_count():
  # return f'現在、{len(client.guilds)}個のサーバーで検討が進んでいます。'
  return "現在このコマンドはWeb版では利用できません"

@app.get("/cmd/version")
async def cmd_version():
  # return f'➤検討Bot バージョン {VERSION}'
  return "現在このコマンドはWeb版では利用できません"

@app.get("/cmd/koizumi")
async def cmd_koizumi():
  return f'{koizumi.rand()}'

def run():
  uvicorn.run(app, host='0.0.0.0', port=8080)

ka = Thread(target=run)
ka.start()
