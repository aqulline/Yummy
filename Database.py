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
    week_day = ""
    day = ""
    orders = "0"

    def __init__(self):
        self.day_calc()

    def day_calc(self):
        date1 = datetime.datetime.now()
        date2 = datetime.datetime(day=1, month=7, year=2021)

        today = str(datetime.date.today())
        y, mon, day = today.strip().split("-")
        DAYNAMES = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        name = DAYNAMES[datetime.date(int(y), int(mon), int(day)).weekday()]
        timedelta = date2 - date1
        print(timedelta)
        day1, time = str(timedelta).split(",")
        num, wrd = str(day1).split(" ")
        new = wrd + "_" + num
        print(new, name)
        self.week_day = str(name)
        self.day = str(new)

    def get_date(self):
        return str(datetime.datetime.now()).split(" ")[0]

    def get_order(self):
        if True:
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
            try:
                ref = db.reference("Yummy").child("stat").child(self.day).child("orders")
                self.orders = str(ref.get())
                self.orders = str(int(self.orders) + 1)
            except:
                ref = db.reference('Yummy').child("stat").child(self.day)
                ref.set({
                    "week_day": self.week_day,
                    "orders": self.orders
                })
                self.orders = "0"

    def upload_data(self, phone, location, quantity, amount, product_name):
        # from connection_status import connect
        self.get_order()
        if True:
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
            ref = db.reference('Yummy').child("stat").child(self.day)
            ref.set({
                "week_day": self.week_day,
                "orders": self.orders
            })

        return True

    def Signing_in_admin(self, phone, password):
        # from connection_status import connect
        if True:
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
