from .mysql_ import Mysql_
from .dbutil import MysqlUtil
from .regist_article import regist_article
from .scrapings import bussiness_insider,gigazine,wired
import random

def cash_article():
    with MysqlUtil() as mysqlutil:
        mysql = Mysql_(mysqlutil)
        site_name_list = mysql.fetch_sites_name()
        print(site_name_list)
        for site_name in site_name_list:    
            try:
                article = eval("{}.scraping()".format(site_name))
            except:
                continue
            print(article["site_name"])
            regist_article(mysql,article["site_name"],article["article_url"],article["article_text"],article["article_title"],article["article_image"])    
        mysqlutil.commit()
if __name__ == "__main__":
    cash_article()
    
    