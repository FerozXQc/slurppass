from fastapi import APIRouter
from database import db_addPass,db_deletePassLog,db_listPassLogs,db_getPassLog
from schemas import AddPassLog
passlog_router = APIRouter(tags=["passLog"])


@passlog_router.get('/listPassLogs')
def listPassLogs(user_id:str):
    result = db_listPassLogs(user_id)
    print(result)
    return result

@passlog_router.post('/addPassLog')
def addPassLog(passLog: AddPassLog):
    return db_addPass(user_id=passLog.user_id, title=passLog.title, desc=passLog.desc, passlog=passLog.passlog)

@passlog_router.delete('/deletePassLog')
def delPassLog(user_id:str, task_id:int):
    return db_deletePassLog(user_id,task_id)
