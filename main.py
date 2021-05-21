import os
import datetime
from kivy.properties import NumericProperty, ObjectProperty, StringProperty, BooleanProperty
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.uix.image import AsyncImage
from kivy.base import EventLoop
from kivy.core.audio import SoundLoader

import phonenumbers
import random
import re
import threading

from kivymd.uix.card import MDCard, MDSeparator
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.label import MDLabel

from Database import Upload_image as DB

from kivymd.toast import toast
from kivy.clock import Clock
from kivymd.uix.boxlayout import MDBoxLayout
from phonenumbers import carrier
from phonenumbers.phonenumberutil import number_type
from kivymd.uix.button import MDFlatButton, MDRaisedButton, MDIconButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import OneLineListItem
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.textfield import MDTextField, MDTextFieldRound
from pusher_push_notifications import PushNotifications
from firebase_admin import credentials, initialize_app, db
from plyer import notification, utils

# keyboard monitor and sensor
Window.keyboard_anim_args = {"d": .2, "t": "linear"}
Window.softinput_mode = "below_target"

if utils.platform == 'win':
    from kivy import Config

    Config.set('graphics', 'multisamples', '0')

    os.environ['KIVY_GL_BACKEND'] = 'angle_sdl2'


class category(MDCard):
    pass


class category_gal(MDCard):
    pass


class category_ga(AsyncImage):
    pass


class Labels(MDLabel):
    pass


class phone_dialog(MDDialog):
    pass


class Item(OneLineListItem):
    divider = None


class last_dialog(MDBoxLayout):
    pass


class NumberOnly(MDTextField):
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
    dialog = None
    dialog_phone = None
    dialog_last = None
    setter = None
    counter_image = NumericProperty(0)
    spin_active = BooleanProperty(False)
    menu_text = StringProperty("Your Location")

    # Business
    product_name = StringProperty("")
    phone_number = StringProperty("")
    location = StringProperty("")
    quantity = StringProperty("")
    total_amount = NumericProperty(0)
    order_number = StringProperty("0")

    # MATH
    calculator = StringProperty("0")
    calculator2 = StringProperty("0")

    # XXX-------ADMIN LOGIN VAR-------XXX
    admin_name = StringProperty("")
    admin_phone = StringProperty("")
    admin_password = StringProperty("")
    admin_true = BooleanProperty(False)
    admin_product = StringProperty("")

    # DATABASE
    cred = credentials.Certificate("farmzon-abdcb-c4c57249e43b.json")
    if number_of_app.times == 0:
        x = random
        default_app = initialize_app(cred, {'databaseURL': 'https://farmzon-abdcb.firebaseio.com/'})
        print(default_app.name)
        number_of_app.times = 1 + number_of_app.times
    else:
        default_app = initialize_app(cred, {'databaseURL': 'https://farmzon-abdcb.firebaseio.com/'},
                                     name="default" + str(number_of_app.times))
        print(default_app.name)
        number_of_app.times += 1
    pn_client = PushNotifications(
        instance_id='4eacff80-61d8-48d7-ba72-9e7aede4119c',
        secret_key='4A9C78664B4FCC25397DD2F780028D9967F69BA4229736B49420727081646EFC',
    )

    def __init__(self, **kwargs):
        super().__init__()
        self.file_manager = MDFileManager()
        self.file_manager.exit_manager = self.exit_manager
        self.file_manager.select_path = self.select_path
        self.file_manager.preview = True
        self.file_manager.previous = True

    def play(self):
        sound = SoundLoader.load('no.wav')
        if sound:
            print("Sound found at %s" % sound.source)
            print("Sound is %.3f seconds" % sound.length)
            sound.play()

    def stream_handler(self, message):
        print(message.data)
        print(utils.platform)
        kwargs = {'title': 'New follower', 'message': 'you have new follower'}
        if True:
            print("hello")
            response = self.pn_client.publish(
                interests=["hello"],
                publish_body={
                    'apns': {
                        'apns': {
                            'alert': 'Hello',
                        },
                    },
                    'fcm': {
                        'notification': {
                            'title': 'Hello',
                            'body': 'Hello , world',
                        },
                    },
                },
            )

            return notification.notify(title='New order', message='you have new order!')

    def notifi(self):
        try:
            my_stream = db.reference("Yummy").child("Orders").listen(self.stream_handler)
        except:
            pass

    def remember_me_admin(self, user, password, name):
        with open("admin.txt", "w") as fl:
            fl.write(user + "\n")
            fl.write(password)
        with open("admin_info.txt", "w") as ui:
            ui.write(name)
        fl.close()
        ui.close()

    def admin_memory(self):
        file_size = os.path.getsize("admin.txt")
        if file_size == 0:
            sm = self.root
            sm.current = "login"
        else:
            sm = self.root
            self.admin_true = True
            file1 = open('admin.txt', 'r')
            file2 = open("admin_info.txt")
            Lines = file1.readlines()
            Lines2 = file2.readlines()

            # Strips the newline character
            self.admin_phone = Lines[0].strip()
            self.admin_password = Lines[1].strip()
            self.admin_name = Lines2[0]
            self.Signing_in_admin(self.admin_phone, self.admin_password)
            sm.current = "admin_main"
            self.count += 1
            thread = threading.Thread(target=self.notifi)
            thread.start()
            kamba = threading.Thread(target=self.listen_db)
            kamba.start()

    def permision_req(self):
        if utils.platform == 'android':
            from android.permissions import request_permissions, Permission  # todo
            request_permissions([Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE])

    def on_start(self):
        drop_one = self.root.ids.drop_item_one
        drop_two = self.root.ids.drop_item_two
        EventLoop.window.bind(on_keyboard=self.hook_keyboard)
        notification.notify(title="hi", message="me")
        self.menu_fun(drop_one)
        self.menu_fun(drop_two)
        self.permision_req()

        # cards background colors

        price = self.root.ids.price_miho
        price.md_bg_color = 245 / 255, 0 / 255, 72 / 255, 1

        price_rim = self.root.ids.price_rim
        price_rim.md_bg_color = 245 / 255, 0 / 255, 72 / 255, 1

        price_juice = self.root.ids.price_juice
        price_juice.md_bg_color = 245 / 255, 0 / 255, 72 / 255, 1

        juice = self.root.ids.juice_carry
        juice.md_bg_color = 121 / 255, 174 / 255, 141 / 255, 1

        mihogo = self.root.ids.mihogo_carry
        mihogo.md_bg_color = 60 / 255, 66 / 255, 75 / 255, 1

        logo = self.root.ids.cart
        logo.md_bg_color = 245 / 255, 0 / 255, 72 / 255, 1

        order = self.root.ids.order
        order.md_bg_color = 245 / 255, 0 / 255, 72 / 255, 1

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
        thread = threading.Thread(target=DB.upload_data,
                                  args=(DB(), phone, self.location, quantity, self.total_amount, product))
        thread.start()
        toast("Ordered successfully!", 10)

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

    def callculator(self, mingapi):
        identity = self.root.ids.mingap
        self.calculator = mingapi + "0"
        if mingapi == "":
            pass
        elif mingapi == '.':
            identity.text = "1"
        else:
            self.total_amount = self.calculator = str(float(mingapi) * 150)

    def callculator2(self, mingapi):
        self.calculator2 = mingapi + "0"
        identity = self.root.ids.mingap_juice
        if mingapi == "":
            pass
        elif mingapi == '.':
            identity.text = '1'
        else:
            self.total_amount = self.calculator2 = str(float(mingapi) * 500)

    def callculator_rim(self, mingapi):
        identity = self.root.ids.rim_mingap
        self.calculator = mingapi + "0"
        if mingapi == "":
            pass
        elif mingapi == '.':
            identity.text = "1"
        else:
            self.total_amount = self.calculator = str(float(mingapi) * 50)

    def callback(self, button):
        self.menu.caller = button
        self.menu.open()

    food_count = 0

    def order_spinner2(self):
        self.spin_active = True

    def add_order(self):
        try:
            if self.food_count == 0:
                self.food_count = self.food_count + 1
                food = self.root.ids.food_cat
                from firebase_admin import credentials, initialize_app, db
                cred = credentials.Certificate("farmzon-abdcb-c4c57249e43b.json")
                current_time = str(datetime.datetime.now())
                default_app = initialize_app(cred, {'databaseURL': 'https://farmzon-abdcb.firebaseio.com/'},
                                             name="food" + str(current_time))
                store = db.reference("Yummy", default_app).child("Orders")
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

        self.add_order()

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
        db.reference("Yummy").child("Orders").child(name).delete()

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
                sm.FadeTransition(duration=.2)
                sm.current = "admin_main"
                self.listen_db()

        else:
            if self.admin_true:
                toast("no internet connection")
                self.spin_active = False
            else:
                self.spin_active = False
                toast("oops! phone number or password in correct or internet connection")

    def listen_db(self):
        try:
            print("i am listening......")
            my_stream = db.reference("Yummy").child("Orders").listen(self.success)
        except:
            pass

    def Permission(self, android=None):
        if self.counter_image <= 0:
            if utils.platform == 'android':
                from gallary import Gambler as GA
                Clock.schedule_once(GA.user_select_image, 0)
                self.admin_product = str(GA.path_of_picture)
                image = self.root.ids.product_image
                image.source = self.admin_product

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
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "DeepPurple"
        self.theme_cls.accent = "Brown"
        # Window.size = (360, 640)
        self.size_x, self.size_y = Window.size
        self.title = "yummy"


if __name__ == '__main__':
    MainApp().run()
