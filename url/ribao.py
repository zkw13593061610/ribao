from flask import Flask,Blueprint,request
from sql import cursor,db
import json
ribao=Blueprint('ribao',__name__)

@ribao.route("/tijiaoribao",methods=['POST'])
def tijiaoribao():
    neirong=request.form['neirong']
    finish=request.form['finish']
    wenti=request.form['wenti']
    xinde=request.form['xinde']
    yijian=request.form['yijian']
    qita=request.form['qita']
    print(neirong,finish,wenti,xinde,yijian,qita)
    return 'ok'