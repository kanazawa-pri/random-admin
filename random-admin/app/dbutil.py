import pymysql.cursors
import os

os.environ['ROS_HOST'] = 'localhost'
os.environ['ROS_PORT'] = '3306'
os.environ['ROS_USER'] = 'root'
os.environ['ROS_PASSWORD'] = ''
os.environ['ROS_DB'] = 'random'
os.environ['ROS_CHARSET'] = 'utf8mb4'


class MysqlUtil():
    def __enter__(self):
        self.__conn = None
        self.__open()
        return self

    def __exit__(self,exception_type,exception_value,traceback):
        self.__close()
    
    def __open(self):
        if self.__conn is None:
            self.__conn = pymysql.connect(
                host=os.environ['ROS_HOST'],
                user=os.environ['ROS_USER'],
                port=int(os.environ['ROS_PORT']),
                password=os.environ['ROS_PASSWORD'],
                db=os.environ['ROS_DB'],
                charset=os.environ['ROS_CHARSET'],
                cursorclass=pymysql.cursors.DictCursor)

    def __close(self):
        if self.__conn is not None:
            self.__conn.close()
            self.__conn = None

    def commit(self):
        if self.__conn is not None:
            self.__conn.commit()

    def rollback(self):
        if self.__conn is not None:
            self.__conn.rollback()
    
    def exec(self,sql,params):
        if self.__conn is not None:
            with self.__conn.cursor() as cursur:
                cursur.execute(sql,params)
                return cursur.fetchall()
        else:
            raise Exception('connection is closed')

