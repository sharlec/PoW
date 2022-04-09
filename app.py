from flask import Flask,render_template,url_for,redirect,request,session
from client import buy_ticket, check_remain

app = Flask(__name__)
routes = ["K98665", "K67332", "D66775"]

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/tickets')
def tickets():
    remains = []
    for route in routes:
        remain = check_remain(route)
        remains.append(remain)
    return render_template('tickets.html', remains = remains)

@app.route('/outcome/<trainID>/')
def outcome(trainID):
    ticket = buy_ticket(trainID)
    return render_template('outcome.html', ticket = ticket)
