import time
import pymysql
class Task:
    def __init__(self,counter=0,gender=0,month=0,day=0,years=0,city=0):
        self.time = time.time()
        self.counter=counter
        self.gender_status=gender
        self.month_status=month
        self.day_status=day
        self.years_status=years
        self.city_status=city
class VK_parser:
    def __init__(self):
        self.counter_status=0
        self.start_age = 14
        self.end_age = 75
        self.cities = [282]
        self.gender_status = 1
        self.month_status = 1
        self.day_status=0
        self.years_status = 20
        self.city_status = self.cities[0]
        self.tasks = []
    def give_task(self):
        for task in self.tasks:
            if(time.time()-task.time>3600):
                return {"counter":task.counter,"city": task.city_status, "month": task.month_status, "day":task.day_status,"gender":task.gender_status,"years":task.years_status}
        if self.day_status == 31:
            self.day_status=1
            if self.month_status == 12:
                self.month_status=1
                if self.gender_status == 2:
                    self.gender_status = 1
                    if self.years_status == self.end_age:
                        return {"info":"done"}
                    else:
                        self.years_status+=1
                else:
                    self.gender_status+=1
            else: self.month_status+=1
        else:
            self.day_status+=1
        self.counter_status+=1
        self.tasks.append(Task(self.counter_status, self.gender_status, self.month_status, self.day_status,self.years_status,self.city_status))
        con = pymysql.connect(host='localhost',
                user='root',
                password='',
                db='faces',
                charset='utf8mb4')
        with con: 
            cur = con.cursor()
            cur.execute("insert into tasks (counter, gender_status, month_status, day_status, years_status,city_status,task_status) values ("+str(self.counter_status)+","+str(self.gender_status)+","+str(self.month_status)+","+ str(self.day_status)+","+str(self.years_status)+","+str(self.city_status)+",1)")
            con.commit()
        print('New task! List of tasks:', self.tasks)

        return {"counter":self.counter_status,"city": self.city_status, "month": self.month_status, "day":self.day_status,"gender":self.gender_status,"years":self.years_status}


