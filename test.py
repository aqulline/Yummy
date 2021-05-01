import datetime


class number_app:
    time = 0
    print(time)


class NOTIFIC():
    from plyer import uniqueid
    proxy_dict = {
        "http": "http://127.0.0.1",
        "https": "http://127.0.0.1",
    }
    config = {
        "apiKey": "AIzaSyDveKdgwTTz8wPgxj7TgIZ6tB1ER0BXG5I",
        "authDomain": "farmzon-abdcb.firebaseapp.com",
        "databaseURL": "https://farmzon-abdcb.firebaseio.com",
        "storageBucket": "farmzon-abdcb.appspot.com",
        "serviceAccount": "farmzon-abdcb-firebase-adminsdk-uudib-6e5e724931.json"
    }

    def notify(self):
        registration_id = "5c:26:0a:51:c9:86"
        from pyfcm import FCMNotification
        push_service = FCMNotification(api_key="AIzaSyDveKdgwTTz8wPgxj7TgIZ6tB1ER0BXG5I", proxy_dict=self.proxy_dict)
        message_title = "Uber update"
        message_body = "Hi john, your customized news for today is ready"
        result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title,
                                                   message_body=message_body)
        print(result)

    print(uniqueid.id)


# NOTIFIC.notify(NOTIFIC())

import random

x = random

print(x.random())