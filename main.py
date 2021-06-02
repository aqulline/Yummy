import os
import time

from kivy.properties import NumericProperty, ObjectProperty, StringProperty, BooleanProperty
from kivy.uix.floatlayout import FloatLayout
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.uix.image import AsyncImage
from kivy.base import EventLoop

import phonenumbers
import datetime
import re
import threading

from kivymd.uix.behaviors import CircularRippleBehavior
from kivymd.uix.card import MDCard, MDSeparator
from kivymd.uix.label import MDLabel

from Database import Upload_Data as DB

from kivymd.toast import toast
from kivy.clock import Clock
from kivymd.uix.boxlayout import MDBoxLayout
from phonenumbers import carrier
from phonenumbers.phonenumberutil import number_type
from kivymd.uix.button import MDFlatButton, MDRaisedButton, MDIconButton, MDTextButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import OneLineListItem
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.textfield import MDTextField, MDTextFieldRound, MDTextFieldRect
from plyer import notification, utils

# keyboard monitor and sensor
Window.keyboard_anim_args = {"d": .2, "t": "linear"}
Window.softinput_mode = "below_target"

if utils.platform == 'win':
    from kivy import Config

    Config.set('graphics', 'multisamples', '0')

    os.environ['KIVY_GL_BACKEND'] = 'angle_sdl2'


class Cool(CircularRippleBehavior, AsyncImage):
    def __init__(self, **kwargs):
        self.ripple_scale = 0.85
        super().__init__(**kwargs)


class category(MDCard):
    pass


class Front_shop(MDCard):
    pass


class Shops(MDCard):
    pass


class category_gal(MDCard):
    pass


class category_ga(AsyncImage):
    pass


class Labels(MDLabel):
    pass


class phone_dialog(MDDialog):
    pass


class Shop_image(AsyncImage):
    pass


class Item(OneLineListItem):
    divider = None


class last_dialog(MDBoxLayout):
    pass


class NumberOnlyField(MDTextField):
    pat = re.compile('[^0-9]')

    def insert_text(self, substring, from_undo=False):

        pat = self.pat

        if "." in self.text:
            s = re.sub(pat, "", substring)

        else:
            s = ".".join([re.sub(pat, "", s) for s in substring.split(".", 1)])

        return super(NumberOnlyField, self).insert_text(s, from_undo=from_undo)


class NumberOnly(MDTextFieldRect):
    pat = re.compile('[^0-9]')

    def insert_text(self, substring, from_undo=False):

        pat = self.pat

        if "." in self.text:
            s = re.sub(pat, "", substring)

        else:
            s = ".".join([re.sub(pat, "", s) for s in substring.split(".", 1)])

        return super(NumberOnly, self).insert_text(s, from_undo=from_undo)


class NumberOnlyRound(MDTextFieldRound):
    pat = re.compile('[^0-9]')

    def insert_text(self, substring, from_undo=False):
        pat = self.pat

        if "." in self.text:
            s = re.sub(pat, "", substring)

        else:
            s = ".".join([re.sub(pat, "", s) for s in substring.split(".", 1)])

        return super(NumberOnlyRound, self).insert_text(s, from_undo=from_undo)


class number_of_app:
    times = 0


class MainApp(MDApp):
    # APP
    storage_url = "https://farmzon-abdcb.appspot.com"
    database_url = "https://farmzon-abdcb.firebaseio.com/.json"
    data = {"uu": {"Joe Tilsed": "me"}}
    auth_key = "sBlt6fzvguYnrGl2FlXRK3k4vRxSfZJBV2P7yIRv"
    size_x = NumericProperty(0)
    size_y = NumericProperty(0)
    menu = ObjectProperty(None)
    count = NumericProperty(0)
    count_update = NumericProperty(0)
    dialog = None
    dialog_phone = None
    dialog_last = None
    setter = None
    counter_image = NumericProperty(0)
    spin_active = BooleanProperty(False)
    menu_text = StringProperty("Your Location")
    loading = StringProperty("")

    # Business
    product_name = StringProperty("")
    phone_number = StringProperty("")
    location = StringProperty("")
    quantity = StringProperty("")
    total_amount = NumericProperty(0)
    order_number = StringProperty("0")
    category_tp = StringProperty("")

    # MATH
    calculator = StringProperty("0")
    calculator2 = StringProperty("0")

    # XXX-------ADMIN LOGIN VAR-------XXX
    admin_name = StringProperty("")
    admin_phone = StringProperty("")
    admin_password = StringProperty("")
    admin_true = BooleanProperty(False)
    admin_product_image = StringProperty("images/picture.png")
    admin_product_name = StringProperty("")
    admin_product_price = StringProperty("")
    admin_product_id = StringProperty("")
    admin_product_url = StringProperty("")

    # DATABASE

    def stream_handler(self, message):
        print(message.data)
        print(utils.platform)
        if True:
            print("hello")

            return notification.notify(title='New order', message='you have new order!')

    def notifi(self, phone):
        try:
            import firebase_admin
            firebase_admin._apps.clear()
            from firebase_admin import credentials, initialize_app, db
            id = datetime.datetime.now()
            cred = credentials.Certificate("credential/farmzon-abdcb-c4c57249e43b.json")
            initialize_app(cred, {'databaseURL': 'https://farmzon-abdcb.firebaseio.com/'}, name=str(id))

            my_stream = db.reference("Yummy").child("Admin").child(phone).child("Orders").listen(self.stream_handler)
        except:
            print("poor me")

    def remember_me_admin(self, user, password, name):
        with open("admin.txt", "w") as fl:
            fl.write(user + "\n")
            fl.write(password)
        with open("admin_info.txt", "w") as ui:
            ui.write(name)
        fl.close()
        ui.close()

    def admin_memory(self):
        file_size = os.path.getsize("credential/admin.txt")
        if file_size == 0:
            sm = self.root
            sm.current = "login"
        else:
            sm = self.root
            self.admin_true = True
            file1 = open('credential/admin.txt', 'r')
            file2 = open("credential/admin_info.txt")
            Lines = file1.readlines()
            Lines2 = file2.readlines()

            # Strips the newline character
            self.admin_phone = Lines[0].strip()
            self.admin_password = Lines[1].strip()
            self.admin_name = Lines2[0]
            self.Signing_in_admin(self.admin_phone, self.admin_password)
            sm.current = "admin_main"
            self.count += 1
            thread = threading.Thread(target=self.notifi, args=self.admin_phone)
            thread.start()
            kamba = threading.Thread(target=self.listen_db, args=self.admin_phone)
            kamba.start()

    def actively_reg(self):
        if self.spin_active:
            self.spin_active = False
            toast("Successfully Registered!")

    def permision_req(self):
        if utils.platform == 'android':
            from android.permissions import request_permissions, Permission  # todo
            request_permissions([Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE])

    def notifier(self):
        notification.notify(title="Welcome", message="you can also sell and buy!")

    def on_start(self):
        m = self.root
        m.current = "one"

    def menu_fun(self, identity):
        vimbweta = [
            "vimbweta vya uwanjani",
            "vimbweta vya stationary",
            "vimbweta vya girls hostel",
            "vimbweta vya boys hostel",
            "vimbweta nyuma ya ndege",
            "vimbweta vya block 16",
            "vimbweta vya adminstration"
        ]
        self.menu = MDDropdownMenu(
            caller=identity,
            width_mult=9,
            position="auto",
            callback=self.menu_callback
        )
        for i in range(vimbweta.__len__()):
            self.menu.items.append(
                {
                    "text": vimbweta[i]
                }
            )
        for i in range(22):
            if i == 0:
                pass
            else:
                self.menu.items.append(
                    {
                        "text": "Block " + "" + str(i)
                    }
                )
        self.menu.bind(
            on_release=self.menu_callback
        )

        self.setter = identity
        self.setter.set_item(self.menu_text)

    def show_alert_dialog(self):
        if not self.dialog:
            self.dialog = MDDialog(
                title="Do you real want to quit?",
                buttons=[
                    MDFlatButton(
                        text="CANCEL", text_color=self.theme_cls.primary_color, on_release=self.kill
                    ),
                    MDRaisedButton(
                        text="QUIT!", text_color=self.theme_cls.primary_color,
                        on_release=lambda x: toast("Please press the home button!", 5)
                    ),
                ],
            )
        self.dialog.open()

    def phone_number_dialog(self):
        if not self.dialog_phone:
            self.dialog_phone = phone_dialog(
                title="Enter Your phone number",
                auto_dismiss=False,
                buttons=[
                    MDFlatButton(
                        text="Cancel", text_color=self.theme_cls.primary_color, on_release=self.kill_phone
                    ),
                    MDRaisedButton(
                        text="Submit", text_color=self.theme_cls.primary_color,
                        on_release=lambda x: self.phone_number_check(self.phone_number)
                    ),
                ],
            )
        self.dialog_phone.open()

    def last_step_dialog(self):
        if not self.dialog_last:
            self.dialog_last = MDDialog(
                title="Confirm",
                type="custom",
                content_cls=last_dialog(),
                buttons=[
                    MDFlatButton(
                        text="Cancel",
                        text_color=self.theme_cls.primary_color,
                        on_release=self.kill_phone
                    ),
                    MDRaisedButton(
                        text="Submit",
                        on_release=lambda x: self.phone_number_check(self.phone_number),
                        theme_text_color="Custom",
                        md_bg_color=[243 / 255, 189 / 255, 106 / 255, 1]
                    ),

                ],
            )
        self.dialog_last.md_bg_color = 245 / 255, 0 / 255, 72 / 255, 1
        self.dialog_last.open()

    def phone_number_check(self, phone):
        new_number = ""
        for i in range(phone.__len__()):
            if i == 0:
                pass
            else:
                new_number = new_number + phone[i]
        number = "+255" + new_number
        if not carrier._is_mobile(number_type(phonenumbers.parse(number))):
            toast("Please check your phone number!", 1)
            return False
        else:
            self.phone_number = phone
            self.Business(self.product_name, self.quantity, self.phone_number)
            self.kill_phone()
            return True

    def phone_number_check_admin(self, phone):
        new_number = ""
        for i in range(phone.__len__()):
            if i == 0:
                pass
            else:
                new_number = new_number + phone[i]
        number = "+255" + new_number
        if not carrier._is_mobile(number_type(phonenumbers.parse(number))):
            toast("Please check your phone number!", 1)
            return False
        else:
            return True

    def kill(self, *kwargs):
        self.dialog.dismiss()

    def kill_phone(self, *kwargs):
        self.dialog_phone.dismiss()

    def Business(self, product, quantity, phone):
        self.last_step_dialog()
        print("location:", self.location, '\n'
                                          "Product name:", product, '\n'
                                                                    "quantity:", quantity, '\n'
                                                                                           "Total amount:",
              self.total_amount, '\n'
                                 "Phone number:", phone)
        if self.category_tp != "admin":
            thread = threading.Thread(target=DB.upload_data,
                                      args=(
                                          DB(), self.admin_phone, phone, self.location, quantity, self.total_amount,
                                          product))
            thread.start()
            thread.join()
            toast("Ordered successfully!", 10)
        else:
            thread = threading.Thread(target=DB.upload_data_admin,
                                      args=(
                                          DB(), self.admin_phone, phone, self.location, quantity, self.total_amount,
                                          product))
            thread.start()
            thread.join()
            toast("Ordered successfully!", 10)

    def keyboard_hooker(self):
        EventLoop.window.bind(on_keyboard=self.hook_keyboard)

    def hook_keyboard(self, window, key, *largs):
        sm = self.root
        if key == 27 and self.count == 1:
            Window.on_minimize()
            sm.current = "one"
            self.count = self.count - 1
            return True
        elif key == 278:
            print("yes")
            Window.on_minimize()
            return True
        elif key == 27 and self.count == 0:
            # Window.on_close()
            self.show_alert_dialog()
            return True

    def menu_callback(self, menu):
        self.menu_text = menu.text
        self.setter.set_item(menu.text)
        self.menu.dismiss()
        print(menu.text)
        self.location = menu.text

    def callculator_rim(self, mingapi, price):
        identity = self.root.ids.quantity
        self.calculator = mingapi + "0"
        if mingapi == "":
            pass
        elif mingapi == '.':
            identity.text = "1"
        else:
            self.total_amount = self.calculator = str(float(mingapi) * int(price))

    def callback(self, button):
        self.menu.caller = button
        self.menu.open()

    food_count = 0

    def order_spinner2(self):
        if self.front_shop_count == 0:
            identity = self.root.ids.drop_item_one
            self.menu_fun(identity)
            self.notifier()
            self.spin_active = True
            try:
                toast("loading please wait...", 10)
                self.loading = "Loading..."
                Clock.schedule_once(lambda x: self.front_shop(), 4)
                # thread = threading.Thread(target=self.front_shop)
                # thread.start()
            except:
                toast("no internet!")
                self.spin_active = False

    def order_spinner3(self):
        if self.other_shops == 0:
            self.spin_active = True
            try:
                toast("loading please wait...", 10)
                Clock.schedule_once(lambda x: self.other_shop(), 4)
                # thread = threading.Thread(target=self.other_shop)
                # thread.start()
            except:
                toast("no internet!")
                self.spin_active = False

    def add_order(self):
        try:
            if self.food_count == 0:
                self.food_count = self.food_count + 1
                food = self.root.ids.food_cat
                import firebase_admin
                firebase_admin._apps.clear()
                from firebase_admin import credentials, initialize_app, db
                if not firebase_admin._apps:
                    cred = credentials.Certificate("credential/farmzon-abdcb-c4c57249e43b.json")
                    initialize_app(cred, {'databaseURL': 'https://farmzon-abdcb.firebaseio.com/'})

                    store = db.reference("Yummy").child("Orders")
                    stores = store.get()

                    count = 0
                    for y, x in stores.items():
                        food_categories = category()
                        del_btn = MDIconButton(icon="delete", on_release=self.remove_widgets,
                                               pos_hint={"center_x": .9, "center_y": .3}, theme_text_color="Custom",
                                               text_color={60 / 255, 66 / 255, 75 / 255}, user_font_size="26sp")
                        count += 1
                        # food_categories.md_bg_color = 245 / 255, 0 / 255, 72 / 255, 1
                        food_categories.id = y
                        del_btn.id = y
                        food_categories.md_bg_color = 121 / 255, 174 / 255, 141 / 255, 1
                        food_categories.add_widget(Labels(text="Admin-phone:" + " " + str(x['Admin phone'])))
                        food_categories.add_widget(Labels(text="Phone:" + " " + y))
                        food_categories.add_widget(MDSeparator(height="5dp"))
                        food_categories.add_widget(Labels(text="Amount:" + " " + " " + str(x['amount'])))
                        food_categories.add_widget(Labels(text="Location:" + " " + " " + str(x['location'])))
                        food_categories.add_widget(Labels(text="Product-Name:" + " " + " " + str(x['product name'])))
                        food_categories.add_widget(Labels(text="Quantity:" + " " + " " + str(x['quantity'])))
                        food_categories.add_widget(Labels(text="Time-Ordered:" + " " + " " + str(x['time'])))
                        food_categories.add_widget(del_btn)
                        food.add_widget(food_categories)
                    self.order_number = str(count)

            else:
                pass
        except:
            toast("no internet")
            self.spin_active = False

    def add_order_admin(self):
        try:
            if self.food_count == 0:
                self.food_count = self.food_count + 1
                food = self.root.ids.food_cat
                import firebase_admin
                firebase_admin._apps.clear()
                from firebase_admin import credentials, initialize_app, db
                if not firebase_admin._apps:
                    cred = credentials.Certificate("credential/farmzon-abdcb-c4c57249e43b.json")
                    initialize_app(cred, {'databaseURL': 'https://farmzon-abdcb.firebaseio.com/'})

                    if self.admin_phone != "0788204327":
                        store = db.reference("Yummy").child("Admin").child(self.admin_phone).child("Orders")
                        stores = store.get()

                        count = 0
                        for y, x in stores.items():
                            food_categories = category()
                            del_btn = MDIconButton(icon="delete", on_release=self.remove_widgets,
                                                   pos_hint={"center_x": .9, "center_y": .3}, theme_text_color="Custom",
                                                   text_color={60 / 255, 66 / 255, 75 / 255}, user_font_size="26sp")
                            count += 1
                            # food_categories.md_bg_color = 245 / 255, 0 / 255, 72 / 255, 1
                            food_categories.id = y
                            del_btn.id = y
                            food_categories.md_bg_color = 121 / 255, 174 / 255, 141 / 255, 1
                            food_categories.add_widget(Labels(text="Admin-phone:" + " " + str(x['Admin phone'])))
                            food_categories.add_widget(Labels(text="Phone:" + " " + y))
                            food_categories.add_widget(MDSeparator(height="5dp"))
                            food_categories.add_widget(Labels(text="Amount:" + " " + " " + str(x['amount'])))
                            food_categories.add_widget(Labels(text="Location:" + " " + " " + str(x['location'])))
                            food_categories.add_widget(
                                Labels(text="Product-Name:" + " " + " " + str(x['product name'])))
                            food_categories.add_widget(Labels(text="Quantity:" + " " + " " + str(x['quantity'])))
                            food_categories.add_widget(Labels(text="Time-Ordered:" + " " + " " + str(x['time'])))
                            food_categories.add_widget(del_btn)
                            food.add_widget(food_categories)
                        self.order_number = str(count)
                    else:
                        self.add_order()

            else:
                pass
        except:
            toast("no internet")
            self.spin_active = False

    all_products = {}
    front_products = {}
    front_shop_count = 0
    other_shops = 0

    def other_shop(self):
        if True:
            try:
                if self.other_shops == 0:
                    self.other_shops = self.other_shops + 1
                    import firebase_admin
                    firebase_admin._apps.clear()
                    from firebase_admin import credentials, initialize_app, db
                    if not firebase_admin._apps:
                        shop = self.root.ids.other_shop
                        cred = credentials.Certificate("credential/farmzon-abdcb-c4c57249e43b.json")
                        initialize_app(cred, {'databaseURL': 'https://farmzon-abdcb.firebaseio.com/'})
                        store = db.reference("Yummy").child("Products")
                        stores = store.get()
                        self.all_products = stores
                        for y, x in stores.items():
                            self.admin_product_name = x["product_name"]
                            self.admin_phone = x["admin_phone"]
                            self.admin_product_url = x["image_url"]
                            self.admin_product_price = x["product_price"]

                            other_shops = Shops(on_release=self.selling_other)
                            other_shops.add_widget(Labels(text=self.admin_product_name))
                            other_shops.add_widget(Shop_image(source=self.admin_product_url))
                            other_shops.id = y
                            shop.add_widget(other_shops)
                            self.spin_active = False
            except:
                toast("no internet!")
                self.spin_active = False

    def selling_other(self, instance):
        print(instance.id)
        product = instance.id
        self.admin_phone = self.all_products[product]["admin_phone"]
        self.admin_product_url = self.all_products[product]["image_url"]
        self.admin_product_name = self.all_products[product]["product_name"]
        self.admin_product_price = self.all_products[product]["product_price"]
        sm = self.root
        sm.current = "selling"

    def summon(self):
        sm = self.root
        sm.current = "other_shops"
        if self.other_shops == 0:
            self.spin_active = True

    def front_shop(self):
        if True:
            try:
                if self.front_shop_count == 0:
                    self.front_shop_count = self.front_shop_count + 1
                    import firebase_admin
                    firebase_admin._apps.clear()
                    from firebase_admin import credentials, initialize_app, db
                    if not firebase_admin._apps:
                        shop = self.root.ids.front_shop
                        cred = credentials.Certificate("credential/farmzon-abdcb-c4c57249e43b.json")
                        initialize_app(cred, {'databaseURL': 'https://farmzon-abdcb.firebaseio.com/'})
                        store = db.reference("Yummy").child("Products_admin")
                        stores = store.get()
                        self.front_products = stores
                        for y, x in stores.items():
                            self.admin_product_name = x["product_name"]
                            self.admin_phone = x["admin_phone"]
                            self.admin_product_url = x["image_url"]
                            self.admin_product_price = x["product_price"]

                            front_shops = Front_shop(on_release=self.selling_front)
                            layout = FloatLayout()
                            layout.add_widget(Labels(text=self.admin_product_name,
                                                     pos_hint={"center_x": .5, "center_y": .2},
                                                     halign="center"))
                            layout.add_widget(Cool(source=self.admin_product_url))
                            front_shops.add_widget(layout)
                            front_shops.id = y
                            shop.add_widget(front_shops)
                            time.sleep(2)
                            self.spin_active = False
                            self.loading = ""
                    else:
                        print("fuck!")

            except:
                toast("no internet!")
                button = MDTextButton(text="Retry", pos_hint={"center_x": .5, "center_y": .5}, on_release=lambda x: self.refresh_front())
                button.id = "you"
                button.custom_color = 40/255, 123/255, 222/255, 1
                shop = self.root.ids.front_shop
                shop.add_widget(button)
                self.spin_active = False

    def selling_front(self, instance):
        print(instance.id)
        self.count = self.count + 1
        self.category_tp = "admin"
        product = instance.id
        self.admin_phone = self.front_products[product]["admin_phone"]
        self.admin_product_url = self.front_products[product]["image_url"]
        self.admin_product_name = self.front_products[product]["product_name"]
        self.admin_product_price = self.front_products[product]["product_price"]
        sm = self.root
        sm.current = "selling"

    def success(self, *kwargs):
        self.refresh()

    def refresh(self):
        parent = self.root.ids.food_cat
        all_childs = parent.children
        identity = []
        self.food_count = 0
        for child in all_childs:
            identity.append(child.id)

        self.order_number = str(identity.__len__())

        for i in identity:
            self.remove_wide(i)

        if self.admin_phone == "0788204327":
            self.add_order()
        else:
            self.add_order_admin()

    def refresh_front(self):
        parent = self.root.ids.front_shop
        all_childs = parent.children
        identity = []
        self.front_shop_count = 0
        for child in all_childs:
            identity.append(child.id)

        for i in identity:
            print(i)
            self.remove_wide_front(i)

        self.spin_active = True
        self.order_spinner2()

    def remove_wide_front(self, name):
        parent = self.root.ids.front_shop
        for child in parent.children:
            if name == child.id:
                parent.remove_widget(child)

    def remove_wide(self, name):
        parent = self.root.ids.food_cat
        for child in parent.children:
            if name == child.id:
                parent.remove_widget(child)

    def remove_widgets(self, instance):
        name = instance.id
        parent = self.root.ids.food_cat
        for child in parent.children:
            if name == child.id:
                parent.remove_widget(child)
                self.del_entity(child.id)

    def del_entity(self, name):
        import firebase_admin
        firebase_admin._apps.clear()
        from firebase_admin import credentials, initialize_app, db
        if not firebase_admin._apps:
            cred = credentials.Certificate("credential/farmzon-abdcb-c4c57249e43b.json")
            initialize_app(cred, {'databaseURL': 'https://farmzon-abdcb.firebaseio.com/'})

            if self.admin_phone == "0788204327":
                db.reference("Yummy").child("Orders").child(name).delete()
            else:
                db.reference("Yummy").child("Admin").child(self.admin_phone).child("Orders").child(name).delete()

    def validate_user(self, phone, password):
        if phone == "" and phone.Isdigit():
            toast("please enter your phone number correctly")
        elif password == "":
            toast("please enter your password")
        else:
            self.spin_active = True
            thread = threading.Thread(target=self.Signing_in_admin_function, args=(phone, password))
            thread.start()

    def Signing_in_admin(self, phone, password):
        thread = threading.Thread(target=self.Signing_in_admin_function, args=(phone, password,))
        thread.start()

    def Signing_in_admin_function(self, phone, password):
        if DB.Signing_in_admin(DB(), phone, password):
            sm = self.root
            self.admin_name = DB.name_admin
            self.remember_me_admin(phone, password, self.admin_name)
            if not self.admin_true:
                sm.current = "admin_main"
                self.listen_db(phone)

        else:
            if self.admin_true:
                toast("no internet connection")
                self.spin_active = False
            else:
                self.spin_active = False
                toast("oops! phone number or password in correct or internet connection")

    # XXX---------CUSTOMER--------------XXXXXXX

    def id_generator(self):
        not_allowed = ".-:"
        date1 = datetime.datetime.now()
        date, time = id = str(date1).split(" ")
        self.admin_product_id = date + time
        product_id = ""
        for i in range(len(self.admin_product_id)):
            if self.admin_product_id[i] not in not_allowed:
                product_id = self.admin_product_id[i] + product_id
        id = self.admin_product_id = product_id
        print(id)
        return self.admin_product_id

    def get_info(self, phone, phone_other, name, price, product_name, image_path, password, category):
        if phone != "" and self.phone_number_check_admin(phone):
            if name != "" and name.isalpha() and price != "" and password != "":
                self.admin_phone = phone
                self.admin_password = password
                self.admin_name = name
                self.admin_product_image = image_path
                self.admin_product_price = price
                self.admin_product_name = product_name
                self.admin_product_id = self.id_generator()
                cate = category
                print(phone, name, price, product_name, image_path, password, self.admin_product_id)
                try:
                    thread = threading.Thread(target=self.transporter, args=(
                        phone, phone_other, name, price, product_name, image_path, password, self.admin_product_id,
                        cate))
                    thread.start()
                except:
                    toast("no internet")
            else:
                toast("check your info well")
                self.spin_active = False

        else:
            toast("check your mobile number")
            self.spin_active = False

    def transporter(self, phone, phone_other, name, price, product_name, image_path, password, id, cate):
        thread = threading.Thread(target=DB.upload_product_image, args=(
            DB(), cate, image_path, phone, phone_other, name, price, product_name, password, id))
        thread.start()

        thread.join()

        self.actively_reg()

    def listen_db(self, phone):
        try:
            import firebase_admin
            firebase_admin._apps.clear()
            from firebase_admin import credentials, initialize_app, db
            id = datetime.datetime.now()
            cred = credentials.Certificate("credential/farmzon-abdcb-c4c57249e43b.json")
            initialize_app(cred, {'databaseURL': 'https://farmzon-abdcb.firebaseio.com/'}, name=str(id))
            print("i am listening......")
            my_stream = db.reference("Yummy").child("Admin").child(phone).child("Orders").listen(self.success)
        except:
            print("poor you")

    def Permission(self, android=None):
        if self.counter_image <= 0:
            if utils.platform == 'android':
                if self.count_update == 0:
                    from gallary import Gambler as GA
                    Clock.schedule_once(GA.user_select_image, 0)
                    self.admin_product_image = GA.path_of_picture
                    img = self.root.ids.product_image
                    img.source = GA.path_of_picture
                    self.count_update += self.count_update + 1
                else:
                    from gallary import Gambler as GA
                    self.count_update = self.count_update - 1
                    self.admin_product_image = GA.path_of_picture
                    img = self.root.ids.product_image
                    img.source = GA.path_of_picture

            else:
                self.counter_image = self.counter_image + 1
                for root, dirs, files in os.walk("/home/alpha9060/Downloads", topdown=False):
                    for file_ in files:
                        full_file_path = os.path.join(root, file_)
                        if full_file_path.endswith(('.png', '.jpg', '.jpeg')):
                            print(full_file_path)
                            image = full_file_path
                            cat_class = category_gal()
                            cat_class.add_widget(category_ga(source=image))
                            img = self.root.ids.images_added
                            img.add_widget(cat_class)
        else:
            pass

    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "DeepOrange"
        self.theme_cls.accent = "Brown"
        Window.size = (360, 640)
        self.size_x, self.size_y = Window.size
        self.title = "yummy"


if __name__ == '__main__':
    MainApp().run()
