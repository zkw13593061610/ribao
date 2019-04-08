from flask import Blueprint,request
from sql import cursor,db
import json

exam=Blueprint('exam',__name__)

@exam.route("/down")
def down():
    return 'ok'
@exam.route("/seleJD")
def seleJD():
    cid=request.args.get("cid")
    cid=int(cid)
    cursor.execute("select id,step from category_info where cid=%s",cid)
    result=cursor.fetchall()
    for i in range(len(result)):
        result[i]['value']=result[i].pop('id')
        result[i]['label'] = result[i].pop('step')
    return json.dumps(result)
@exam.route("/addDanxuan")
def addDanxuan():
    FX=request.args.get("FX")
    JD=request.args.get("JD")
    TiXing=request.args.get("TiXing")
    TiGan=request.args.get("TiGan")
    daan=request.args.get("daan")
    choice=request.args.get("choice")
    score=request.args.get("score")
    print(FX,JD,TiGan,TiXing,choice,daan)
    cursor.execute("insert into shiti (tigan,xuanxiang,daan,types,fangxiang,jieduan,score) values(%s,%s,%s,%s,%s,%s,%s)",(TiGan,choice,daan,TiXing,FX,JD,score))
    db.commit()
    return 'ok'
@exam.route("/addDuoxuan")
def addDuoxuan():
    FX=request.args.get("FX")
    JD=request.args.get("JD")
    TiXing=request.args.get("TiXing")
    TiGan=request.args.get("TiGan")
    daan=request.args.get("daan")
    choice=request.args.get("choice")
    score=request.args.get("score")
    print(FX,JD,TiGan,TiXing,choice,daan)
    cursor.execute("insert into shiti (tigan,xuanxiang,daan,types,fangxiang,jieduan,score) values(%s,%s,%s,%s,%s,%s,%s)",(TiGan,choice,daan,TiXing,FX,JD,score))
    db.commit()
    return 'ok'
@exam.route("/findPro")
def findPro():
    FX=request.args.get("FX")
    JD=request.args.get("JD")
    TX=request.args.get("TX")
    cursor.execute("select id,tigan,xuanxiang,daan,score from shiti where types=%s and fangxiang=%s and jieduan=%s",(TX,FX,JD))
    result=cursor.fetchall()
    for item in range(len(result)):
        if len(result[item]['daan'])>20:
            result[item]['daan']=result[item]['daan'][:20]
    return json.dumps(result)
@exam.route("/addJianda")
def addJianda():
    FX=request.args.get("FX")
    JD=request.args.get("JD")
    TiXing=request.args.get("TiXing")
    TiGan=request.args.get("TiGan")
    daan=request.args.get("daan")
    score=request.args.get("score")
    cursor.execute("insert into shiti (tigan,daan,types,fangxiang,jieduan,score) values(%s,%s,%s,%s,%s,%s)",(TiGan,daan,TiXing,FX,JD,score))
    db.commit()
    return 'ok'
@exam.route("/makeShijuan")
def makeShijuan():
    FX=request.args.get("FX")
    JD=request.args.get("JD")
    TX=request.args.get("TX")
    Pid=request.args.get("pid")
    cursor.execute("insert into shijuan (fx,jd,tx,pid) values (%s,%s,%s,%s)",(FX,JD,TX,Pid))
    db.commit()
    print(FX,JD,TX,Pid)
    return 'ok'
@exam.route("/uppShijuan")
def uppShijuan():
    FX=request.args.get("FX")
    JD=request.args.get("JD")
    TX=request.args.get("TX")
    Pid=request.args.get("pid")
    print(FX,JD,TX,Pid)
    cursor.execute("update shijuan set pid=%s where fx=%s and jd=%s and tx=%s",(Pid,FX,JD,TX))
    db.commit()
    return 'ok'


