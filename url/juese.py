from flask import Flask,Blueprint,request,redirect
from sql import cursor,db
import json
juese=Blueprint('juese',__name__)

@juese.route('/jueseadd')
def jueseadd():
    juese=request.args.get('name')
    roots=request.args.get('roots')
    cursor.execute("insert into role (rname,rinfo) values(%s,%s)",(juese,roots))
    db.commit()
    return 'ok'
@juese.route('/selejuese')
def selejuese():
    cursor.execute("select * from role")
    result = cursor.fetchall()
    return json.dumps(result)
@juese.route("/deljuese")
def deljuese():
    rid=request.args.get('rid')
    cursor.execute("delete from role where rid=%s",rid)
    db.commit()
    cursor.execute("select * from role")
    result = cursor.fetchall()
    return json.dumps(result)
@juese.route("/editjuese")
def editjuese():
    rid=request.args.get('rid')
    name=request.args.get('name')
    root=request.args.get('roots')
    cursor.execute("update role set rname=%s,rinfo=%s where rid=%s",(name,root,rid))
    db.commit()
    print(rid,root,name)
    return "ok"