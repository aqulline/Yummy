import json
import requests


def send_sms(phone, location):
    URL = 'https://apisms.beem.africa/v1/send'
    content_type = 'application/json'
    source_addr = 'INFO'
    secrete_key = "ZGVmNWVkMzYxZmRhNWQ3MjM3NDhkMThmMWFkYzg4ZTM0ZGUwMjZmMGZjYTkzNWNkODRkMzFiMWJkZmM0M2JmYw=="
    api_key = '8ccab9418dedde47'
    phonee = phone_repr(phone)
    apikey_and_apisecret = api_key + ':' + secrete_key

    first_request = requests.post(url=URL, data=json.dumps({
        'source_addr': 'INFO',
        'schedule_time': '',
        'encoding': '0',
        'message': f'Thank you for ordering with YUMMY {phonee} we shall deliver to you soon at {location}, your '
                   f'mostly welcome to order again',
        'recipients': [
            {
                'recipient_id': 1,
                'dest_addr': phonee,
            }
        ],
    }),

                                  headers={
                                      'Content-Type': content_type,
                                      'Authorization': 'Basic ' + api_key + ':' + secrete_key,
                                  },
                                  auth=(api_key, secrete_key), verify=False)

    print(first_request.status_code)
    print(first_request.json())
    return (first_request.json())


# send_sms('255786857974', 'moshi')
def phone_repr(phone):
    new_number = ""
    if phone != "":
        for i in range(phone.__len__()):
            if i == 0:
                pass
            else:
                new_number = new_number + phone[i]
        number = "255" + new_number
        public_number = number
        return public_number


phone_repr('0786857974')
