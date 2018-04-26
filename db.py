from pymongo import MongoClient
from pprint import pprint
from hashlib import sha512

Client = MongoClient(port=27017)
db = Client.Users_eMalli

def add_user(username , password):
	if (get_Id(username,password)==None):
		db.Users.insert_one({
			"username" 		    : 	username,
			"Id" 			    : 	sha512(str(username+password).encode('utf-8')).hexdigest(),
			"Humidity" 		    : 	 0,
			"Soil_Moisture"     : 	 0,
			"Temprature" 	    :  	 0,
			"Water_Level" 	    : 	 0,
			"Subscription_info" :    {}
		})

def get_Id(username , password):
	cursor = db["Users"].find({
			"Id" : sha512(str(username+password).encode('utf-8')).hexdigest()
		})
	if (cursor.count()==0):
		return None
	else:
		return cursor[0]["Id"]

def print_db():
	cursor = db["Users"].find({})
	for dc in cursor:
		pprint(dc)

def get_user_data(Id):
	cursor = db["Users"].find({'Id' : Id})
	if cursor.count()==0:
		return None
	else:
		return cursor[0]

def update_user_data(data):
	print("Updating")
	db.Users.update_one(
		{
			"Id" : data["Id"]
		},
		{
			"$set" : {
				"Humidity"      :  data["Humidity"],
				"Soil_Moisture" :  data["Soil_Moisture"],
				"Temprature"    :  data["Temprature"],
				"Water_Level"   :  data["Water_Level"]
			}
		},
	)

def subscribe_user(Id,Subscription_info):
	db.Users.update_one(
		{
			"Id" : Id
		},
		{
			"$set" : {
				"Subscription_info" : Subscription_info
			}
		}
	)

if __name__ == "__main__":
	# db['Users'].remove({})
	add_user("admin" , "admin")
	add_user("rishi" , "rishi")
	add_user("fahad" , "fahad")
	add_user("Harsh" , "Harsh")
	print_db()