from flask import Flask,Blueprint,request
from sql import cursor,db
import json
import hashlib
users=Blueprint('users',__name__)

# @users.route("/addusers",methods=['POST'])
# def addusers():
#     username = request.form['uname']
#     usertel = request.form['utel']
#     userpass = request.form['upass']
#     md5 = hashlib.md5()
#     md5.update(userpass.encode('utf8'))
#     userpass = md5.hexdigest()
#     roots = request.form['roots']
#     print(userpass,usertel,username,roots)
#     cursor.execute('select rid from role where rinfo=%s',roots)
#     result=cursor.fetchone()
#     roots=result['rid']
#     cursor.execute("insert into user (name,tel,pass,rid) values(%s,%s,%s,%s)",(username,usertel,userpass,roots))
#     db.commit()
#     return 'ok'
@users.route("/seleuser")
def seleuser():
    # cursor.execute("select * from user,role where user.rid=role.rid")
    # result = cursor.fetchall()
    # lis=[]
    # root=[]
    # for item in result:
    #     lis.append(item['rid'])
    # for rid in lis:
    #     cursor.execute("select rname from role where rinfo=%s",rid)
    #     roots=cursor.fetchone()
    #     root.append(roots)
    # for index in range(len(lis)):
    #     result[index]['rname']=root[index]['rname']
    # return json.dumps(result)
    cursor.execute("select * from user,role where user.rid=role.rid")
    result=cursor.fetchall()
    results=json.dumps(result)
    return results
@users.route("/deluser")
def deluser():
    id=request.args.get('id')
    cursor.execute("delete from user where id=%s",id)
    db.commit()
    cursor.execute("select * from user")
    result = cursor.fetchall()
    return json.dumps(result)
@users.route("/updausers",methods=['POST'])
def updausers():
    uid = request.form["uid"]
    username = request.form['uname']
    usertel = request.form['utel']
    userpass = request.form['upass']
    md5 = hashlib.md5()
    md5.update(userpass.encode('utf8'))
    userpass = md5.hexdigest()
    roots = request.form['roots']
    cursor.execute('select rid from role where rinfo=%s', roots)
    result = cursor.fetchone()
    roots = result['rid']
    cursor.execute("update user set name=%s,tel=%s,pass=%s,rid=%s where id=%s",(username,usertel,userpass,roots,uid))
    db.commit()
    return 'ok'
@users.route("/seleYH")
def seleclasses():
    cursor.execute("select rinfo,rname from role")
    result=cursor.fetchall()
    for i in range(len(result)):
        result[i]['value']=result[i].pop('rinfo')
        result[i]['label'] = result[i].pop('rname')
    return json.dumps(result)
@users.route("/insertOne")
def insertOne():
    name=request.args.get("name")
    tel=request.args.get("tel")
    pswd=request.args.get("pass")
    md5 = hashlib.md5()
    md5.update(pswd.encode('utf8'))
    pswd = md5.hexdigest()
    roots=request.args.get("YH")
    cursor.execute('select rid from role where rinfo=%s', roots)
    result = cursor.fetchone()
    roots = result['rid']
    cursor.execute("insert into user (name,tel,pass,rid) values(%s,%s,%s,%s)", (name, tel, pswd, roots))
    db.commit()
    return 'ok'
@users.route("/updateOne")
def updateOne():
    uid = request.args.get("uid")
    name = request.args.get('name')
    tel = request.args.get('tel')
    pswd = request.args.get('pass')
    roots = request.args.get("YH")
    # uid = request.form['id']
    # name=request.form['name']
    # tel=request.form['tel']
    # pswd=request.form['pass']
    # roots=request.form['roots']
    md5 = hashlib.md5()
    md5.update(pswd.encode('utf8'))
    pswd = md5.hexdigest()
    cursor.execute('select rid from role where rinfo=%s', roots)
    result = cursor.fetchone()
    roots = result['rid']
    # print(uid,name,tel,pswd,roots)
    cursor.execute("update user set name=%s,tel=%s,pass=%s,rid=%s where id=%s",
                   (name, tel, pswd, roots, uid))
    db.commit()
    return 'ok'
