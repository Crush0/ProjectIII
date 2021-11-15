import datetime
import time

from utils.DBUnitls import DBHelper as db

class MessageService:
    @staticmethod
    def get_messageNear(fromId,toId):
        sql = f'select id,msg,send_time,uuid,`from`,`to` from message where (`from`={fromId} and `to` = {toId}) or (`from`={toId} and `to` = {fromId}) and DATEDIFF(\'{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}\',send_time)<=1 order by send_time'
        rs = db.RunSQLReturnRS(sql)
        messages = []
        for msg in rs:
            sql = f'select username from user where id={fromId}'
            user = db.RunSQLReturnRS(sql)
            messages.append({
                'id':msg[0],
                'from':msg[4],
                'to':msg[5],
                'username':user[0][0],
                'message':msg[1],
                'uuid':msg[3],
                'time':datetime.datetime.strftime(msg[2], '%Y-%m-%d %H:%M:%S')
            })
        return messages

    @staticmethod
    def sendMsg(fromId,toId,msg,uuid):
        sql = 'insert into message(`from`,`to`,msg,send_time,uuid) values({},{},\'{}\',\'{}\',\'{}\')'.format(fromId,toId,msg.replace('\n',''),datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S'),uuid)
        if db.RunSQL(sql):
            return {'result':True}
        else:
            return {'result': False,'message':'消息发送失败'}