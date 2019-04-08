from flask import Blueprint,Flask,make_response,send_from_directory,request
import os
import hashlib
import pymysql
import xlrd
import json
from sql import cursor,db

students=Blueprint('students',__name__)

app=Flask(__name__)

UPLOAD_FOLDER = 'upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
basedir = os.path.abspath(os.path.dirname(__file__))
ALLOWED_EXTENSIONS = set(['txt', 'png', 'jpg', 'xls', 'JPG', 'PNG', 'xlsx', 'gif', 'GIF'])

@students.route('/down')
def down():
    res = make_response(send_from_directory('download', 'students.xlsx', as_attachment=True))
    res.headers['content-disposition'] = 'attachment;filename=students.xlsx'
    return res
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS
@students.route("/upload",methods=['POST'])
def upload():
    db1 = pymysql.connect(host="localhost",
                         user="root",
                         password="154303",
                         db="ribaoxitong",
                         charset="utf8")
    cursor1 = db1.cursor()
    cursor1.execute("select name,id from classes")
    classes=cursor1.fetchall()
    cursor1.close()
    db1.close()
    classes=dict(classes)
    # print(classes)
    file_dir = os.path.join(basedir, app.config['UPLOAD_FOLDER'])
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    f = request.files['file']  # 从表单的file字段获取文件，file为该表单的name值
    if f and allowed_file(f.filename):  # 判断是否是允许上传的文件类型
        f.save(os.path.join(file_dir, 'students.xlsx'))
        book = xlrd.open_workbook("url/upload/" + 'students.xlsx')
        sheet = book.sheet_by_index(0)
        user=[]
        stu=[]
        md5=hashlib.md5()
        md5.update(b'123456')
        pw=md5.hexdigest()
        for item in range(1, sheet.nrows):
            # print(sheet.row_values(item))
            con = (sheet.row_values(item))
            single_user=[str(con[0]),str(int(con[2])),pw,9]
            single_stu=[str(con[0]),int(con[2]),classes[str(int(con[1]))],con[3],con[4]]
            user.append(single_user)
            stu.append(single_stu)
        print(user,stu)
        cursor.executemany("insert into user (name,tel,pass,rid) values(%s,%s,%s,%s)", (user))
        cursor.executemany("insert into students (name,phone,classid,sex,school) values(%s,%s,%s,%s,%s)", (stu))
        db.commit()
        return 'ok'
@students.route('/seleclasses')
def seleclasses():
    cursor.execute("select id,name from classes")
    result = cursor.fetchall()
    db.commit()
    # print(result,type(result))
    for i in range(len(result)):
        result[i]['value']=result[i].pop('id')
        result[i]['label'] = result[i].pop('name')
        # result[i]['id']=result[i].pop('value')
        # result[i]['name']=result[i].pop('label')
    # print(result)
    return json.dumps(result)
@students.route("/findsame")
def findsame():
    phone=request.args.get('phone')
    cursor.execute('select * from user where tel=%s',phone)
    result=cursor.fetchone()
    if(result):
        return 'error'
    else:
        return 'ok'
@students.route("/insertOne")
def insertOne():
    name=request.args.get('name')
    tel=request.args.get('tel')
    school=request.args.get('school')
    sex=request.args.get('sex')
    banji=request.args.get('banji')
    rid='9'
    md5 = hashlib.md5()
    md5.update(b'123456')
    pswd = md5.hexdigest()
    cursor.execute("insert into user (name,tel,pass,rid) values(%s,%s,%s,%s)", (name,tel,pswd,rid))
    cursor.execute("insert into students (name,phone,classid,sex,school) values (%s,%s,%s,%s,%s)",(name,tel,banji,sex,school))
    db.commit()
    return 'ok'
@students.route("/seleAll")
def seleAll():
    db3 = pymysql.connect(host="localhost",
                          user="root",
                          password="123456",
                          db="ribao1",
                          cursorclass=pymysql.cursors.DictCursor,
                          charset="utf8")
    cursor3 = db3.cursor()
    cursor3.execute("select * from students ORDER BY id LIMIT 10")
    result=cursor3.fetchall()
    print(result)
    return json.dumps(result)