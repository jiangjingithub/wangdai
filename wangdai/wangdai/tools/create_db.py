import pymysql

class PyMysql():
    def __init__(self,host="localhost",user="root",passwd=None, port=3306,db=None):
        """

        :param host: mysql链接ip
        :param user: 用户名
        :param passpw: 密码
        :param port: 端口默认3306
        :param db: 创建的数据库名
        """
        self.host = host
        self.user = user
        self.passwd = passwd
        self.port = port
        self.db = db
        self.connect = pymysql.connect(host=self.host,user=self.user,passwd=self.passwd,port=self.port)
        self.cursor = self.connect.cursor()
        sql = "create database if not exists %s charset='utf8'" % self.db
        # print(sql)
        self.cursor.execute(sql)
        self.cursor.close()
    def craete_table(self,sql):
        connect = pymysql.connect(host=self.host,user=self.user,passwd=self.passwd,port=self.port,db=self.db)
        cursor = connect.cursor()
        cursor.execute(sql)
        connect.close()
if __name__ == "__main__":
    db = PyMysql(passwd="jj890311",db="data")
    print("1")
    sql = "create table if not exists test(id int not null primary key auto_increment,name varchar(10))"
    db.craete_table(sql)