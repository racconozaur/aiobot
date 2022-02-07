import sqlite3


class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)  # connection to our db
        self.cursor = self.connection.cursor()  # query to our db

    # functions

    # add user by user id
    def add_user(self, user_id):
        with self.connection:
            return self.cursor.execute("INSERT INTO `users` (`user_id`) VALUES (?)", (user_id,))

    # check if this user exists
    def check_user(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM `users` WHERE `user_id` = ?", (user_id,)).fetchall()
            return bool(len(result))

    # set name ( column name for our phone number => name == phone number )
    def set_name(self, user_id, name):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `name` =? WHERE `user_id` =?", (name, user_id,))

    # set room
    def set_room(self, user_id, room):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `room` =? WHERE `user_id` =?", (room, user_id,))

    # set date
    def set_date(self, user_id, date):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `date` =? WHERE `user_id` =? ", (date, user_id,))

    # set time
    def set_time(self, user_id, time):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `time` =? WHERE `user_id` =?", (time, user_id,))

    # registration stage
    def get_signups(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT `signup` FROM `users` WHERE `user_id` =?", (user_id,)).fetchall()
            for row in result:
                signup = str(row[0])
            return signup

    def set_signup(self, user_id, signup):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `signup` =? WHERE `user_id` =?", (signup, user_id,))

    # get name
    def get_name(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT `name` FROM `users` WHERE `user_id` =?", (user_id,)).fetchall()
            for row in result:
                name1 = str(row[0])
            return name1

    # get room
    def get_room(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT `room` FROM `users` WHERE `user_id` =?", (user_id,)).fetchall()
            for row in result:
                car = str(row[0])
            return car

    # get time
    def get_time(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT `time` FROM `users` WHERE `user_id` =?", (user_id,)).fetchall()
            for row in result:
                time = str(row[0])
            return time

    # get the date
    def get_date(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT `date` FROM `users` WHERE `user_id` =?", (user_id,)).fetchall()
            for row in result:
                date = str(row[0])
            return date

    # del usr

    # def del_usr(self, user_id):

    # get all date
    def get_alld(self):
        with self.connection:
            return self.cursor.execute("SELECT `date`, `user_id` FROM `users`").fetchall()

    def del_usrdate(self, user_id):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `date` = '1111-11-11' WHERE `user_id` =?", (user_id,))

    # is admin

    def get_admin(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT `isadmin` FROM `users` WHERE `user_id` =?", (user_id,)).fetchall()
            for row in result:
                admn = int(row[0])
            return admn

    def set_admin(self, user_id, isadmin):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `isadmin` =? WHERE `user_id` =?", (isadmin, user_id,))

    # get all

    def get_allu(self):
        with self.connection:
            return self.cursor.execute("SELECT * FROM `users`").fetchall()

    # outdated

    def get_outd(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT `outdated` FROM `users` WHERE `user_id` =?", (user_id,)).fetchall()
            for row in result:
                outdate = str(row[0])
            return outdate

    def set_outdated(self, user_id, outdated):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `outdated` =? WHERE `user_id` =?", (outdated, user_id,))
