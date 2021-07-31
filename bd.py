import pymysql
 
con = pymysql.connect(host='localhost',
        user='root',
        password='',
        db='faces',
        charset='utf8mb4')
 
with con: 
    cur = con.cursor()
    cur.execute("insert into faces values (1,2,'2')")
    con.commit()