from flask import render_template , Flask , flash , request , session , redirect , abort, Response
from db import add_user , get_Id , get_user_data , update_user_data, subscribe_user
from os import urandom
from push import push
from pprint import pprint

app = Flask(__name__)

@app.route('/')
def home():
	if session.get('Id') == None:
		return render_template('login.html')
	else :
		return redirect("/home")

@app.route('/login' , methods=['POST'])
def login():
	user = request.form['uname']
	pswd = request.form['psw']
	Id = get_Id(user , pswd)

	if Id == None:
		flash("Wrong Username or password")
		return home()
	else:
		session['Id'] = Id
		return redirect("/home")

@app.route('/home')
def dashboard():
	Id = session.get('Id')
	if Id == None:
		return redirect('/')
	data = get_user_data(Id)
	return render_template('home.html' , name=data['username'] , temprature=data['Temprature'] , Water=data['Water_Level'] , SM=data['Soil_Moisture'] , HM=data['Humidity'])

@app.route('/note')
def sched():
	Id = session.get('Id')
	if Id == None:
		return redirect('/')
	data = get_user_data(Id)
	return render_template('note.html' , name=data['username'])

@app.route('/update' , methods=['POST'])
def update():
	print(request.headers)
	print(type(request.get_json()))
	data = request.form
	update_user_data(request.get_json())
	return "Done"

@app.route('/subscribe' , methods=['POST'])
def subscribe():
	if session.get('Id')!=None:
		subi = request.get_json("Subscription_Token")
		print("Subscribed!!!!")
		subscribe_user(session['Id'] , subi)
		return Response(status=201 , mimetype='application/json')

@app.route('/push' , methods=['POST'])
def notify():
	Id = request.get_json()['Id']
	if Id != None:
		push(get_user_data(Id)["Subscription_info"])
	return Response(status=200)

@app.route('/clear-session')
def clrsession():
	session.clear()
	return redirect("/")

if __name__ == "__main__":
	app.secret_key = urandom(12)
	app.run(host="0.0.0.0",debug=True , port=8080)