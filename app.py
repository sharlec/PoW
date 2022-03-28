from flask import Flask,render_template,url_for,redirect,request,session

app = Flask(__name__)

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/demo', methods=['GET', 'POST'])
@app.route('/demo/input', methods=['GET', 'POST'])
def demo():
    if request.method == 'POST':
        text = request.form['text']
        return redirect(url_for("outcome", text=text))
    return render_template('input.html')

@app.route('/demo/outcome/<text>/')
def outcome(text):
    return render_template('outcome.j2')

