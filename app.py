from flask import Flask,render_template,url_for,redirect,request,session
from client import buy_ticket

app = Flask(__name__)

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/tickets')
def tickets():
    return render_template('tickets.html')

@app.route('/outcome/<trainID>/')
def outcome(trainID):
    ticket = buy_ticket(trainID)
    return render_template('outcome.html', ticket = ticket)
