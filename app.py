from flask import Flask,render_template,request,redirect,session,make_response,send_from_directory,jsonify
import math
import pymysql
from werkzeug.utils import secure_filename
import os
import time
import json
from sql import cursor,db
from flask_session import Session
from url.students import students
from url.users import users
from url.juese import juese
from url.roots import roots
from url.ribao import ribao
from url.kecheng import kecheng
from url.banji import banji
from url.teacher import teacher
from url.logs import logs
from yanzhengma import code
from url.exam import exam


import json
import hashlib

app=Flask(__name__)
# UPLOAD_FOLDER = 'upload'
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# basedir = os.path.abspath(os.path.dirname(__file__))
# ALLOWED_EXTENSIONS = set(['txt', 'png', 'jpg', 'xls', 'JPG', 'PNG', 'xlsx', 'gif', 'GIF'])
debug = False
app.register_blueprint(users,url_prefix='/ajax/users')
app.register_blueprint(juese,url_prefix='/ajax/juese')
app.register_blueprint(roots,url_prefix='/ajax/roots')
app.register_blueprint(ribao,url_prefix='/ajax/ribao')
app.register_blueprint(kecheng,url_prefix='/ajax/kecheng')
app.register_blueprint(students,url_prefix='/ajax/students')
app.register_blueprint(banji,url_prefix='/ajax/banji')
app.register_blueprint(teacher,url_prefix='/ajax/teacher')
app.register_blueprint(logs,url_prefix='/ajax/logs')
app.register_blueprint(exam,url_prefix='/ajax/exam')

app.secret_key='123456'
# app.config["SESSION_FILE_DIR"]='F:\My Files\ShiYiYue\logs'
app.config['SESSION_PERMANENT'] = True  # 如果设置为True，则关闭浏览器session就失效。
app.config['SESSION_TYPE']='filesystem'
Session(app)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('login.html'), 404
# @app.before_request
# def before_request():
#     if request.path!=('/delu') and request.path!=("/yanzheng"):
#         if request.path!=('/login'):
#             if session.get('name')!='yes':
#                 return redirect("/login")
@app.route("/")
def home():
    if(session.get("login")=="yes"):
        res = make_response(render_template("index.html"))
        return res
    else:
        return redirect("/login")
@app.route("/yanzheng")
def yanzheng():
    codeobj = code()
    skt = make_response(codeobj.output())
    session['code'] = codeobj.arr
    # print(codeobj.arr)
    skt.headers["content-type"]="image/png"
    return skt
# 跳转至登录页面
@app.route("/login")
def login():
    return render_template("login.html")
# 登录处理程序
@app.route("/delu",methods=['POST'])
def delu():
    tel=request.form['tel']
    pswd=request.form['userpass']
    code=request.form['code']
    # print(code,session.get("code"))
    if code!=session.get("code"):
        return redirect("/login")
    md5 = hashlib.md5()
    md5.update(pswd.encode('utf8'))
    pswd = md5.hexdigest()
    cursor.execute("select * from user where tel=%s and pass=%s",(tel,pswd))
    result = cursor.fetchone()
    print(tel,pswd)
    if(result):
        res = make_response(redirect('/'))
        res.set_cookie('gg',str(result['rid']))
        session['login'] = 'yes'
        session['name'] = result['name']
        session['rid'] = result['rid']
        session['tel'] = result['tel']
        return res
    else:
        return redirect("/login")
# 退出
@app.route("/ajax/tuichu")
def tuichu():
    session.pop('login', None)
    session.pop('name', None)
    session.pop('rid', None)
    session.pop('tel', None)
    return redirect('/login')
@app.route('/ajax/seleitems')
def seleitems():
    items=request.cookies.get("gg")
    cursor.execute('select rinfo from role where rid=%s',items)
    result=cursor.fetchone()
    return json.dumps(result['rinfo'])
    # items="1|2|5|3|6|4|8|9|7"
    # return json.dumps(items)
@app.route('/ajax/welname')
def welname():
    name=session.get("name")
    return json.dumps(name)
@app.route('/ajax/classname')
def classname():
    phone=session.get("tel")
    cursor.execute("SELECT name FROM `classes` WHERE id in (SELECT classid FROM students WHERE phone=%s)", phone)
    res = cursor.fetchone()
    # print(res['name'])
    return json.dumps(res['name'])
@app.route('/ajax/logsWriter')
def logsWriter():
    rid=session.get("rid")
    # rid='9'
    return json.dumps(rid)
@app.route('/ajax/logs')
def logs():
    url = ''
    logsType = int(session.get("rid"))
    # logsType = 3
    if (logsType==3):
        url = '/logs_rooter'
    if(logsType==9):
        url = '/logs_stu'
    if (logsType==10):
        url = '/logs_tea'
    # print(1111)
    return json.dumps(url)
@app.route("/ajax/seleJD")
def seleJD():
    tel=session.get('tel')
    db1 = pymysql.connect(host="localhost",
                          user="root",
                          password="154303",
                          db="ribaoxitong",
                          cursorclass=pymysql.cursors.DictCursor,
                          charset="utf8")
    cursor1 = db1.cursor()
    cursor1.execute("select * from students where phone=%s",tel)
    result1=cursor1.fetchone()
    classid=result1['classid']
    # print(classid)
    session['classid'] = result1['classid']
    db2 = pymysql.connect(host="localhost",
                          user="root",
                          password="123456",
                          db="ribao1",
                          cursorclass=pymysql.cursors.DictCursor,
                          charset="utf8")
    cursor2 = db2.cursor()
    cursor2.execute("select cid from classes where id=%s", classid)
    result2 = cursor2.fetchone()
    cid = result2['cid']
    # cid = 3
    # session['classid'] = 3
    session['classid'] = cid
    cursor.execute("select id,step from category_info where cid=%s",cid)
    result=cursor.fetchall()
    for i in range(len(result)):
        result[i]['value']=result[i].pop('id')
        result[i]['label'] = result[i].pop('step')
    return json.dumps(result)
@app.route("/ajax/seleClassid")
def seleClassid():
    classid=session.get('classid')
    return json.dumps(classid)
@app.route("/ajax/ShiTi")
def ShiTi():
    JD=request.args.get('JD')
    FX=request.args.get('FX')
    db1 = pymysql.connect(host="localhost",
                          user="root",
                          password="123456",
                          db="ribao1",
                          cursorclass=pymysql.cursors.DictCursor,
                          charset="utf8")
    cursor1 = db1.cursor()
    cursor1.execute("select pid from shijuan where fx=%s and jd=%s",(FX,JD))
    res=cursor1.fetchall()
    str1=''
    pid=[]
    for item in range(len(res)):
        str1+=res[item]['pid']+','
        pid.append(res[item]['pid'])
    str1=str1[0:-1]
    pid=str1.split(",")
    # cursor.execute("select * from shiti where fangxiang=%s and jieduan=%s",(FX,JD))
    cursor.execute("select * from shiti where id=%s or id=%s or id=%s or id=%s or id=%s or id=%s or id=%s",(pid[0],pid[1],pid[2],pid[3],pid[4],pid[5],pid[6]))
    result=cursor.fetchall()
    db.commit()
    # print(result)
    return json.dumps(result)
@app.route("/ajax/findDXid")
def findDXid():
    JD = request.args.get('JD')
    FX = request.args.get('FX')
    types = 1
    # print(JD,FX,types)
    cursor.execute("select id from shiti where fangxiang=%s and jieduan=%s and types=%s", (FX,JD,types))
    result=cursor.fetchall()
    # print(result)
    return json.dumps(result)
def pages(total,pageNum):
    if request.url.find("?")<0:
        url=request.url+"?page="
    else:
        if request.url.rfind("page")<0:
            url=request.url+"&page="
        else:
            url=request.url[0:request.url.rfind("=")+1]
    pageNums=math.ceil(total/pageNum)
    currentpage=int(request.args.get('page') or 0)
    pagestr=''
    pagestr+='共%s页'%(pageNums)
    pagestr+="<a href='%s'>首页</a>"%(url+'0')
    last=currentpage-1 if currentpage-1>0 else 0
    pagestr+="<a href='%s'>上一页</a>"(url+str(last))
    start=currentpage-2 if currentpage-2>0 else 0
    end=start+4 if start+2<pageNums else pageNums
    for item in range(start,end+1):
        if currentpage==item:
            pagestr+="<a href='%s'>[%s]</a>"%(url+str(item),item+1)
    next=currentpage+1 if currentpage+1<pageNums else pageNums-1
    pagestr += "<a href='%s'>下一页</a>"(url + str(next))
    pagestr+="<a href='%s'>尾页</a>"%(url+str(pageNums-1))
    limit="limit"+str(currentpage*pageNum+','+str(pageNum))
    return {"pagestr":pagestr,"limit":limit}


if __name__ == '__main__':
    app.run()