from flask import Flask,Blueprint,request
from sql import cursor,db
import json
roots=Blueprint('roots',__name__)

@roots.route('/selectroot')
def selectroot():
    cursor.execute("select * from role")
    result = cursor.fetchall()
    # print(result)
    return json.dumps(result)