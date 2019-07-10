import nagisa

katakana = "ァアィイゥウェエォオカガキギクグケゲコゴサザシジスズセゼソゾタダチヂッツヅテデトドナニヌネノハバパヒビピフブプヘベペホボポマミムメモャヤュユョヨラリルレロヮワヰヱヲンヴ"


def extract_top_words(text):
    def __iskata(strj):
        return all([ch in katakana for ch in strj])

    def __iskanji(strj):
        return all(["一" <= ch <= "龥" for ch in strj])

    def __adjust_text(text, is_kana, num, cnt):
        if is_kana:
            text_list = [strj for strj in text if __iskata(strj)]
        else:
            text_list = [strj for strj in text if __iskanji(strj)]
        text_list = sorted({i: text_list.count(i) for i in set(text_list)}.items(), key=lambda x: x[1], reverse=True)
        del text_list[num:]
        for list_ in text_list:
            if list_[1] < cnt:
                text_list.remove(list_)
            if len(list_[0]) == 1:
                text_list.remove(list_)
        return [list_[0] for list_ in text_list]

    text = nagisa.extract(text, extract_postags=['名詞']).words
    top_word_list =  __adjust_text(text, True, 3, 2) + __adjust_text(text, False, 4, 3)

    return top_word_list

if __name__=="__main__":
    print(extract_top_words("私はボブです。私はボブです。パソコンが好きです。青森県に住んでいます。新聞を読んでいます。青森県に住んでいます。パソコンが好きです。"))
