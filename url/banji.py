from flask import Blueprint,request,make_response,send_from_directory,Flask
import pymysql
import os
import xlrd
import time
import datetime
from sql import cursor,db
import json

banji=Blueprint("banji",__name__)

app=Flask(__name__)

UPLOAD_FOLDER = 'upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
basedir = os.path.abspath(os.path.dirname(__file__))
ALLOWED_EXTENSIONS = set(['txt', 'png', 'jpg', 'xls', 'JPG', 'PNG', 'xlsx', 'gif', 'GIF'])

@banji.route("/download")
def download():
    res=make_response(send_from_directory('download','banji.xlsx',as_attachment=True))
    res.headers['content-disposition']='attachment;filename=banji.xlsx'
    return res
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS
@banji.route("/upload",methods=['POST'])
def upload():
    db1 = pymysql.connect(host="localhost",
                         user="root",
                         password="154303",
                         db="ribaoxitong",
                         charset="utf8")
    cursor1 = db1.cursor()
    cursor1.execute("select cname,cid from category")
    category=cursor1.fetchall()
    cursor1.close()
    db1.close()
    # print(category)
    category=dict(category)
    # print(category)
    file_dir = os.path.join(basedir, app.config['UPLOAD_FOLDER'])
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    f = request.files['file']  # 从表单的file字段获取文件，file为该表单的name值
    if f and allowed_file(f.filename):  # 判断是否是允许上传的文件类型
        # fname = secure_filename(f.filename)
        # ext = fname.rsplit('.', 1)[1]  # 获取文件后缀
        # unix_time = int(time.time())
        # new_filename = str(unix_time) + '.' + ext  # 修改了上传的文件名
        f.save(os.path.join(file_dir, 'banji.xlsx'))
        book = xlrd.open_workbook("url/upload/" + 'banji.xlsx')
        sheet = book.sheet_by_index(0)
        shit = []
        for item in range(1, sheet.nrows):
            # print(sheet.row_values(item))
            arr=(sheet.row_values(item))
            # arr[0]=int(arr[0])
            arr[1]=category[arr[1]]
            arr[2]=xlrd.xldate_as_datetime(arr[2],0).strftime("%Y-%m-%d %H:%M:%S")
            arr[3]=xlrd.xldate_as_datetime(arr[3],0).strftime("%Y-%m-%d %H:%M:%S")
            # print(arr[0],arr[1],arr[2],arr[3])
            shit.append((arr[0],arr[2],arr[3],arr[1]))
        # print(shit)
        cursor.executemany("insert into classes (name,start,end,cid) values(%s,%s,%s,%s)", (shit))
        db.commit()
        return 'ok'
@banji.route("/selecategory")
def selecategory():
    cid=request.args.get('cid')
    cursor.execute("select * from category where cid=%s",cid)
    result=cursor.fetchone()
    print(result)
    return json.dumps(result)
@banji.route("/insertone")
def insertone():
    name = request.args.get('name')
    start = request.args.get('start')
    end = request.args.get('ends')
    cid = request.args.get('cid')
    name=name.upper()
    cursor.execute("insert into classes (name,start,end,cid) values (%s,%s,%s,%s)",(name,start,end,cid))
    db.commit()
    return 'ok'
@banji.route("/seleKC")
def seleKC():
    cursor.execute("select * from category")
    result=cursor.fetchall()
    return json.dumps(result)
@banji.route("/seleClasses")
def seleClasses():
    cid=request.args.get('cid')
    cursor.execute("select * from classes where cid=%s",cid)
    result=cursor.fetchall()
    return json.dumps(result,default=str)
@banji.route("/updateOne")
def updateOne():
    id=request.args.get('id')
    name = request.args.get('name')
    start = request.args.get('start')
    end = request.args.get('ends')
    cid = request.args.get('cid')
    name = name.upper()
    # print(id,name,start,end,cid)
    cursor.execute("update classes set name=%s,start=%s,end=%s,cid=%s where id=%s",
                   (name, start, end, cid, id))
    db.commit()
    return 'ok'
@banji.route("/seleKCS")
def seleKCS():
    cursor.execute("select cid,cname from category")
    result = cursor.fetchall()
    db.commit()
    for i in range(len(result)):
        # print(result[i])
        result[i]['value'] = str(result[i].pop('cid'))
        result[i]['label'] = result[i].pop('cname')
    return json.dumps(result)
