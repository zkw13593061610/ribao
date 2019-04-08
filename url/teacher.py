from flask import Blueprint,Flask,make_response,send_from_directory,request
import pymysql
import os
import hashlib
import xlrd
import json
from sql import cursor,db

teacher=Blueprint('teacher',__name__)

app=Flask(__name__)

UPLOAD_FOLDER = 'upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
basedir = os.path.abspath(os.path.dirname(__file__))
ALLOWED_EXTENSIONS = set(['txt', 'png', 'jpg', 'xls', 'JPG', 'PNG', 'xlsx', 'gif', 'GIF'])

@teacher.route('/down')
def down():
    res = make_response(send_from_directory('download', 'teacher.xlsx', as_attachment=True))
    res.headers['content-disposition'] = 'attachment;filename=teacher.xlsx'
    return res
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS
@teacher.route("/upload",methods=['POST'])
def upload():
    db1 = pymysql.connect(host="localhost",
                         user="root",
                         password="154303",
                         db="ribaoxitong",
                         charset="utf8")
    cursor1 = db1.cursor()
    cursor1.execute("select name,id from classes")
    classes=cursor1.fetchall()
    db1.commit()
    classes=dict(classes)
    cursor1.execute("select cname,cid from category")
    kecheng = cursor1.fetchall()
    kecheng=dict(kecheng)
    cursor1.close()
    db1.close()
    file_dir = os.path.join(basedir, app.config['UPLOAD_FOLDER'])
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    f = request.files['file']  # 从表单的file字段获取文件，file为该表单的name值
    if f and allowed_file(f.filename):  # 判断是否是允许上传的文件类型
        f.save(os.path.join(file_dir, 'teachers.xlsx'))
        book = xlrd.open_workbook("url/upload/" + 'teachers.xlsx')
        sheet = book.sheet_by_index(0)
        user=[]
        tea=[]
        md5=hashlib.md5()
        md5.update(b'123456')
        pw=md5.hexdigest()
        for item in range(1, sheet.nrows):
            # print(sheet.row_values(item))
            con = (sheet.row_values(item))
            single_user=[str(con[0]),str(int(con[1])),pw,10]
            single_tea=[str(con[0]),int(con[1]),kecheng[str(con[2]).upper()],classes[str(con[3]).upper()]]
            user.append(single_user)
            tea.append(single_tea)
        cursor.executemany("insert into user (name,tel,pass,rid) values(%s,%s,%s,%s)", (user))
        cursor.executemany("insert into teacher (name,phone,cid,classid) values(%s,%s,%s,%s)", (tea))
        db.commit()
        return 'ok'
@teacher.route('/seleclasses')
def seleclasses():
    cursor.execute("select id,name from classes")
    result = cursor.fetchall()
    db.commit()
    for i in range(len(result)):
        result[i]['value']=str(result[i].pop('id'))
        result[i]['label'] = result[i].pop('name')
    return json.dumps(result)
@teacher.route('/seleKC')
def seleKC():
    cursor.execute("select cid,cname from category")
    result = cursor.fetchall()
    db.commit()
    for i in range(len(result)):
        # print(result[i])
        result[i]['value']=str(result[i].pop('cid'))
        result[i]['label'] = result[i].pop('cname')
    return json.dumps(result)
@teacher.route("/findsame")
def findsame():
    phone=request.args.get('phone')
    cursor.execute('select * from user where tel=%s',phone)
    result=cursor.fetchone()
    db.commit()
    if(result):
        return 'error'
    else:
        return 'ok'
@teacher.route("/insertOne")
def insertOne():
    name=request.args.get('name')
    tel=request.args.get('tel')
    banji=request.args.get('banji')
    FX=request.args.get('FX')
    name = name.upper()
    rid = '10'
    md5 = hashlib.md5()
    md5.update(b'123456')
    pswd = md5.hexdigest()
    cursor.execute("insert into user (name,tel,pass,rid) values(%s,%s,%s,%s)", (name, tel, pswd, rid))
    cursor.execute("insert into teacher (name,phone,cid,classid) values(%s,%s,%s,%s)",(name,tel,FX,banji))
    db.commit()
    return 'ok'
@teacher.route("/seleKCS")
def seleKCS():
    cursor.execute("select * from category")
    result=cursor.fetchall()
    return json.dumps(result)
@teacher.route("/seleClasses")
def seleClasses():
    cid=request.args.get('cid')
    cursor.execute("select * from teacher where cid=%s",cid)
    result1=cursor.fetchall()
    db.commit()
    for i in range(len(result1)):
        id=result1[i]['classid']
        cursor.execute("select name,id from classes where id=%s", id)
        result2 = cursor.fetchone()
        result1[i]['banjiID'] = result2['id']
        result1[i]['classid']=result2['name']
    # print(result1)
    return json.dumps(result1)
@teacher.route("/updateOne")
def updateOne():
    id=request.args.get('id')
    name = request.args.get('name')
    phone = request.args.get('tel')
    banji = request.args.get('banji')
    FX = request.args.get('FX')
    # print(id,name,phone,banji,FX)
    # name = name.upper()
    print(name,phone,id)
    cursor.execute("select * from user where tel=%s",phone)
    result=cursor.fetchone()
    tid=result['id']
    print(tid)
    cursor.execute("update teacher set name=%s,phone=%s,cid=%s,classid=%s where id=%s",
                   (name, phone, FX, banji, id))
    cursor.execute("update user set name=%s,tel=%s where id=%s", (name, phone, tid))
    db.commit()
    return 'ok'
@teacher.route("/deleTea")
def deleTea():
    phone=request.args.get("phone")
    cursor.execute("delete from teacher where phone=%s",phone)
    cursor.execute("delete from user where tel=%s", phone)
    db.commit()
    cid = request.args.get('cid')
    cursor.execute("select * from teacher where cid=%s", cid)
    result1 = cursor.fetchall()
    for i in range(len(result1)):
        id = result1[i]['classid']
        cursor.execute("select name,id from classes where id=%s", id)
        result2 = cursor.fetchone()
        result1[i]['banjiID'] = result2['id']
        result1[i]['classid'] = result2['name']
    db.commit()
    return json.dumps(result1)