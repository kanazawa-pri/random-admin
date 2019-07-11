from app.mysql_ import Mysql_
from app.dbutil import MysqlUtil
from app.cash_article import cash_article
import json
from flask import Flask,request
import schedule
import time

app = Flask(__name__)

@app.route('/cron_task', methods=['GET'])
def task():
    if request.method =='GET': 
        cash_article()
    return "cashed"

@app.route('/site', methods=['GET'])
def article_post():
    with MysqlUtil() as mysqlutil:
        mysql = Mysql_(mysqlutil)
        if request.method == 'GET':
            return json.dumps({'result':mysql.fetch_site_names()})

@app.route('/article',methods=['GET','POST'])
def history():
    with MysqlUtil() as mysqlutil:
        mysql = Mysql_(mysqlutil)
        if request.method == 'GET':
            print(request.args)
            return json.dumps({'result':mysql.fetch_article_for_user(request.args.get('user_id'),int(request.args.get('page')),request.args.get('ng_sites'))})
        elif request.method == 'POST':
            mysql.regist_user_history(int(request.json["user_id"]),int(request.json["article_id"]),int(request.json["is_later"]))
            mysqlutil.commit()
            return json.dumps({'result':'ok'})

if __name__ == '__main__':
    app.debug = True 
    app.run(host='0.0.0.0')
    
    


