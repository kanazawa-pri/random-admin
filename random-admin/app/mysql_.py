
class Mysql_():
    def __init__(self, mysqlutil):
        self.__mysqlutil = mysqlutil

    def fetch_site_names(self):
        return [i["site_name"] for i in self.__mysqlutil.exec('''
                                                        select site_name from sites
                                                        ''',())]

    def fetch_top_words(self):
        return self.__mysqlutil.exec('''
                                select article_id,top_words from articles
                                where updated_at > ( NOW( ) - INTERVAL 8 HOUR )
                            ''', ())

    def fetch_article_for_user(self, user_id, page, ng_sites):
        start = (page-1) * 12
        end = start + 11
        recent_article_list = list(self.__mysqlutil.exec('''
                                            select article_id,site_name,article_reporter,article_url,article_title,article_image,red,blue,green,1 as is_later from articles a
                                            INNER JOIN sites USING(site_name)
                                            where updated_at > ( NOW( ) - INTERVAL 12 HOUR )
                                            and NOT EXISTS (SELECT article_id FROM user_article_history u WHERE user_id = %s and u.article_id = a.article_id and updated_at > ( NOW( ) - INTERVAL 1 DAY))
                                            and ((sites.site_name not in ({})) or (attention_degree > 1))
                                            ORDER BY attention_degree DESC, updated_at DESC
                                            limit %s,%s
					'''.format(ng_sites),(user_id,start,end)))
        if page ==1:
            later_article_list = list(self.__mysqlutil.exec('''
                                    select articles.article_id,site_name,article_reporter,article_url,article_title,article_image,red,blue,green,is_later from articles
                                    INNER JOIN sites USING(site_name)
                                    INNER JOIN (SELECT ht.article_id,ht.is_later from user_article_history ht WHERE ht.user_id = %s AND ht.is_later = 4 and ht.updated_at > ( NOW( ) - INTERVAL 12 HOUR)) as st2
                                    USING(article_id)
                                    where updated_at > ( NOW( ) - INTERVAL 12 HOUR )
                                    ORDER BY updated_at DESC
                '''.format(ng_sites),(user_id)))
            if len(recent_article_list) > 1:
                return [recent_article_list[0]] + later_article_list + recent_article_list[1:]
            else:
                return recent_article_list + later_article_list
        return recent_article_list
    
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

    def regist_article(self,article_id,site_name,article_reporter,article_url,top_word_list,article_title,article_image):
        self.__mysqlutil.exec('''
                            insert into articles(article_id,article_url,site_name,article_reporter,top_words,article_title,article_image)
                            values(%s,%s,%s,%s,%s,%s,%s)
                            ''',(article_id,article_url,site_name,article_reporter,",".join(top_word_list),article_title,article_image))
        return
    
    def update_user_info(self,user_id,user_fav_reporters,user_ng_sites):
        self.__mysqlutil.exec('''
                                INSERT INTO users_info(user_id, user_fav_reporters,user_ng_sites) 
                                VALUES(%s, %s, %s)
				                on duplicate key update user_fav_reporters=%s,user_ng_sites=%s
                            ''',(user_id,user_fav_reporters,user_ng_sites,user_fav_reporters,user_ng_sites))
        return

    def update_attention_degree(self,article_id,top_word_list,article_url,site_name,article_title,article_image):
        self.__mysqlutil.exec('''
                            update articles 
                            SET attention_degree = attention_degree + 1,
                                article_url = %s,
                                site_name = %s,
                                top_words = %s,
                                article_title = %s,
                                article_image = %s
                            WHERE article_id=%s
                            ''',(article_url,site_name,",".join(top_word_list),article_title,article_image,article_id))
        return
