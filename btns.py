from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# first menu

btnServices = KeyboardButton('Services')
btnContacts = KeyboardButton('Contacts')
btnProfile = KeyboardButton('Profile')


mainMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnServices, btnContacts, btnProfile)

# second menu

btnCheck = KeyboardButton('Check Reservation')
btnReserve = KeyboardButton('Make Reservation')
btnCancel = KeyboardButton('Cancel')

secondMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnCheck, btnReserve, btnCancel)

# rooms menu

room1 = '125'
room2 = '420'
room3 = '108'


btnRoom1 = KeyboardButton(room1)
btnRoom2 = KeyboardButton(room2)
btnRoom3 = KeyboardButton(room3)

roomsMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnRoom1, btnRoom2, btnRoom3, btnCancel)

# set date menu

btnDate = KeyboardButton('/setstate 1')
datesMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnDate)

# set time

btnSetTime = KeyboardButton('/setstate 2')
setTimeMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnSetTime, btnCancel)

# time menu

time1 = '15:00 - 17:00'
time2 = '13:00 - 15-00'
time3 = '20:00 - 22-00'

btnTime1 = KeyboardButton(time1)
btnTime2 = KeyboardButton(time2)
btnTime3 = KeyboardButton(time3)

timeMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnTime1, btnTime2, btnTime3, btnCancel)


# adminka

btnAdmin = KeyboardButton('/setstate 4')
setAdmMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnAdmin, btnCancel)




