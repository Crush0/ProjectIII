import pymysql

class DBHelper:
    #创建一个连接
    @staticmethod  # 静态方法
    def __createConnection():
        con=pymysql.connect(host="xxx",port=xxx,user="xxx",password="xxx",db="xxx",charset="utf8")
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
