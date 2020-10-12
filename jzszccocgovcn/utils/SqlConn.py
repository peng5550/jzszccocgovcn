import pymysql


HOST = "127.0.0.1"
PORT = 3306
DATABASE = "projects"
TABLE = "jzszcreport"
USER = "root"
PASSWORD = "123456"



class SQLConnection:

    def __init__(self):

        self.conn = pymysql.connect(host=HOST, port=PORT, user=USER, passwd=PASSWORD, db=DATABASE,
                                    charset="utf8")
        self.db = self.conn.cursor()



    def insert_data(self, item_info):
        keys = ', '.join(list(item_info.keys()))
        values = ', '.join(['%s'] * len(item_info))
        insert_sql = "insert into `{}`({})values({});".format(TABLE, keys, values)
        try:
            self.db.execute(insert_sql, tuple(item_info.values()))
            self.conn.commit()
        except Exception as e:
            print(e.args)
            self.conn.rollback()

    def select_data(self, item_info):
        string_list = []
        for i in item_info.keys():
            string = '%s="%s"' % (i, item_info.get(i))
            string_list.append(string)
        sql_string = ' and '.join(string_list)

        select_sql = "select * from {} where {};".format(TABLE, sql_string)

        self.db.execute(select_sql)
        res = self.db.fetchall()
        if res:
            return True
        else:
            return False