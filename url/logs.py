from flask import Blueprint,make_response,send_from_directory,request,jsonify,Flask
from sql import cursor,db
import json
import pymysql

logs=Blueprint('logs',__name__)

# 管理员查看日报
@logs.route('/searchAllLogs')
def searchAllLogs():
    KC = request.args.get("KC")
    banji = request.args.get("banji")
    times = request.args.get("date")
    clickpageNum =request.args.get("pagesNow")
    clickpageNum=int(clickpageNum)
    # print(clickpageNum)
    if (times=='NaN-NaN-NaN NaN:NaN:NaN'):
        times=''
    if (times=='1970-1-1 8:0:0'):
        times=''
    seleCon = ""
    if not times=='':
        # times = times[0:10]
        times = times.rsplit(" ")[0]
        # print(times)
    timecon = "where 1=1 AND date_format(logs.time,'%Y-%m-%d')='" + times + "'" if times else ""
    # print(timecon,type(timecon))
    if KC:
        seleCon = "where logs.phone in (select phone from students where classid in (select id from classes where cid in ('"+KC+"')))"
    if banji and not KC:
        seleCon = "where logs.phone in (select phone from students where classid= "+banji+")"
    if banji and KC:
        seleCon = "where logs.phone in (select phone from students where classid in (select id from classes where cid=%s and id=%s))" % (
     KC, banji)
    sql="select logs.*,students.name as sname,classes.name as cname from logs left join students on logs.phone=students.phone left join classes on students.classid=classes.id "+seleCon+" "+timecon+" ORDER BY id LIMIT "+str((clickpageNum-1)*3)+",3"
    cursor.execute(sql)
    result = cursor.fetchall()
    return json.dumps(result,default=str)
@logs.route('/searchAllLogsGAI')
def searchAllLogsGAI():
    db44 = pymysql.connect(host="localhost",
                           user="root",
                           password="154303",
                           db="ribaoxitong",
                           cursorclass=pymysql.cursors.DictCursor,
                           charset="utf8")
    cursor44 = db44.cursor()
    KC = request.args.get("KC")
    banji = request.args.get("banji")
    times = request.args.get("date")
    if (times=='NaN-NaN-NaN NaN:NaN:NaN'):
        times=''
    if (times=='1970-1-1 8:0:0'):
        times=''
    seleCon = ""
    if not times=='':
        times = times.rsplit(" ")[0]
    timecon = "where 1=1 AND date_format(logs.time,'%Y-%m-%d')='" + times + "'" if times else ""
    if KC:
        seleCon = "where logs.phone in (select phone from students where classid in (select id from classes where cid in ('"+KC+"')))"
    if banji and not KC:
        seleCon = "where logs.phone in (select phone from students where classid= "+banji+")"
    if banji and KC:
        seleCon = "where logs.phone in (select phone from students where classid in (select id from classes where cid=%s and id=%s))" % (
     KC, banji)
    sql="select logs.*,students.name as sname,classes.name as cname from logs left join students on logs.phone=students.phone left join classes on students.classid=classes.id "+seleCon+" "+timecon
    cursor44.execute(sql)
    result = cursor44.fetchall()
    return json.dumps(result,default=str)
# 查看日报总数量
@logs.route("/selelen")
def selelen():
    db33 = pymysql.connect(host="localhost",
                         user="root",
                         password="154303",
                         db="ribaoxitong",
                         cursorclass=pymysql.cursors.DictCursor,
                         charset="utf8")
    cursor33 = db33.cursor()
    cursor33.execute("select logs.*,students.name as sname,classes.name as cname from logs left join students on logs.phone=students.phone left join classes on students.classid=classes.id where 1=1")
    result=cursor33.fetchall()
    # print(len(result))
    return json.dumps(result,default=str)
# 管理员查看日报，分页处理
@logs.route("/selelogs")
def selelogs():
    db22 = pymysql.connect(host="localhost",
                         user="root",
                         password="154303",
                         db="ribaoxitong",
                         cursorclass=pymysql.cursors.DictCursor,
                         charset="utf8")
    cursor22 = db22.cursor()
    cursor22.execute("select logs.*,students.name as sname,classes.name as cname from logs left join students on logs.phone=students.phone left join classes on students.classid=classes.id where 1=1 ORDER BY id LIMIT 3")
    result=cursor22.fetchall()
    # print(len(result))
    return json.dumps(result,default=str)
# 学生提交日报处理
@logs.route("/tijiaoribao",methods=["POST"])
def tijiaoribao():
    ZYM=request.form['ZYM']
    xinde=request.form['XinDe']
    yijian=request.form['YiJian']
    qita=request.form['QiTa']
    con=request.form['con']
    phone='20181116996'
    print(type(con),con)
    cursor.execute("insert into logs (phone,zym,workspace,yijian,xinde,qita) values (%s,%s,%s,%s,%s,%s)",(phone,ZYM,con,yijian,xinde,qita))
    db.commit()
    return 'ok'
@logs.route("/ShowLog")
def ShowLog():
    id=request.args.get("id")
    cursor.execute("select * from logs where id=%s",id)
    result=cursor.fetchone()
    return json.dumps(result,default=str)