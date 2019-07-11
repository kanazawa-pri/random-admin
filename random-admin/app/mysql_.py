
class Mysql_():
    def __init__(self, mysqlutil):
        self.__mysqlutil = mysqlutil

    def fetch_site_names(self):
        return [i["site_name"] for i in self.__mysqlutil.exec('''
                                                        select site_name from sites
                                                        ''',())]

    def fetch_top_words(self):
        return [i["top_words"] for i in self.__mysqlutil.exec('''
                                select top_words from articles
                                where updated_at > ( NOW( ) - INTERVAL 1 DAY )
                            ''', ())]

    def fetch_article_for_user(self, user_id, page, ng_sites):
        start = (page-1) * 6
        end = start + 6
        later_article_list = list(self.__mysqlutil.exec('''
                                            select articles.article_id,site_name,article_url,article_title,article_image,red,blue,green,is_later from articles
                                            INNER JOIN sites USING(site_name)
                                            INNER JOIN (SELECT ht.article_id,ht.is_later from user_article_history ht WHERE ht.user_id = %s AND ht.is_later != 4 and ht.updated_at > ( NOW( ) - INTERVAL 12 HOUR)) as st2
                                            USING(article_id)
                                            where sites.site_name not in ({})
                                            limit %s,%s
					   '''.format(ng_sites),(user_id,start,end)))
        end = start + 6 - len(later_article_list)
        if len(later_article_list) == 7:
            return later_article_list
        recent_article_list = list(self.__mysqlutil.exec('''
                                            select article_id,site_name,article_url,article_title,article_image,red,blue,green,1 as is_later from articles a
                                            INNER JOIN sites USING(site_name)
                                            where updated_at > ( NOW( ) - INTERVAL 2 DAY )
                                            and NOT EXISTS (SELECT article_id FROM user_article_history u WHERE user_id = %s and u.article_id = a.article_id and updated_at > ( NOW( ) - INTERVAL 1 DAY))
                                            and sites.site_name not in ({})
                                            limit %s,%s
					'''.format(ng_sites),(user_id,start,end)))
        print(later_article_list,recent_article_list)
        return later_article_list + recent_article_list
    
    def is_registed(self,article_url):
        return True if len(self.__mysqlutil.exec('''
                                       select * from articles
                                       where article_url = %s 
                                        ''',(article_url))) > 0 else False

    def regist_user_history(self,user_id,article_id,is_later):
        self.__mysqlutil.exec('''
                                INSERT INTO user_article_history(user_id, article_id, is_later) 
                                VALUES(%s, %s, %s)
				                on duplicate key update is_later=%s
                            ''',(user_id,article_id,is_later,is_later))
        return

    def regist_article(self,article_id,site_name,article_url,top_word_list,article_title,article_image):
        self.__mysqlutil.exec('''
                            insert into articles(article_id,article_url,site_name,top_words,article_title,article_image)
                            values(%s,%s,%s,%s,%s,%s)
                            ''',(article_id,article_url,site_name,",".join(top_word_list),article_title,article_image))
        return
