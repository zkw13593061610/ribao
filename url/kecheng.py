from flask import Blueprint,make_response,send_from_directory,request,jsonify,Flask
from sql import cursor,db
import json
import xlrd
import os

kecheng=Blueprint('kecheng',__name__)
app=Flask(__name__)

UPLOAD_FOLDER = 'upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
basedir = os.path.abspath(os.path.dirname(__file__))
ALLOWED_EXTENSIONS = set(['txt', 'png', 'jpg', 'xls', 'JPG', 'PNG', 'xlsx', 'gif', 'GIF'])

@kecheng.route("/download")
def download():
    res=make_response(send_from_directory('download','ribaomoban.xlsx',as_attachment=True))
    res.headers['content-disposition']='attachment;filename=kecheng.xlsx'
    return res
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS
@kecheng.route("/upload",methods=['POST'])
def upload():
    # file=request.files['file']
    # file.save('1.xlsx')
    # book=xlrd.open_workbook("1.xlsx")
    # sheet=book.sheet_by_index(0)
    file_dir = os.path.join(basedir, app.config['UPLOAD_FOLDER'])
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    f = request.files['file']  # 从表单的file字段获取文件，file为该表单的name值
    if f and allowed_file(f.filename):  # 判断是否是允许上传的文件类型
        # fname = secure_filename(f.filename)
        # ext = fname.rsplit('.', 1)[1]  # 获取文件后缀
        # unix_time = int(time.time())
        # new_filename = str(unix_time) + '.' + ext  # 修改了上传的文件名
        f.save(os.path.join(file_dir, 'kecheng.xlsx'))  # 保存文件到upload目录
        # token = base64.b64encode(new_filename)
        book = xlrd.open_workbook("url/upload/"+'kecheng.xlsx')
        sheet=book.sheet_by_index(0)
        arr = []
        for item in range(1, sheet.nrows):
            con = sheet.row_values(item)
            cursor.execute("insert into category (cname) values (%s)", con[0])
            cid = db.insert_id()
            step = con[1].split("\n")
            part = con[2].split("\n")
            for index in range(len(step)):
                arr.append((step[index], part[index], cid))
        cursor.executemany("insert into category_info (step,part,cid) values (%s,%s,%s)", (arr))
        db.commit()
        return 'ok'
    else:
        return jsonify({"errno": 1001, "errmsg": "上传失败"})
def chuli(con):
    arr=[]
    cursor.execute("insert into category (cname) values (%s)",con[0])
    cid = db.insert_id()
    step = con[1].split("\n")
    part = con[2].split("\n")
    for index in range(len(step)):
        arr.append((step[index],part[index],cid))
    cursor.executemany("insert into category_info (step,part,cid) values (%s,%s,%s)",(arr))
    db.commit()
# 添加单条课程信息
@kecheng.route("/addKCone")
def addKCone():
    file=request.args.get('file')
    file=json.loads(file)
    chuli(file)
    # print(file)
    return 'ok'
@kecheng.route("/seleFX")
def seleFX():
    cursor.execute("select * from category")
    result=cursor.fetchall()
    return json.dumps(result)
@kecheng.route("/selekecheng")
def selekecheng():
    id=request.args.get('cid')
    # cursor.execute("select * from category,category_info where category.cid=category_info.cid")
    # result = cursor.fetchall()
    cursor.execute("select * from category_info where cid=%s",id)
    result=cursor.fetchall()
    # print(result,type(result))
    return json.dumps(result)