import pymysql

class DBHelper:
    #创建一个连接
    @staticmethod  # 静态方法
    def __createConnection():
        con=pymysql.connect(host="sh-cynosdbmysql-grp-4y65np2q.sql.tencentcdb.com",port=22505,user="ytc",password="Yan20010703",db="project",charset="utf8")
        return con

    # 执行单向操作：添，删，改
    @staticmethod   #静态方法
    def RunSQL(sql):
        con=DBHelper.__createConnection()
        bol=True
        cmd=con.cursor()
        try:
            cmd.execute(sql)
            con.commit()
        except Exception as e:
            print(e)
            bol=False
            con.rollback()

        cmd.close()
        con.close()
        return bol

    # 执行对向操作：查
    @staticmethod
    def RunSQLReturnRS(sql):
        con=DBHelper.__createConnection()
        cmd=con.cursor()
        cmd.execute(sql)
        rs=cmd.fetchall()

        cmd.close()
        con.close()
        return rs