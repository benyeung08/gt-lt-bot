from flask import Flask,render_template,redirect
from threading import Thread
app = Flask('')

@app.route('/')
def home():
   return "READY"
def run():
    app.run(host="0.0.0.0", port=8080)
def keep_alive():
    server = Thread(target=run)
    server.start()

@app.route('/invite')
def invite():
   return redirect('https://discord.com/api/oauth2/authorize?client_id=881788746222157884&permissions=8&scope=applications.commands%20bot')

@app.route('/github')
def github():
   return redirect('https://github.com/tooty-1135/discord.py-bot')