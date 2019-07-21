from .mysql_ import Mysql_
from .dbutil import MysqlUtil
from .regist_article import regist_article
from .scrapings import bussiness_insider,gigazine,wired,bbc,the_bridge,note
import random

def cash_article():
    with MysqlUtil() as mysqlutil:
        mysql = Mysql_(mysqlutil)
        site_name_list = mysql.fetch_site_names()
        random.shuffle(site_name_list)
        for site_name in site_name_list:    
            try:
                article = eval("{}.scraping()".format(site_name))
                print(article["site_name"])
            except:
                continue
            regist_article(mysql,article["site_name"],article["article_reporter"],article["article_url"],article["article_text"],article["article_title"],article["article_image"])    
        mysqlutil.commit()
if __name__ == "__main__":
    cash_article()
    
    
