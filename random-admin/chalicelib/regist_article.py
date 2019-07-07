from .extract_top_words import extract_top_words
import random

def regist_article(mysql,site_name,article_url,text,article_title,article_image):
    def __is_similar(top_word_list1,top_word_list2):
        top_word_list = top_word_list1 + top_word_list2
        return True if len(top_word_list) != len(set(top_word_list)) else False

    def __grant_article_id(mysql,top_word_list):
        top_word_lists = mysql.fetch_top_words()
        for top_word in top_word_lists:
            if __is_similar(top_word_list,top_word.split(",")):
                return 1
        return random.randint(1000000,99999999)
    if mysql.is_registed(article_url):
        print("すでに同じURLが登録されています")
        return
    top_word_list = extract_top_words(text)
    article_id = __grant_article_id(mysql,top_word_list)
    if article_id == 1:
        ("同じ内容の記事がすでに登録されています。")
        return
    mysql.regist_article(article_id,site_name,article_url,top_word_list,article_title,article_image)


