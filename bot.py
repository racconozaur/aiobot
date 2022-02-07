from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from datetime import date, datetime
import locale
import logging
import asyncio

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware

from utils import TestStates
# from file db.py importing our class Database
from db import Database

# importing our btns file
import btns

# set local time
locale.setlocale(locale.LC_TIME, 'C')

TOKEN = "token"  # change this to ur token

bot = Bot(token=TOKEN)

# set level of logging

logging.basicConfig(level=logging.INFO)

dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())

# connection our db file
db = Database('reservation.db')


# on command start
@dp.message_handler(commands="start")
async def cmd_start(message: types.Message):
    await bot.send_message(message.from_user.id, '✌️ {0.first_name}'.format(message.from_user))

    if not db.check_user(message.from_user.id):
        db.add_user(message.from_user.id)
        await bot.send_message(message.from_user.id, "Enter ur Phone number 📱")

    else:
        await bot.send_message(message.from_user.id, "You are already registered 😄", reply_markup=btns.mainMenu)


# on command admin
@dp.message_handler(commands="admin")
async def admin(message: types.Message):
    await bot.send_message(message.from_user.id,
                           'Please press the "/setstate 4" button\n and then enter the admin password *️⃣',
                           reply_markup=btns.setAdmMenu)


# state machine
@dp.message_handler(state='*', commands=['setstate'])
async def process_setstate_command(message: types.Message):
    argument = message.get_args()
    state = dp.current_state(user=message.from_user.id)
    if not argument:
        await state.reset_state()
        return await message.reply('state rested ')

    if (not argument.isdigit()) or (not int(argument) < len(TestStates.all())):
        return await message.reply('invalid key'.format(key=argument))

    await state.set_state(TestStates.all()[int(argument)])
    await message.reply('state changed', reply=False)


# first state
@dp.message_handler(state=TestStates.TEST_STATE_1)
async def first_test_state_case_met(message: types.Message):
    # getting our message and converting it into date format
    dateStr = message.text
    dateConv = datetime.strptime(dateStr, "%Y-%m-%d").date()
    # validation
    if dateConv < date.today():
        await message.reply('❗️incorrect dat')
    else:
        # more validation
        if db.get_signups(message.from_user.id) == "done":
            db.set_date(message.from_user.id, message.text)
            await message.reply('ℹ️date saved')
            await message.reply("ℹNow press <b>here '/setstate'</b> and peak available time",
                                reply_markup=btns.timeMenu, reply=False, parse_mode=types.ParseMode.HTML)


# state 4
@dp.message_handler(state=TestStates.TEST_STATE_4)
async def second_test_state_case_met(message: types.Message):
    # checking our password
    if message.text == 'admin1337':
        if db.get_admin(message.from_user.id) == int(0):
            # set admin in database
            db.set_admin(message.from_user.id, int(1))
            await bot.send_message(message.from_user.id, "✳️Now you have admin rights\n")
            await bot.send_message(message.from_user.id, "/getall - to get all users\n"
                                                         "You can also send messages to all users by typing '!send' and after ur message\n"
                                                         "/setstate and then press cancel button to exit")
        elif db.get_admin(message.from_user.id) == int(1):
            await bot.send_message(message.from_user.id, "✳️You already have admin rights")
            await bot.send_message(message.from_user.id, "/getall - to get all users\n"
                                                         "You can also send messages to all users by typing '!send' and after ur message\n"
                                                         "/setstate and then press cancel button to exit")
        else:
            await message.reply("❗️Incorrect")

    # get all users from our db
    elif message.text == '/getall':
        # validation
        if db.get_admin(message.from_user.id) == int(1):
            allUsers = db.get_allu()
            for row in allUsers:
                await bot.send_message(message.from_user.id, text=f'Id: <b>{row[0]}</b>\n'
                                                                  f'UserId: <b>{row[1]}</b>\n'
                                                                  f'Number: <b>{row[2]}</b>\n'
                                                                  f'Room reserved: <b>{row[3]}</b>\n'
                                                                  f'Time: <b>{row[4]}</b>\n'
                                                                  f'Date: <b>{row[5]}</b>\n'
                                                                  f'Is Admin: <b>{row[7]}</b>',
                                       parse_mode=types.ParseMode.HTML)
        else:
            await message.reply('❗️ur not admin')

    # send message to all users in db
    elif '!send' in message.text:
        # checking to admin rights
        if db.get_admin(message.from_user.id) == int(1):
            text = message.text[6:]  # cutting our !send symbols
            sendAll = db.get_allu()
            for row in sendAll:
                await bot.send_message(row[1], text)
        else:
            await message.reply('❗️ur not admin')
    else:
        await message.reply('incorrect password')


@dp.message_handler()
async def bot_message(msg: types.Message):
    if msg.chat.type == 'private':
        if msg.text == 'Profile':
            user_name = "✅Your number is: " + db.get_name(msg.from_user.id)
            await bot.send_message(msg.from_user.id, user_name)

        elif msg.text == 'Services':
            await bot.send_message(msg.from_user.id, 'Available Services🔣', reply_markup=btns.secondMenu)

        elif msg.text == 'Contacts':
            await bot.send_message(msg.from_user.id, '✅Our Contacts: <b>+998912345678</b>',
                                   parse_mode=types.ParseMode.HTML)

        elif msg.text == 'Cancel':
            await bot.send_message(msg.from_user.id, "Main Menu🔣", reply_markup=btns.mainMenu)

        elif msg.text == 'Make Reservation':
            await bot.send_message(msg.from_user.id, "please select available rooms ", reply_markup=btns.roomsMenu)

        # rooms
        elif msg.text == btns.room1:
            if db.get_signups(msg.from_user.id) == "done":  # check our registration status
                db.set_room(msg.from_user.id, msg.text)
                await bot.send_message(msg.from_user.id, "You reserved: " + btns.room1, reply_markup=btns.datesMenu)
                # date
                await bot.send_message(msg.from_user.id,
                                       "Now enter the reservation date\n"
                                       "by pressing '/setstate 1' button\n"
                                       "Date should be in this format: \n"
                                       "<b>year-month-day</b>\n"
                                       "Example: <b>2022-01-30</b>",
                                       parse_mode=types.ParseMode.HTML)

        elif msg.text == btns.room2:
            if db.get_signups(msg.from_user.id) == "done":  # check our registration status
                db.set_room(msg.from_user.id, msg.text)
                await bot.send_message(msg.from_user.id, "You reserved: " + btns.room2, reply_markup=btns.datesMenu)
                # date
                await bot.send_message(msg.from_user.id,
                                       "Now enter the reservation date\n"
                                       "by pressing '/setstate 1' button\n"
                                       "Date should be in this format: \n"
                                       "<b>year-month-day</b>\n"
                                       "Example: <b>2022-01-30</b>",
                                       parse_mode=types.ParseMode.HTML)

        elif msg.text == btns.room3:
            if db.get_signups(msg.from_user.id) == "done":  # check our registration status
                db.set_room(msg.from_user.id, msg.text)
                await bot.send_message(msg.from_user.id, "You reserved: " + btns.room3, reply_markup=btns.datesMenu)
                # date
                await bot.send_message(msg.from_user.id,
                                       "Now enter the reservation date\n"
                                       "by pressing '/setstate 1' button\n"
                                       "Date should be in this format: \n"
                                       "<b>year-month-day</b>\n"
                                       "Example: <b>2022-01-30</b>",
                                       parse_mode=types.ParseMode.HTML)

        # time
        elif msg.text == btns.time1:
            if db.get_signups(msg.from_user.id) == "done":
                db.set_time(msg.from_user.id, msg.text)
                await msg.reply('U peaked' + btns.time1)
                await msg.reply('Ur reservation is done\n'
                                'You can check the reservation in this menu: ',
                                reply_markup=btns.secondMenu)

        elif msg.text == btns.time2:
            if db.get_signups(msg.from_user.id) == "done":
                db.set_time(msg.from_user.id, msg.text)
                await msg.reply('U peaked' + btns.time2)
                await msg.reply('Ur reservation is done\n'
                                'You can check the reservation in this menu: ',
                                reply_markup=btns.secondMenu)

        elif msg.text == btns.time3:
            if db.get_signups(msg.from_user.id) == "done":
                db.set_time(msg.from_user.id, msg.text)
                await msg.reply('U peaked' + btns.time3)
                await msg.reply('Ur reservation is done\n'
                                'You can check the reservation in this menu: ',
                                reply_markup=btns.secondMenu)

        elif msg.text == 'date':
            user_date = 'Ur date is: ' + db.get_date(msg.from_user.id)
            await bot.send_message(msg.from_user.id, user_date)

        elif msg.text == 'Check Reservation':
            num = db.get_name(msg.from_user.id)
            rum = db.get_room(msg.from_user.id)
            time = db.get_time(msg.from_user.id)
            dt = db.get_date(msg.from_user.id)
            await bot.send_message(msg.from_user.id, f'Your number: <b>{num}</b>\n'
                                                     f'Reserved room: <b>{rum}</b>\n'
                                                     f'Time: <b>{time}</b>\n'
                                                     f'Reservation date: <b>{dt}</b>', parse_mode=types.ParseMode.HTML)

        else:
            if db.get_signups(msg.from_user.id) == "setname":
                # validation
                if len(msg.text) > 13:
                    await msg.reply('Ur number should contain 13 characters')
                elif not '+998' in msg.text:
                    await msg.reply('Ur number should begin with <b>(+998)</b>', parse_mode=types.ParseMode.HTML)
                else:
                    db.set_name(msg.from_user.id, msg.text)
                    db.set_signup(msg.from_user.id, "done")
                    await bot.send_message(msg.from_user.id, "You have successfully registered",
                                           reply_markup=btns.mainMenu)
            else:
                await bot.send_message(msg.from_user.id, "Incorrect input")

    else:
        await bot.send_message(msg.from_user.id, " Messages from Groups are not allowed")


# checking dates from db every x-seconds after starting bot
# NOW THE BOT DOES A CHECK EVERY 300 SECONDS
async def gg(wait):
    while True:
        # set timer
        await asyncio.sleep(wait)
        # get all by id and date
        alls = db.get_alld()
        for row in alls:
            # converting to date format
            a = datetime.strptime(row[0], "%Y-%m-%d").date()
            #
            exp = '1111-11-11'
            err = datetime.strptime(exp, "%Y-%m-%d").date()

            if a == date.today():
                await bot.send_message(row[1], 'one day left')

            # set outdated date to db
            elif a == err:
                if db.get_outd(row[1]) == 'no':
                    db.set_outdated(row[1], 'yes')

            elif a < date.today():
                db.del_usrdate(row[1])
                await bot.send_message(row[1], 'Your order was canceled due to delay')


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(gg(300))  # set a time to check
    executor.start_polling(dp, skip_updates=True, loop=loop)
