import pymysql
db = pymysql.connect(host="localhost",
                     user="root",
                     password="123456",
                     db="ribao1",
                     cursorclass=pymysql.cursors.DictCursor,
                     charset="utf8")
cursor = db.cursor()