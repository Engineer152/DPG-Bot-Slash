from flask import Flask, render_template
from threading import Thread

app = Flask('')

@app.route('/')
#def index():
#   return render_template
#('index.html')
def main():
  return '<html><head><title>DPG Bot Slash Commands.</title></head><body bgcolor="black"  link ="cyan" vlink="red">  <font color="white" size ="4"><h2>DPG Bot Slash Commands is Alive!</h2><font></body></html>'

def run():
    app.run(host="0.0.0.0", port=8080)
def keep_alive():
    server = Thread(target=run)
    server.start()
