import pprint
import arrow
from dotenv import load_dotenv
import asyncio
from requests import session
from telebot.async_telebot import AsyncTeleBot, types
import os
import json
from pymongo import MongoClient
import arrow
import math
import schedule
import time
import pytz
from datetime import datetime


class Universal:
    def __init__(
        self,
        semstartdate,
        mt1date,
        mt1edate,
        mt2date,
        mt2edate,
        mt3date,
        exclusions_l,
        exclusions_r,
    ):
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
    def __init__(self, name, wlist):
        self.name = name
        self.weeklist = f_weeklist(wlist)
        self.totaldays = numdate_multi(
            universal.semstartdate, universal.mt3date, self.weeklist
        )
        self.new_totaldays = final(self.totaldays, universal.exclusions)
        self.total_classes = len(self.new_totaldays)
        self.total_leaves = math.floor(0.25 * len(self.new_totaldays))
        self.class_a = 0
        self.class_l = 0
        self.class_h = 0
        self.mt1classes = 0
        self.mt2classes = 0
        self.mt3classes = 0
        for i in self.new_totaldays:
            if i < universal.mt1date:
                self.mt1classes += 1
            if i < universal.mt2date:
                self.mt2classes += 1
            if i < universal.mt3date:
                self.mt3classes += 1
        self.mt1leaves = math.floor(0.25 * self.mt1classes)
        self.mt2leaves = math.floor(0.25 * self.mt2classes)
        self.mt3leaves = math.floor(0.25 * self.mt3classes)

    def to_dict(self):
        return {
            "name": self.name,
            "weeklist": [pdate(i) for i in self.weeklist],
            "totaldays": [pdate(i) for i in self.totaldays],
            "new_totaldays": [pdate(i) for i in self.new_totaldays],
            "total_classes": self.total_classes,
            "total_leaves": self.total_leaves,
            "class_a": self.class_a,
            "class_h": self.class_h,
            "class_l": self.class_l,
            "mt1classes": self.mt1classes,
            "mt1leaves": self.mt1leaves,
            "mt2classes": self.mt2classes,
            "mt2leaves": self.mt2leaves,
            "mt3classes": self.mt3classes,
            "mt3leaves": self.mt3leaves,
        }

    @classmethod
    def from_dict(cls, data):
        # Create a Subject object with essential data
        weeklist = [date(str(i)) for i in data.get("weeklist", [])]
        obj = cls(data["name"], weeklist)

        # Update the object's attributes from the dictionary
        obj.totaldays = [date(i) for i in data["totaldays"]]
        obj.new_totaldays = [date(i) for i in data["new_totaldays"]]
        obj.total_classes = data["total_classes"]
        obj.total_leaves = data["total_leaves"]
        obj.class_a = data["class_a"]
        obj.class_h = data["class_h"]
        obj.class_l = data["class_l"]
        obj.mt1classes = data["mt1classes"]
        obj.mt1leaves = data["mt1leaves"]
        obj.mt2classes = data["mt2classes"]
        obj.mt2leaves = data["mt2leaves"]
        obj.mt3classes = data["mt3classes"]
        obj.mt3leaves = data["mt3leaves"]
        return obj


class User:
    def __init__(self, userid, username, dict_wlist, daylist):
        self.session_list = []
        self.userid = userid
        self.dict_wlist = dict_wlist
        self.subdict = {}
        self.section = 0
        self.username = username
        self.daylist = daylist
        for i in dict_wlist:
            self.subdict[f"{i}"] = Subject(i, dict_wlist[i])

    def to_dict(self):
        return {
            "session_list": self.session_list,
            "userid": self.userid,
            "dict_wlist": self.dict_wlist,
            "subdict": {key: value.to_dict() for key, value in self.subdict.items()},
            "section": self.section,
            "username": self.username,
            "daylist": self.daylist,
        }

    @classmethod
    def from_dict(cls, data):
        user = cls(
            userid=data["userid"],
            dict_wlist=data["dict_wlist"],
            username=data["username"],
            daylist=data["daylist"],
        )
        # Rebuild the subdict with Subject objects
        user.subdict = {
            key: Subject.from_dict(value) for key, value in data["subdict"].items()
        }
        user.session_list = data["session_list"]
        user.section = data["section"]
        return user


def date(strdate):
    try:
        # Try parsing as DD-MM-YY
        return arrow.get(strdate, "DD-MM-YY")
    except arrow.parser.ParserError:
        # If it fails, try parsing as an ISO 8601 string
        return arrow.get(strdate)


def pdate(date):
    str = date.format("DD-MM-YY")
    return str


def f_weeklist(wlist):
    return [date(str(i)) if not isinstance(i, str) else date(i) for i in wlist]


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
    for i in range(0, len(list), 2):
        start = date(list[i])
        end = date(list[i + 1])
        while start <= end:
            exclusions.append(start)
            start = start.shift(days=1)
        return exclusions


def f_exclusions_l(list):
    exclusions = []
    for i in list:
        exclusions.append(date(i))
    return exclusions


def final(totaldays, exclusions):
    new_totaldays = []
    for i in totaldays:
        if i not in exclusions:
            new_totaldays.append(i)
    return new_totaldays


def main(sub):
    a = 1
    today = date("01-01-25")
    att = 1
    itemlist = []
    while a != 0:
        if today <= universal.mt1date:
            total_leaves = sub.mt1leaves
        if today > universal.mt1date and today <= universal.mt2date:
            total_leaves = sub.mt2leaves
        if today > universal.mt2date:
            total_leaves = sub.mt3leaves
        print(f"Today's date is {today}")
        if today in sub.new_totaldays:
            att = int(input(f"Today is {sub.name} period mark attendance 0 or 1 :"))
            if att == 1:
                sub.class_a += 1
                sub.class_h += 1
            else:
                sub.class_l += 1
                sub.class_h += 1
        else:
            print(f"No {sub.name} period today!")
        sub.remaining_leaves = total_leaves - sub.class_l
        itemlist = {
            "remaining_leaves": sub.remaining_leaves,
            "class_a": sub.class_a,
            "class_l": sub.class_l,
        }
        print(itemlist)
        a = int(input("Continue 0 (no) or 1 (next) or 2 (random date):"))
        if a == 1:
            today = today.shift(days=1)
        elif a == 2:
            today = date(input("Enter the next date :"))
        print("\n\n")


def initial(userid, username, dict1):
    global daylist
    userdict = get_userdict()
    userdict.setdefault(userid, User(userid, username, dict1, daylist))
    return userdict


def continous(user):
    for i in user.subdict:
        main(user.subdict[i])


def today_subject(sub):
    today = date(pdate(arrow.now()))
    print(today)
    if today in sub.new_totaldays:
        return sub.name
    else:
        return 0


def show(user1, str):
    sub = user1.subdict[str]
    print(vars(sub))


def get_userdict():
    dict_data = collection.find_one({"_id": 15122005})
    if not dict_data:
        return {}
    userdict = {}
    for key, value in dict_data.items():
        if key != "_id":
            userdict[key] = User.from_dict(value)
    return userdict


def update_userdict(userdicto):
    userdictd = {}
    for i in userdicto:
        if i != "_id":
            userdictd[i] = userdicto[i].to_dict()
    collection.update_one({"_id": 15122005}, {"$set": userdictd})


load_dotenv()
token = os.getenv("TELEGRAM_BOT_TOKEN_TEST")    
bot = AsyncTeleBot(token)

URI = os.getenv("MONGODB_URI")
client = MongoClient(URI)
db = client.bot_test
collection = db.Userdict
exclusions_l = ["26-02-25", "31-03-25", "10-04-25", "18-04-25"]
exclusions_r = ["08-03-25", "16-03-25"]
first_date = date("01-01-25")
daylist = {pdate(first_date.shift(days=i)): False for i in range(1600)}
userdict = {}
global universal
universal = Universal(
    "02-01-25",
    "06-02-25",
    "08-02-25",
    "27-03-25",
    "29-03-25",
    "02-05-25",
    exclusions_l,
    exclusions_r,
)
if collection.find_one({"_id": 15122005}) == None:
    userdict = {"_id": 15122005}
    collection.insert_one(userdict)
else:
    userdict = get_userdict()


@bot.message_handler(commands=["start"])
async def bot_start(message):
    userdict = get_userdict()
    from_user = message.from_user
    reply = f"Hello {from_user.first_name}\n Welcome to the attendance tracker bot !"
    await bot.reply_to(message, reply)
    id = str(from_user.id)
    await bot.reply_to(message, f"You can always see help using /help.")
    if id not in userdict:
        await bot_registerb(message)


@bot.message_handler(commands=["help"])
async def bot_help(message):
    reply = """1.Type /start to start the bot.
    If your section is not mentioned then use /register &
      Example : 
    /register & 
    {
            "MAT" : ["02-01-25","06-01-25","07-01-25","07-01-25"],
            "PHY" : ["06-01-25","07-01-25","08-01-25"],
            "SS" : ["06-01-25","08-01-25"],
            "EEE" : ["03-01-25","06-01-25","08-01-25"],
            "ED" : ["02-01-25","07-01-25","08-01-25"],
            "TC" : ["07-01-25","07-01-25"],
            "PHY-Lab" : ["06-01-25"],
            "ED-Lab" : ["03-01-25"],
            "EEE-Lab" : ["02-01-25"],
            "TC-Lab" : ["06-01-25","03-01-25"],
            "Sports" : ["07-01-25","08-01-25"]
        }
    Type /markattendance to mark attendance
    Type /showattendance to show attendance of all subjects"""
    await bot.reply_to(message, reply)


@bot.message_handler(commands=["register"])
async def bot_register(message):
    global userdict
    if str(message.from_user.id) not in userdict:
        text = message.text
        dict_text = ((text.strip()).split("&")[1]).strip()
        if dict_text in ["PG2", "pg2"]:
            print("Under pg2")
            dict_text = '{"MAT" : ["02-01-25","06-01-25","07-01-25","07-01-25"],"PHY" : ["06-01-25","07-01-25","08-01-25"],"SS" : ["06-01-25","08-01-25"],"EEE" : ["03-01-25","06-01-25","08-01-25"],"ED" : ["02-01-25","07-01-25","08-01-25"],"TC" : ["07-01-25","07-01-25"],"PHY-Lab" : ["06-01-25"],"ED-Lab" : ["03-01-25"],"EEE-Lab" : ["02-01-25"],"TC-Lab" : ["06-01-25","03-01-25"],"Sports" : ["07-01-25","08-01-25"]}'
        try:
            result_dict = json.loads(dict_text)
        except json.JSONDecodeError:
            print("Invalid JSON format!")
        userdict = initial(
            str(message.from_user.id), str(message.from_user.first_name), result_dict
        )
        update_userdict(userdict)
        await bot.reply_to(message, f"You are registerd, now you can procees further !")
    else:
        await bot.reply_to(message, "You are already registered !")


@bot.message_handler(commands=["registerb"])
async def bot_registerb(message):
    global userdict
    if str(message.from_user.id) not in userdict:
        markup = types.InlineKeyboardMarkup()
        pg1 = types.InlineKeyboardButton("PG2", callback_data="section_PG1")
        markup.add(pg1)
        await bot.send_message(
            message.chat.id, "Choose your section", reply_markup=markup
        )

        # text = message.text
        # dict_text = ((text.strip()).split("&")[1]).strip()
        # if dict_text in ["PG2", "pg2"]:
        #     print("Under pg2")
        #     dict_text = '{"MAT" : ["02-01-25","06-01-25","07-01-25","07-01-25"],"PHY" : ["06-01-25","07-01-25","08-01-25"],"SS" : ["06-01-25","08-01-25"],"EEE" : ["03-01-25","06-01-25","08-01-25"],"ED" : ["02-01-25","07-01-25","08-01-25"],"TC" : ["07-01-25","07-01-25"],"PHY-Lab" : ["06-01-25"],"ED-Lab" : ["03-01-25"],"EEE-Lab" : ["02-01-25"],"TC-Lab" : ["06-01-25","03-01-25"],"Sports" : ["07-01-25","08-01-25"]}'
        # try:
        #     result_dict = json.loads(dict_text)
        # except json.JSONDecodeError:
        #     print("Invalid JSON format!")
        # userdict = initial(
        #     str(message.from_user.id),
        #     str(message.from_user.first_name + message.from_user.last_name),
        #     result_dict,
        update_userdict(userdict)
    else:
        await bot.reply_to(message, f"You are already registered !")


# @bot.callback_query_handler(func=lambda call: True)
# async def handle_query(call):
#     global userdict
#     if call.data == "PG1":
#         dict_text = '{"MAT" : ["02-01-25","06-01-25","07-01-25","07-01-25"],"PHY" : ["06-01-25","07-01-25","08-01-25"],"SS" : ["06-01-25","08-01-25"],"EEE" : ["03-01-25","06-01-25","08-01-25"],"ED" : ["02-01-25","07-01-25","08-01-25"],"TC" : ["07-01-25","07-01-25"],"PHY-Lab" : ["06-01-25"],"ED-Lab" : ["03-01-25"],"EEE-Lab" : ["02-01-25"],"TC-Lab" : ["06-01-25","03-01-25"],"Sports" : ["07-01-25","08-01-25"]}'
#         try:
#             result_dict = json.loads(dict_text)
#         except json.JSONDecodeError:
#             print("Invalid JSON format!")
#         userdict = initial(
#             str(call.from_user.id),
#             str(call.from_user.first_name),
#             result_dict
#         )
#         update_userdict(userdict)
#         await bot.reply_to(call.from_user.id, f"You are registerd, now you can procees further !")
#         await bot.send_message(call.from_user.id, "PG1 selected")


@bot.callback_query_handler(func=lambda call: call.data.startswith("section_"))
async def handle_query(call):
    global userdict
    l = call.data.split("_")
    a = l[1]
    # Send a message to acknowledge the button click
    await bot.answer_callback_query(call.id, "Section selected!")

    if a == "PG1":
        dict_text = '{"MAT" : ["02-01-25","06-01-25","07-01-25","07-01-25"],"PHY" : ["06-01-25","07-01-25","08-01-25"],"SS" : ["06-01-25","08-01-25"],"EEE" : ["03-01-25","06-01-25","08-01-25"],"ED" : ["02-01-25","07-01-25","08-01-25"],"TC" : ["07-01-25","07-01-25"],"PHY-Lab" : ["06-01-25"],"ED-Lab" : ["03-01-25"],"EEE-Lab" : ["02-01-25"],"TC-Lab" : ["06-01-25","03-01-25"],"Sports" : ["07-01-25","08-01-25"]}'

        try:
            result_dict = json.loads(dict_text)
        except json.JSONDecodeError:
            await bot.send_message(call.message.chat.id, "Invalid JSON format!")
            return

        userdict = initial(
            str(call.from_user.id), str(call.from_user.first_name), result_dict
        )

        update_userdict(userdict)
        await bot.send_message(
            call.message.chat.id, "You have been registered successfully!"
        )


@bot.message_handler(commands=["markattendance"])
async def bot_markattendance(message):
    userdict = get_userdict()
    daylist = userdict[str(message.from_user.id)].daylist
    today_date = pdate(arrow.now())
    if daylist[today_date] == False:
        subdict = userdict[str(message.from_user.id)].subdict
        session_list = []
        for i in subdict:
            subname = today_subject(subdict[i])
            if subname != 0:
                session_list.append(subname)
        if len(session_list) != 0:
            session_list.append(len(session_list))
            session_list.append(0)
            actual_list = session_list[0 : len(session_list) - 2]
            substr = ",".join(actual_list)
            # reply = f"Mark the attendance for the following subjects\n{substr}"
            markup = types.InlineKeyboardMarkup()
            for i in actual_list:
                # Create subject button (disabled by making it unclickable)
                subject_name = types.InlineKeyboardButton(
                    i, callback_data=f"subject_{i}"
                )

                # Create Present and Absent buttons with appropriate callback_data
                present = types.InlineKeyboardButton(
                    "Present ✅", callback_data=f"attendance_{i}_P"
                )
                absent = types.InlineKeyboardButton(
                    "Absent ❌", callback_data=f"attendance_{i}_A"
                )
                # Add buttons to markup
                markup.add(subject_name, present, absent)

            # Send the message with inline keyboard
            await bot.send_message(
                message.chat.id, "Choose your option:", reply_markup=markup
            )
        else:
            reply = "No periods today, hence no attendance to mark !"
            await bot.reply_to(message, reply)
        userdict[str(message.from_user.id)].session_list = session_list
    else:
        session_list = []
        userdict[str(message.from_user.id)].session_list = session_list
        await bot.reply_to(message, f"You have already marked attendance for today!")
    update_userdict(userdict)


@bot.callback_query_handler(func=lambda call: call.data.startswith("attendance_"))
async def handle_attendance(call):
    userdict = get_userdict()
    data = call.data.split("_")
    subject = data[1]
    status = data[2]
    user = userdict[str(call.from_user.id)]
    session_list = user.session_list
    if status == "P":
        sub = user.subdict[subject]
        sub.class_a += 1
        sub.class_h += 1
        session_list[len(session_list) - 1] += 1
        await bot.answer_callback_query(call.id, f"Marked {subject} as Present ✅")

    elif status == "A":
        sub = user.subdict[subject]
        sub.class_l += 1
        sub.class_h += 1
        session_list[len(session_list) - 1] += 1
        await bot.answer_callback_query(call.id, f"Marked {subject} as Absent ❌")

    if session_list[len(session_list) - 1] == session_list[len(session_list) - 2]:
        reply = "Attendance marked for today successfully !"
        today_date = pdate(arrow.now())
        daylist = user.daylist
        daylist[today_date] = True
        session_list = []
        user.session_list = session_list
        await bot.send_message(
            call.message.chat.id, f"Attendance marked for {today_date} successfully !"
        )

    update_userdict(userdict)


@bot.message_handler(commands=["mark"])
async def bot_mark(message):
    userdict = get_userdict()
    session_list = userdict[str(message.from_user.id)].session_list
    if len(session_list) != 0:
        mark_text = message.text.split("&")[1].strip()
        mark_list = mark_text.split(",")
        for i in mark_list:
            i.strip()
        # session_list = ["math", "hndi"]
        # mark_list = ["P","A"]
        att_dict = {}
        for i in range(0, len(mark_list)):
            att_dict[session_list[i]] = mark_list[i]
        # att_dict = {"math" : "P" , "hindi" : "A"}
        for i in att_dict:
            sub = userdict[str(message.from_user.id)].subdict[i]
            print(att_dict)
            if att_dict[i] == "P" or att_dict[i] == "p":
                sub.class_a += 1
                sub.class_h += 1
            else:
                sub.class_l += 1
                sub.class_h += 1
            reply = "Attendanced marked for today successfully !"
            today_date = pdate(arrow.now())
            daylist = userdict[str(message.from_user.id)].daylist
            daylist[today_date] = True
            session_list = []
            userdict[str(message.from_user.id)].session_list = session_list
    else:
        reply = "No periods today, hence no attendance to mark. \nor You have marked today's attendance earlier."
    update_userdict(userdict)
    await bot.reply_to(message, reply)


@bot.message_handler(commands=["showattendance"])
async def bot_showattendance(message):
    userdict = get_userdict()
    user = userdict[str(message.from_user.id)]
    subdict = user.subdict
    for i in subdict:
        sub = subdict[i]
        reply = f"Subject : {sub.name}\nTotal classes taken : {sub.class_h}\nTotal classes attended : {sub.class_a}\nTotal leaves taken : {sub.class_l}\n Leaves till MT1,MT2,ET are : {sub.mt1leaves} {sub.mt2leaves} {sub.mt3leaves}"
        await bot.reply_to(message, reply)


# Define the IST time zone
IST = pytz.timezone("Asia/Kolkata")


async def markattendance():
    global userdict
    print("Executing markattendance...")
    userdict = get_userdict()
    for userid in userdict:
        if userid != "_id":
            daylist = userdict[userid].daylist
            today_date = pdate(arrow.now())
            if daylist[today_date] == False:
                subdict = userdict[userid].subdict
                session_list = []
                for i in subdict:
                    subname = today_subject(subdict[i])
                    if subname != 0:
                        session_list.append(subname)
                if len(session_list) != 0:
                    substr = ",".join(session_list)
                    reply = f"Mark the attendance for the following subjects\n{substr}\n Type /markattendance"
                userdict[userid].session_list = session_list
                await bot.send_message(int(userid), reply)
            update_userdict(userdict)


# Asynchronous scheduling function
async def schedule_task():
    while True:
        now = datetime.now(IST)
        if now.hour == 22 and now.minute == 0:  # Example: run at 9 AM IST
            await markattendance()
        await asyncio.sleep(60)  # Check every minute


# Start the bot and schedule task simultaneously
async def main2():
    bot_task = asyncio.create_task(bot.polling())
    schedule_task_instance = asyncio.create_task(schedule_task())
    await asyncio.gather(bot_task, schedule_task_instance)


# Run the main function
if __name__ == "__main__":
    asyncio.run(main2())
