import datetime


# from main import number_of_app

def get_date():
    return str(datetime.datetime.now()).split(" ")[0]


class Upload_image:
    # Init firebase with your credentials

    name_admin = ""
    number = 0
    current_time = str(datetime.datetime.now())
    date, time = current_time.strip().split()

    def get_date(self):
        return str(datetime.datetime.now()).split(" ")[0]

    def upload_data(self, phone, location, quantity, amount, product_name):
        from connection_status import connect
        if connect():
            from test import number_app
            from firebase_admin import credentials, initialize_app, db
            cred = credentials.Certificate("farmzon-abdcb-c4c57249e43b.json")
            if number_app.time == 0:
                default_app = initialize_app(cred, {'databaseURL': 'https://farmzon-abdcb.firebaseio.com/'},
                                             name="default" + str(self.number))
                print(default_app.name)
                number_app.time += 1
            else:
                default_app = initialize_app(cred, {'databaseURL': 'https://farmzon-abdcb.firebaseio.com/'},
                                             name="default" + str(number_app.time))
                print(default_app.name)
                number_app.time += 1
            self.current_time = str(datetime.datetime.now())
            self.date, self.time = self.current_time.strip().split()
            ref = db.reference('Yummy').child("Orders").child(phone)
            ref.set({
                "Phone number": phone,
                "location": location,
                "quantity": quantity,
                "amount": amount,
                "product name": product_name,
                "time": self.time,
                "date": self.date
            })

        return True

    def Signing_in_admin(self, phone, password):
        from connection_status import connect
        if connect():
            from test import number_app
            from firebase_admin import credentials, initialize_app, db
            cred = credentials.Certificate("farmzon-abdcb-c4c57249e43b.json")
            if number_app.time == 0:
                default_app = initialize_app(cred, {'databaseURL': 'https://farmzon-abdcb.firebaseio.com/'},
                                             name="default" + str(number_app.time))
                print(default_app.name)
                number_app.time += 1
            else:
                default_app = initialize_app(cred, {'databaseURL': 'https://farmzon-abdcb.firebaseio.com/'},
                                             name="default" + str(number_app.time))
                print(default_app.name)
                number_app.time += 1
            admins = db.reference("Yummy").child("Admin")
            admin = admins.get()
            if phone in admin.keys():
                print("ok")
                password_collector = db.reference("Yummy").child("Admin").child(phone).child("password")
                if password == password_collector.get():
                    print(password)
                    # take name
                    name_collector = db.reference("Yummy").child("Admin").child(phone).child("name")
                    Upload_image.name_admin = name_collector.get()

                    return True
                else:
                    return False
            else:
                print("not ok")
                return False
