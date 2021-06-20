import datetime
import os


def day_calc():
    date1 = datetime.datetime.now()
    date2 = datetime.datetime(day=20, month=6, year=2021)

    today = str(datetime.date.today())
    y, mon, day = today.strip().split("-")
    DAYNAMES = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    name = DAYNAMES[datetime.date(int(y), int(mon), int(day)).weekday()]
    timedelta = date1 - date2
    #print(timedelta)
    time, sec = str(timedelta).split(",")
    day1, time = str(timedelta).split(",")
    num, wrd = str(day1).split(" ")
    new = wrd + "_" + num
    # print(new, name)
    week_day = str(name)
    day = str(new)

    return day1


def viewfiles():
    filenames = os.listdir('tester')
    list_name = ['connection_status.py', 'image_store.py', '__pycache__', 'tester']
    for files in filenames:
        if files in list_name:
            pass
        else:
            x = day_calc()
            print(x)
            if x == -7:
                os.remove(files)
                print('deleted', files)


