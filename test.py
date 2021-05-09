import datetime


class number_app:
    time = 0
    print(time)


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
