from hmac import new
from math import floor
import arrow

class Universal:
    def __init__(self, semstartdate, mt1date, mt1edate, mt2date, mt2edate, mt3date,exclusions):
        self.semstartdate = date(semstartdate)
        self.mt1date = date(mt1date)
        self.mt1edate = date(mt1edate)
        self.mt2date = date(mt2date)
        self.mt2edate = date(mt2edate)
        self.mt3date = date(mt3date)
        self.exclusions = exclusions

class subject:
    def __init__(self,universal,weeklist,new_totaldays):
        self.weeklist = weeklist
        self.new_totaldays = new_totaldays
        self.total_classes = len(new_totaldays)
        self.total_leaves = floor(0.25*len(new_totaldays))
        self.class_a = 0
        self.class_l = 0
        self.class_h = self.class_a + self.class_l
        self.mt1leaves = 0
        self.mt2leaves = 0
        self.mt3leaves = 0
        temp = universal.semstartdate
        while temp < universal.mt3date:
            self.mt3leaves += 1
            if temp < universal.mt2date:
                self.mt2leaves += 1
            if temp < universal.mt1date:
                self.mt1leaves += 1
            temp = temp.shift(days=1)  # Update temp

def date(strdate):
    ourdate = arrow.get(strdate, "DD-MM-YY")
    return ourdate

def pdate(date):
    str = date.format("DD-MM-YY")
    return str

def f_weeklist():
    mathweeklist = [date("01-01-25"), date("03-01-25"), date("04-01-25")]
    return mathweeklist

def num_date(semstartdate, mt3date, i):
    l = []
    while i < mt3date:
        l.append(i)
        i = i.shift(weeks=1)
    return l

def numdate_multi(semstartdate, mt3date, weeklist):
    totaldays = []
    for i in weeklist:
        totaldays.extend(num_date(semstartdate, mt3date, i))
    return totaldays

# 18-03-25 from 20-03-25 to 29-03-25
def f_exclusions():
    exclusions = []
    exclusions.append(date("18-03-25"))
    start = date("20-03-25")
    end = date("29-03-25")
    while (start<=end):
        exclusions.append(start)
        start = start.shift(days=1)
    return exclusions

def final(totaldays,exclusions):
    new_totaldays = []
    for i in totaldays:
        if (i not in exclusions):
            new_totaldays.append(i)
    return new_totaldays

exclusions = f_exclusions()
weeklist = f_weeklist()
universal = Universal("01-01-25", "12-03-25", "17-03-25", "12-04-25", "17-04-25", "12-05-25",exclusions)
totaldays = numdate_multi(universal.semstartdate, universal.mt3date, weeklist)
newtotaldays = final(totaldays,exclusions)
math = subject(universal,weeklist,newtotaldays)
print(vars(math))


