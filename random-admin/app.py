from chalicelib.mysql_ import Mysql_
from chalicelib.dbutil import MysqlUtil
from chalicelib.cash_article import cash_article
import json
from chalice import Chalice

app = Chalice(app_name="random_api")
@app.route('/', methods=['GET','POST'])
def article_post():
     with MysqlUtil() as mysqlutil:
        mysql = Mysql_(mysqlutil)
        if request.method == 'GET':
            return json.dumps({'result':mysql.fetch_sites()})
        elif request.method == 'POST':
            print(request.json)
            return json.dumps(mysql.fetch_article_for_user(request.json["user_id"],request.json['ng_site_list'],request.json['ng_word_list']))

@app.route('/history',methods=['GET','POST'])
def history():
    with MysqlUtil() as mysqlutil:
        mysql = Mysql_(mysqlutil)
        if request.method == 'GET':
            return json.dumps(mysql.fetch_user_history(request.args.get('user_id'),True))
        elif request.method == 'POST':
            print(request.json)
            mysql.regist_user_history(request.json["user_id"],request.json["article_id"],request.json["is_later"])
            mysqlutil.commit()
            return

@app.schedule('rate(1 hour)')
def rate_handler(event):
    cash_article()
    return "OK"
    
    


# The view function above will return {"hello": "world"}
# whenever you make an HTTP GET request to '/'.
#
# Here are a few more examples:
#
# @app.route('/hello/{name}')
# def hello_name(name):
#    # '/hello/james' -> {"hello": "james"}
#    return {'hello': name}
#
# @app.route('/users', methods=['POST'])
# def create_user():
#     # This is the JSON body the user sent in their POST request.
#     user_as_json = app.current_request.json_body
#     # We'll echo the json body back to the user in a 'user' key.
#     return {'user': user_as_json}
#
# See the README documentation for more examples.
#
