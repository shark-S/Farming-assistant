from flask import Flask, render_template, request, redirect, url_for, abort, session, send_file

app = Flask(__name__)
app.config['SECRET_KEY'] = 'F34TF$($e34D';

@app.route('/')
def home():
	return send_file('index.html')

@app.route('/getAnswer', methods=['POST'])
def dislayResult():
    state = request.form['state']
    district = request.form['district']
    season = request.form['season']
    return render_template('result.html', state=state, district=district, season=season)

if __name__ == '__main__':
    app.run()