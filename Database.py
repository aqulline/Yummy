import datetime


def get_date():
    return str(datetime.datetime.now()).split(" ")[0]


class Upload_Data:
    # Init firebase with your credentials
    name_admin = ""
    number = 0
    current_time = str(datetime.datetime.now())
    date, time = current_time.strip().split()
    week_day = ""
    day = ""
    orders = "0"
    url = ""

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

    def get_order(self, category, number):
        if True:
            from test import number_app
            from firebase_admin import credentials, initialize_app, db
            cred = credentials.Certificate("credential/farmzon-abdcb-c4c57249e43b.json")
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
                if category == "customer":
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
                        self.orders = "1"
                else:
                    try:
                        ref = db.reference("Yummy").child("Admin").child(number).child("stat").child(self.day).child("orders")
                        self.orders = str(ref.get())
                        self.orders = str(int(self.orders) + 1)
                    except:
                        ref = db.reference('Yummy').child("stat").child(self.day)
                        ref.set({
                            "week_day": self.week_day,
                            "orders": self.orders
                        })
                        self.orders = "1"

    def upload_data(self, admin_phone, phone, location, quantity, amount, product_name):
        # from connection_status import connect
        self.get_order("customer", "0788204327")
        if True:
            from test import number_app
            from firebase_admin import credentials, initialize_app, db
            cred = credentials.Certificate("credential/farmzon-abdcb-c4c57249e43b.json")
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
                "Admin phone":admin_phone,
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

    def upload_data_admin(self, admin_phone, phone, location, quantity, amount, product_name):
        # from connection_status import connect
        self.get_order("admin", admin_phone)
        if True:
            import firebase_admin
            firebase_admin._apps.clear()
            from firebase_admin import credentials, initialize_app, db
            if not firebase_admin._apps:
                cred = credentials.Certificate("credential/farmzon-abdcb-c4c57249e43b.json")
                initialize_app(cred, {'databaseURL': 'https://farmzon-abdcb.firebaseio.com/'})

                self.current_time = str(datetime.datetime.now())
                self.date, self.time = self.current_time.strip().split()
                ref = db.reference('Yummy').child("Admin").child(admin_phone).child("Orders").child(phone)

                ref.set({
                    "Phone number": phone,
                    "location": location,
                    "quantity": quantity,
                    "amount": amount,
                    "product name": product_name,
                    "time": self.time,
                    "date": self.date
                })
                ref = db.reference('Yummy').child("Admin").child(admin_phone).child("stat").child(self.day)
                ref.set({
                    "week_day": self.week_day,
                    "orders": self.orders
                })
                ref = db.reference('Yummy').child("stat").child(self.day)
                ref.set({
                    "week_day": self.week_day,
                    "orders": self.orders
                })

    def upload_product_image(self, cate, path, phone, phone_other, name, price, product_name, password, id):
        print("START.....")
        if True:
            from firebase_admin import credentials, initialize_app, storage
            print("yes")
            import firebase_admin
            firebase_admin._apps.clear()
            if not firebase_admin._apps:
                print("ok good,,")
                cred = credentials.Certificate("credential/farmzon-abdcb-c4c57249e43b.json")
                default = initialize_app(cred, {'storageBucket': 'farmzon-abdcb.appspot.com'})
                print("WELDING..")
                bucket = storage.bucket()
                blob = bucket.blob("products" + "/" + cate + "/" + product_name+id)
                blob.upload_from_filename(path)
                blob.make_public()
                print("NICE...")
                Upload_Data.url = blob.public_url
                print("your file url", Upload_Data.url)
                firebase_admin.delete_app(default)
                self.register_admin(phone, phone_other, name, price, product_name, password, id, cate)

    def register_admin(self, phone, phone_other, name, price, product_name, password, product_id, cate):
        if True:
            import firebase_admin
            firebase_admin._apps.clear()
            from firebase_admin import credentials, initialize_app, db
            if not firebase_admin._apps:
                cred = credentials.Certificate("credential/farmzon-abdcb-c4c57249e43b.json")
                initialize_app(cred, {'databaseURL': 'https://farmzon-abdcb.firebaseio.com/'})
                print("Good..", int(phone))
                if cate == "customer":
                    ref = db.reference('Yummy').child("Customers").child(phone)
                    print("New Start")
                    ref.set(
                        {
                            "customer_name": name,
                            "customer_phone": phone,
                            "other_number": phone_other,
                            "customer_password": password
                        }
                    )
                    print("Done.. one")
                    ref_products = db.reference('Yummy').child("Customers").child(phone).child("products").child(product_id)
                    ref_products.set(
                        {
                            "product_name": product_name,
                            "product_price": price,
                            "image_url": Upload_Data.url
                        }
                    )
                    ref_main = db.reference('Yummy').child("Products").child(product_id)
                    ref_main.set(
                        {
                            "product_name": product_name,
                            "product_price": price,
                            "image_url": Upload_Data.url,
                            "admin_phone": phone
                        }
                    )
                else:
                    ref = db.reference('Yummy').child("Admin").child(phone)
                    print("New Start")
                    ref.set(
                        {
                            "customer_name": name,
                            "customer_phone": phone,
                            "other_number": phone_other,
                            "customer_password": password
                        }
                    )
                    print("Done.. one")
                    ref_products = db.reference('Yummy').child("Admin").child(phone).child("products").child(product_id)
                    ref_products.set(
                        {
                            "product_name": product_name,
                            "product_price": price,
                            "image_url": Upload_Data.url
                        }
                    )
                    ref_main = db.reference('Yummy').child("Products_admin").child(product_id)
                    ref_main.set(
                        {
                            "product_name": product_name,
                            "product_price": price,
                            "image_url": Upload_Data.url,
                            "admin_phone": phone
                        }
                    )

                print("Thanks!!!!")

    def Signing_in_admin(self, phone, password):
        # from connection_status import connect
        if True:
            import firebase_admin
            firebase_admin._apps.clear()
            from firebase_admin import credentials, initialize_app, db
            if not firebase_admin._apps:
                cred = credentials.Certificate("credential/farmzon-abdcb-c4c57249e43b.json")
                initialize_app(cred, {'databaseURL': 'https://farmzon-abdcb.firebaseio.com/'})

                admins = db.reference("Yummy").child("Admin")
                admin = admins.get()
                if phone in admin.keys():
                    print("ok")
                    password_collector = db.reference("Yummy").child("Admin").child(phone).child("customer_password")
                    if password == password_collector.get():
                        print(password)
                        # take name
                        name_collector = db.reference("Yummy").child("Admin").child(phone).child("customer_name")
                        Upload_Data.name_admin = name_collector.get()

                        return True
                    else:
                        return False
                else:
                    print("not ok")
                    return False


# Upload_Data.upload_product_image(Upload_Data(), "admin", "juice.png", "0788204327", "machungwa", "120", "nyanya", "juice.png", "906070", "090989790606")
# Upload_Data.register_admin(Upload_Data(), "0788204327", "machungwa", "120", "nyanya", "juice.png", "906070")
