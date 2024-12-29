from code import interact
from hmac import new
from math import floor
import math
import arrow

class Universal:
    def __init__(self, semstartdate, mt1date, mt1edate, mt2date, mt2edate, mt3date,exclusions_l,exclusions_r):
        self.semstartdate = date(semstartdate)
        self.mt1date = date(mt1date)
        self.mt1edate = date(mt1edate)
        self.mt2date = date(mt2date)
        self.mt2edate = date(mt2edate)
        self.mt3date = date(mt3date)
        self.exclusions = f_exclusions_l(exclusions_l)
        (self.exclusions).extend(f_exclusions_r(exclusions_r))
        self.remaining_leaves = 0

class subject:
    def __init__(self,name,universal,wlist):
        self.name = name
        self.weeklist = f_weeklist(wlist)
        self.totaldays = numdate_multi(universal.semstartdate, universal.mt3date, self.weeklist)
        self.new_totaldays = final(self.totaldays,universal.exclusions)
        self.total_classes = len(self.new_totaldays)
        self.total_leaves = floor(0.25*len(self.new_totaldays))
        self.class_a = 0
        self.class_l = 0
        self.class_h = self.class_a + self.class_l
        self.mt1classes = 0
        self.mt2classes = 0
        self.mt3classes = 0
        for i in self.new_totaldays:
            if (i < universal.mt1date) :
                self.mt1classes += 1
            if (i < universal.mt2date) :
                self.mt2classes += 1
            if (i < universal.mt3date) :
                self.mt3classes += 1
        self.mt1leaves = floor(0.25*self.mt1classes)
        self.mt2leaves = floor(0.25*self.mt2classes)
        self.mt3leaves = floor(0.25*self.mt3classes)

class user():
    def __init__ (self,userid,listsub):
        self.userid = userid
        self.listsub = listsub
        wlist = ["01-01-25","02-01-25","04-01-25"]
        self.math = subject("math",universal,wlist)
        self.english = subject("english",universal,wlist)
        self.sub_list = {"math" : self.math, "english" : self.english}
        
            
            
def date(strdate):
    ourdate = arrow.get(strdate, "DD-MM-YY")
    return ourdate

def pdate(date):
    str = date.format("DD-MM-YY")
    return str

def f_weeklist(list):
    wlist = []
    for i in list:
        wlist.append(date(i))
    return wlist

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
def f_exclusions_r(list):
    exclusions = []
    for i in range(0,len(list),2):
        start = date(list[i])
        end = date(list[i+1])
        while (start<=end):
            exclusions.append(start)
            start = start.shift(days=1)
        return exclusions

def f_exclusions_l(list):
    exclusions = []
    for i in list:
        exclusions.append(date(i))
    return exclusions

def final(totaldays,exclusions):
    new_totaldays = []
    for i in totaldays:
        if (i not in exclusions):
            new_totaldays.append(i)
    return new_totaldays

def main(sub):
    a = 1
    today = date("01-01-25")
    att = 1
    itemlist = []
    while (a!=0):
        if (today <= universal.mt1date):
            total_leaves = sub.mt1leaves
        if (today > universal.mt1date and today <= universal.mt2date):
            total_leaves = sub.mt2leaves
        if (today > universal.mt2date):
            total_leaves = sub.mt3leaves
        print(f"Today's date is {today}")
        if today in sub.new_totaldays:
            att = int(input(f'Today is {sub.name} period mark attendance 0 or 1 :'))
            if att==1:
                sub.class_a += 1
            else:
                sub.class_l += 1
        else :
            print("No maths period today!")
        sub.remaining_leaves = total_leaves - sub.class_l
        itemlist = {"remaining_leaves" : sub.remaining_leaves, "class_a" : sub.class_a, "class_l" : sub.class_l}
        print(itemlist)
        a = int(input("Continue 0 (no) or 1 (next) or 2 (random date):"))
        if (a==1):
            today = today.shift(days=1)
        elif (a==2):
            today = date(input("Enter the next date :"))
        print("\n\n")

def initial():
    exclusions_l = ["26-01-25","26-02-25"]
    exclusions_r = ["09-03-25","19-03-25"]
    global universal
    universal = Universal("01-01-25", "12-03-25", "17-03-25", "12-04-25", "17-04-25", "12-05-25",exclusions_l,exclusions_r)
    global user1
    user1 = user(1,['math','english','hindi'])

def continous(user):
    math = user.math
    english = user.english
    list = [math,english]
    for i in list:
        main(i)

def show(user1,str):
    sub = user1.sub_list[str]
    print(vars(sub))
    

initial()
continous(user1)
show(user1,"english")


