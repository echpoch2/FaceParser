from fastapi import FastAPI, Request
import VK_parser
import pymysql
from pydantic import BaseModel 
from fastapi.encoders import jsonable_encoder
coordinator = VK_parser.VK_parser()
app = FastAPI()

@app.get("/")
def read_root():
    return coordinator.give_task()
@app.post("/done")
def counter(counter:int):
    for task in coordinator.tasks:
        print(task.counter, counter)
        if task.counter == counter:
            #f = open('dones.txt','w+')  # открытие в режиме записи
        #     f.write(str(task.counter)+" "+str(task.gender_status)+" "+str(task.month_status)+" "+str(task.day_status)+" "+str(task.years_status)+" "+str(task.city_status))
            #f.close()  # закрытие файла
            con = pymysql.connect(host='localhost',
                user='root',
                password='',
                db='faces',
                charset='utf8mb4')
            with con: 
                cur = con.cursor()
                cur.execute("update tasks set task_status='0' where counter="+str(counter))
                con.commit()
                coordinator.tasks.remove(task)
            print('Задача удалена! Список задач:',coordinator.tasks)

    return counter

