import pyrebase
config = {
"apiKey": "AIzaSyDFHJnPVHFCyGnYf1dZN7_gAPBs2kUBeV4",
  "authDomain": "numberplate-54561.firebaseapp.com",
  "projectId": "numberplate-54561",
"databaseURL":"https://numberplate-54561-default-rtdb.firebaseio.com/",
  "storageBucket": "numberplate-54561.appspot.com",
  "messagingSenderId": "23839421685",
  "appId": "1:23839421685:web:ee0134c317fafb579e41bc",
  "measurementId": "G-9R212SE5M7"
}

firebase = pyrebase.initialize_app(config)
database = firebase.database()


data = {"LicensePlateNumber":"MH20DY2366","TimeStamp":"5-11-2022::9:51","Fine":500}

#create data
#database.push(data)

#database.child("users").child("FirstPerson").set(data)

#read data

FirstPerson = database.child("users").child("FirstPerson").get()
print(FirstPerson.val())
#list_of_items = list(FirstPerson.item())
#print(list_of_items)

#for person in FirstPerson:
    #print(person.item())

    
#listtype=list(FirstPerson.items())
#print(listtype)
#print(FirstPerson.items())
