from flask import Flask, render_template
app = Flask(__name__)


@app.route('/')
def homes():
    return render_template('home.html')

@app.route('/sobre nós')
def sobre():
    return render_template('sobre.html')

@app.route('/carros')
def carros():
    return render_template('carros.html')


app.run(debug=True)