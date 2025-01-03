from code import interact
import datetime
from hmac import new
from math import floor
import math
from multiprocessing import Value
import arrow
from dotenv import load_dotenv
import asyncio
from telebot.async_telebot import AsyncTeleBot
import os
import json



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

class Subject:
    def __init__(self,name,universal,wlist):
        self.name = name
        self.weeklist = f_weeklist(wlist)
        self.totaldays = numdate_multi(universal.semstartdate, universal.mt3date, self.weeklist)
        self.new_totaldays = final(self.totaldays,universal.exclusions)
        self.total_classes = len(self.new_totaldays)
        self.total_leaves = floor(0.25*len(self.new_totaldays))
        self.class_a = 0
        self.class_l = 0
        self.class_h = 0
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

class User():
    def __init__ (self,userid,dict_wlist):
        self.session_list = []
        self.userid = userid
        self.dict_wlist = dict_wlist
        self.subdict = {}
        for i in dict_wlist:
            self.subdict[f'{i}'] = Subject(i,universal,dict_wlist[i])    
            
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
                sub.class_h += 1
            else:
                sub.class_l += 1
                sub.class_h += 1
        else :
            print(f'No {sub.name} period today!')
        sub.remaining_leaves = total_leaves - sub.class_l
        itemlist = {"remaining_leaves" : sub.remaining_leaves, "class_a" : sub.class_a, "class_l" : sub.class_l}
        print(itemlist)
        a = int(input("Continue 0 (no) or 1 (next) or 2 (random date):"))
        if (a==1):
            today = today.shift(days=1)
        elif (a==2):
            today = date(input("Enter the next date :"))
        print("\n\n")

def initial(userid,dict1):
    userdict.setdefault(userid,User(1,dict1))
    # return userdict[userid]

def continous(user):
    for i in user.subdict:
        main(user.subdict[i])

def today_subject(sub):
    today = date(datetime.date.today())
    if today in sub.new_totaldays:
        return sub.name
    else:
        return 0

def show(user1,str):
    sub = user1.subdict[str]
    print(vars(sub))

exclusions_l = ["26-01-25","26-02-25"]
exclusions_r = ["09-03-25","19-03-25"]
userdict = {}
global universal
universal = Universal("01-01-25", "12-03-25", "17-03-25", "12-04-25", "17-04-25", "12-05-25",exclusions_l,exclusions_r)
load_dotenv()
token = os.getenv("TELEGRAM_BOT_TOKEN")
bot = AsyncTeleBot(token)

@bot.message_handler(commands=['start'])
async def bot_start(message):
    from_user = message.from_user
    reply = f'Hello {from_user.first_name} {from_user.last_name}\n Welcome to the attendance tracker bot !'
    await bot.reply_to(message,reply)
    id = from_user.id
    if id not in userdict:
        await bot.reply_to(message,f'You are not registered kindly register using /register, Thanks')
    await bot.reply_to(message,f'You can always see help using /help.')

@bot.message_handler(commands=['help'])
async def bot_help(message):
    reply = f'Type /start to start the bot. \nType /help for help \nType /register to register yourself on the bot'
    await bot.reply_to(message,reply)

@bot.message_handler(commands=['register'])
async def bot_register(message):
    text = message.text
    dict_text = ((text.strip()).split("#")[1]).strip()

    # # JSON-compatible string representation of a dictionary
    # dict_string = '{"key1": "value1", "key2": "value2"}'

    # Convert to a dictionary
    try:
        result_dict = json.loads(dict_text)
        print(result_dict)
    except json.JSONDecodeError:
        print("Invalid JSON format!")
    print(type(result_dict))
    initial(message.from_user.id,result_dict)

@bot.message_handler(commands=['markattendance'])
async def bot_markattendance(message):
    subdict = userdict[message.from_user.id].subdict
    session_list = []
    for i in subdict:
        subname = today_subject(subdict[i])
        if subname != 0 :
            list.append(subname)
    substr = ",".join(list)
    reply = f'Mark the attendance for the following subjects\n{substr}'
    userdict[message.from_user.id].session_list  = session_list
    await bot.reply_to(message,reply)

@bot.message_handler(commands= ['mark'])
async def bot_mark(message):
    mark_text = message.text.split('#')[1].strip()
    mark_list = mark_text.split(',')
    for i in mark_list:
        i.strip()
    session_list = userdict[message.from_user.id].session_list
    #session_list = ["math", "hndi"]
    #mark_list = ["P","A"]
    att_dict = {}
    for i in range[0,len(mark_list)]:
        att_dict[session_list[i]] = mark_list[i]
    #att_dict = {"math" : "P" , "hindi" : "A"}
    for i in att_dict:
        sub = userdict[message.from_user.id].subdict[i]
        if att_dict[i] == "P" :
            sub.class_a += 1 
            sub.class_h += 1
        else :
            sub.class_l += 1
            sub.class_h += 1
    




asyncio.run(bot.polling())