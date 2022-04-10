from flask import Flask,render_template,redirect
from threading import Thread
app = Flask('')

#-----------render_template------------
@app.route('/')
def home():
    return render_template("home.html", title="首頁")
def run():
    app.run(host="0.0.0.0", port=8080)
def keep_alive():
    server = Thread(target=run)
    server.start()

@app.route('/privacy-policy')
def privacypolicy():
   return render_template('privacy-policy.html', title="隱私政策")

@app.route('/commands')
def commands():
    return render_template("cmds.html", title="指令大全")

@app.route('/list')
def list():
    return render_template("list.html", title="投票大全")

@app.route('/supportw')
def supportw():
    return render_template("support.html", title="支援大全")

#-----------redirect------------
@app.route("/home")
def redirect_home():
   return redirect('/')
        
@app.route("/support")
def support():
   return redirect('https://discord.gg/F8GfF37GWh')

@app.route('/invite')
def invite():
   return redirect('https://discord.com/api/oauth2/authorize?client_id=881788746222157884&permissions=8&scope=applications.commands%20bot')

@app.route('/github')
def github():
   return redirect('https://github.com/tooty-1135/discord.py-bot')

#-----------list------------
@app.route('/topgg')
def topgg():
   return redirect('https://top.gg/bot/881788746222157884')

@app.route('/discordbotlist')
def discordbotlist():
   return redirect('https://discordbotlist.com/bots/pia8')

@app.route('/discordtw')
def discordtw():
   return redirect('https://discordservers.tw/bots/881788746222157884')