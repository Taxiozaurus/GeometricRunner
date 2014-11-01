import MySQLdb

# for this class to work you will need a MySQL database that presumably has 2 tables
# t1:
#   users
#       id int primary auto_inc
#       nick
#       password
#
# t2
#   hiscore
#       u_id int FK_users_id
#       level varchar
#       score


class Score :
    def __init__(self) :
        self.db_con = MySQLdb.connect(host='', user='', passwd='', db='')
        self.c = self.db_con.cursor()

    def login(self, nick, password) :
        my_query = "SELECT * FROM users WHERE nick = '" + nick + "';"
        self.c.execute(my_query)
        ans = self.c.fetchone()
        if ans :
            if ans[2] == password :
                return ans[0]
            else :
                return ""
        else :
            return ""

    def register(self, nick, password):
        data = self.login(nick, password)
        if data > -1 :
            my_query = "INSERT INTO users (nick, password) VALUES ('" + nick + "','" + password + "')"
            self.c.execute(my_query)
            self.db_con.commit()
        return self.login(nick, password)


    def send_score(self, u_id, level, score) :
        my_query = "SELECT score FROM hiscore WHERE u_id = " + str(u_id) + " AND level = '" + level + "' ;"
        self.c.execute(my_query)
        ans = self.c.fetchone()
        if ans :
            if ans[0] < score :
                my_query = "UPDATE hiscore SET score = " + str(score) + " WHERE u_id = " + str(u_id) + " AND level = '" + level + "';"
                self.c.execute(my_query)
        else :
            my_query = "INSERT INTO hiscore VALUES (" + str(u_id) + ",'" + level + "'," + str(score) + ");"
            self.c.execute(my_query)
        self.db_con.commit()

    def get_scores(self, level) :
        my_query = "SELECT nick, score FROM users JOIN hiscore ON id = u_id WHERE level = '" + level + "' ORDER BY score LIMIT 0,10 ;"
        self.c.execute(my_query)
        ans = self.c.fetchall()
        self.db_con.commit()
        if len(ans) > 0 :
            return ans
        else :
            return []

    def finish(self):
        self.db_con.commit()
        self.c.close()
        self.db_con.close()