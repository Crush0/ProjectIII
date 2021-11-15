from utils.DBUnitls import DBHelper as db


class UserService:
    @staticmethod
    def login(username, password):
        try:
            sql_exist = f'select * from user where username=\'{username}\''
            rs = db.RunSQLReturnRS(sql_exist)
            if len(rs) == 0:
                return {'result': False, 'message': '用户名不存在'}
            if rs[0][2] == password:
                user = {
                    'id': rs[0][0],
                    'username': rs[0][1],
                    'password':rs[0][2],
                    'email':rs[0][3],
                    'phone':rs[0][4],
                    'sex':'男' if rs[0][5] == 1 else '女',
                    'head':rs[0][5]
                }
                return {'result': True, 'message': '登录成功', 'user': user}
            else:
                return {'result': False, 'message': '密码错误'}
        except Exception as e:
            print(e)
            return {'result': False, 'message': '内部服务器错误'}


    @staticmethod
    def register(username, password, twice):
        try:
            if password != twice:
                return {'result': False, 'message': '两次密码输入不一致'}
            sql_exist = f'select count(*) from user where username=\'{username}\''
            rs = db.RunSQLReturnRS(sql_exist)
            if rs[0][0] != 0:
                return {'result': False, 'message': '用户名已存在'}
            sql_reg = f'insert into user(username,password) values(\'{username}\',\'{password}\')'
            if db.RunSQL(sql_reg):
                return {'result': True, 'message': '注册成功'}
            else:
                return {'result': False, 'message': '注册失败'}
        except Exception as e:
            print(e)
            return {'result': False, 'message': '内部服务器错误'}

    # status -1 发送申请 1 收到申请 0 忽略请求 100 为好友 -100 拒绝请求
    @staticmethod
    def addFriend(userid,friendName):
        sql_exist = f'select * from user where username=\'{friendName}\''
        rs = db.RunSQLReturnRS(sql_exist)
        if len(rs) == 0:
            return {'result': False, 'message': '用户名不存在'}
        sql_isFriend = f'select * from friend where userid={userid} AND friendid={rs[0][0]}'
        rs2 = db.RunSQLReturnRS(sql_isFriend)
        if len(rs2)!=0 and rs[0][3] == 100:
            return {'result': False, 'message': '你们已经是好友了'}
        elif len(rs2) == 0:
            sql_1 = f'insert into friend(userid,friendid,status) values({userid},{rs[0][0]},-1)'
            sql_2 = f'insert into friend(userid,friendid,status) values({rs[0][0]},{userid},1)'
            if db.RunSQL(sql_1) and db.RunSQL(sql_2):
                return {'result': True, 'message': '请求发送成功'}
            else:
                return {'result': False, 'message': '请求发送失败'}
        else:
            sql_1 = f'update friend set status=-1 where userid={userid} and friendid={rs[0][0]}'
            sql_2 = f'update friend set status=1 where userid={rs[0][0]} and friendid={userid}'
            if db.RunSQL(sql_1) and db.RunSQL(sql_2):
                return {'result': True, 'message': '请求发送成功'}
            else:
                return {'result': False, 'message': '请求发送失败'}

    @staticmethod
    def getRequest(userid):
        sql = f'select * from user where id in (select friendid from friend where userid={userid} and status!=100)'
        rs = db.RunSQLReturnRS(sql)
        users = []
        index = 0
        for user in rs:
            users.append({
                'index':index,
                'id':user[0],
                'username':user[1]
            })
            index += 1
        return users

    @staticmethod
    def getFriend(userid):
        sql = f'select * from user where id in (select friendid from friend where userid={userid} and status=100)'
        rs = db.RunSQLReturnRS(sql)
        users = []
        index = 0
        for user in rs:
            users.append({
                'index': index,
                'id': user[0],
                'username': user[1]
            })
            index += 1
        return users

    @staticmethod
    def processFriend(userid,friendid,action):
        if userid is None and friendid is None and action is None:
            return {'result': False, 'message': '参数错误,请重试'}
        if action == 100:
            sql_1 = f'update friend set status=100 where userid={userid} and friendid={friendid}'
            sql_2 = f'update friend set status=100 where userid={friendid} and friendid={userid}'
            print(sql_1)
            print(sql_2)
            if db.RunSQL(sql_1) and db.RunSQL(sql_2):
                return {'result': True, 'message': '好友请求已接受'}
            else:
                return {'result': False, 'message': '接受失败,请重试'}
        elif action == 0:
            sql_1 = f'update friend set status=0 where userid={userid} and friendid={friendid}'
            if db.RunSQL(sql_1):
                return {'result': True, 'message': '已忽略'}
            else:
                return {'result': False, 'message': '忽略失败,请重试'}

        elif action == -100:
            sql_1 = f'update friend set status=-100 where userid={userid} and friendid={friendid}'
            sql_2 = f'update friend set status=-100 where userid={friendid} and friendid={userid}'
            if db.RunSQL(sql_1) and db.RunSQL(sql_2):
                return {'result': True, 'message': '已拒绝'}
            else:
                return {'result': False, 'message': '拒绝失败,请重试'}
