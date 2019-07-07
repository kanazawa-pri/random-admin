# random-admin [メモ]



chalice + aws lambda + api gatewayでデプロイ


-----------定期実行------------

一時間ごとに、mysqlに登録してあるサイトから最新の記事をスクレイピングで取得し、mysqlへ保存。
複数のサイトから記事を取得するため、記事の本文を分析して、同一の出来事を書いた記事は複数以上取ってこないようにする。chalicelib/extract_top_words.py&regist_article.py


------------API概要------------------

"/" GET site情報を返す


>パラメータ　なし

>レスポンス {site_name:xxx,site_id:xxx}

"/" POST 記事を返す。


>body {user_id:xxx,ng_site_name:[xxx],ng_word_list:[xxx]}

>レスポンス　{article_id:xxx,article_title:xxx,article_url:xxx,article_image:xxx}

"/history" GET 「後で読む」に設定した記事を返す

>パラメータ　user_id

>レスポンス　{article_id:xxx,article_title:xxx,article_url:xxx,article_image:xxx}

"/history" POST　//ユーザーがクリックした記事(is_later =  0)、「後で読む」(is_later = 1)に設定した記事を保存する。

>body {user_id : xxx, article_id : xxx, is_later = x}

>レスポンス なし




