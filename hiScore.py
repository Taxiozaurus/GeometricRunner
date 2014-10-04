import _mysql

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
        self.db_con = _mysql.connect(host='', user='', passwd='s', db='')

    def login(self, nick, password) :
        my_query = "SELECT * FROM users WHERE nick = '" + nick + "';"
        self.db_con.query(my_query)
        db_res = self.db_con.store_result()
        ans = db_res.fetch_rows()
        if len(ans) > 0 :
            if ans[0][2] == password :
                return ans[0]
            else :
                return ""
        else :
            return ""

    def send_score(self, u_id, level, score) :
        my_query = "SELECT score FROM hiscore WHERE u_id = " + u_id + " AND level = '" + level + "';"
        self.db_con.query(my_query)
        db_res = self.db_con.store_result()
        ans = db_res.fetch_rows()

        if len(ans) > 0 :
            if ans[0][0] < score :
                my_query = "UPDATE hiscore SET score = " + score + " WHERE u_id = " + u_id + " AND level = '" + level + "';"
                self.db_con.query(my_query)
        else :
            my_query = "INSERT INTO hiscore VALUES (" + u_id + ",'" + level + "'," + score + ");"
            self.db_con.query(my_query)

    def get_scores(self, level) :
        my_query = "SELECT * FROM users JOIN hiscore ON id = u_id WHERE level = '" + level + "' LIMIT 0,10 ;"
        self.db_con.query(my_query)
        db_res = self.db_con.store_result()
        ans = db_res.fetch_rows(maxrows=0)
        if len(ans) > 0 :
            return ans
        else :
            return []