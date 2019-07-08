
class Mysql_():
    def __init__(self,mysqlutil):
        self.__mysqlutil = mysqlutil

    def fetch_sites(self):
        return list(self.__mysqlutil.exec('''
                                select * from sites
                            ''',()))
    
    def fetch_sites_name(self):
        return [i["site_name"] for i in self.__mysqlutil.exec('''
                                select site_name from sites
                            ''',())]

    def fetch_user_history(self,user_id,is_later):
        condition = "and is_later = 1" if is_later else ""
        return [i["article_id"] for i in self.__mysqlutil.exec('''
                                        select article_id from user_article_history
                                        where user_id = %s
                                        and updated_at > ( NOW( ) - INTERVAL 1 DAY)
                                        {}
                                        '''.format(condition),(user_id))]

    def fetch_top_words(self):
        return [i["top_words"] for i in self.__mysqlutil.exec('''
                                select top_words from articles
                                where updated_at > ( NOW( ) - INTERVAL 1 DAY )
                            ''',())]
        


    def fetch_article_for_user(self,user_id,ng_site_name_list,ng_word_list):
        article_id_list = self.fetch_user_history(user_id,False)
        return list(self.__mysqlutil.exec('''
                                            select article_id,site_name,article_url,article_title,article_image,red,blue,green from articles
                                            INNER JOIN sites
                                            USING(site_name)
                                            where updated_at > ( NOW( ) - INTERVAL 1 DAY )
                                            and article_id not in (%s)
                                             and site_name not in (%s)
                                        ''',(",".join(map(str,article_id_list)),",".join(ng_site_name_list))))
    
    def is_registed(self,article_url):
        return True if len(self.__mysqlutil.exec('''
                                       select * from articles
                                       where article_url = %s 
                                        ''',(article_url))) > 0 else False

    def regist_user_history(self,user_id,article_id,is_later):
        self.__mysqlutil.exec('''
                                INSERT INTO user_article_history(user_id, article_id, is_later) 
                                VALUES(%s, %s, %s)
                                ON DUPLICATE KEY UPDATE is_later = if(is_later = 1, is_later, values(is_later));
                            ''',(user_id,article_id,is_later))
    
    def regist_article(self,article_id,site_name,article_url,top_word_list,article_title,article_image):
        self.__mysqlutil.exec('''
                            insert into articles(article_id,article_url,site_name,top_words,article_title,article_image)
                            values(%s,%s,%s,%s,%s,%s)
                            ''',(article_id,article_url,site_name,",".join(top_word_list),article_title,article_image))

if __name__ == "__main__":
    from dbutil import MysqlUtil
    with MysqlUtil() as mysqlutil:
        mysql = Mysql_(mysqlutil)
        print(mysql.fetch_article_for_user(1,["test"],["test"]))
        mysqlutil.commit()
